import os
import json
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_server.settings')

import django
django.setup()

from bank_server.bank_app.models import Person, BankAccount, Transaction    # noqa: E402


DATA_DIR = Path(__file__).parent / 'data'


def seed():
    with open(DATA_DIR / 'persons.json') as f:
        persons_data = json.load(f)

    with open(DATA_DIR / 'accounts.json') as f:
        accounts_data = json.load(f)

    # Build hex_account_id → hex_person_id from nested accounts in persons.json
    account_to_person_hex = {}
    for person in persons_data:
        for account in person.get('accounts', []):
            account_to_person_hex[account['id']] = person['id']

    # Insert persons, keep hex_id → Person object mapping
    print("Inserting persons...")
    hex_to_person = {}
    for p in persons_data:
        person = Person.objects.create(
            name=p['name'],
            email='',
            phone_number=p.get('phone_number', ''),
        )
        hex_to_person[p['id']] = person
    print(f"  {len(hex_to_person)} persons inserted")

    # Insert accounts, keep hex_id → BankAccount object mapping
    print("Inserting accounts...")
    hex_to_account = {}
    for a in accounts_data:
        person_hex = account_to_person_hex.get(a['id'])
        if not person_hex:
            print(f"  Skipping account {a['id']} — no matching person")
            continue
        account = BankAccount.objects.create(
            account_number=a['account_number'],
            iban=a['iban'],
            balance=a['balance'],
            person=hex_to_person[person_hex],
        )
        hex_to_account[a['id']] = account
    print(f"  {len(hex_to_account)} accounts inserted")

    # Insert transactions using bulk_create to bypass Transaction.save()
    # (which would update balances and double-count)
    print("Inserting transactions...")
    transactions = []
    for a in accounts_data:
        account = hex_to_account.get(a['id'])
        if not account:
            continue
        for t in a.get('transactions', []):
            tr_type = t['transaction_type']
            if tr_type == 'invoice':
                tr_type = 'deposit'
            transactions.append(Transaction(
                createdAt=t['createdAt'],
                transaction_type=tr_type,
                transaction_description=t['transaction_description'],
                transactin_amount=t['transactin_amount'],
                bank_account=account,
            ))
    Transaction.objects.bulk_create(transactions)
    print(f"  {len(transactions)} transactions inserted")


if __name__ == '__main__':
    seed()
