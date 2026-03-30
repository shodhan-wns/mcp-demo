import uuid

from django.db import models
from django.utils import timezone


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_number = models.CharField(max_length=50)
    iban = models.CharField(max_length=34)
    balance = models.DecimalField(max_digits=14, decimal_places=2)
    person = models.ForeignKey(Person, related_name="accounts", on_delete=models.CASCADE)

    def __str__(self):
        return f"A/C {self.account_number} for {self.person}"


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        WITHDRAWAL = "withdrawal", "Withdrawal"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateTimeField()
    transaction_type = models.CharField(max_length=50, choices=TransactionType.choices)
    transaction_description = models.TextField()
    transactin_amount = models.DecimalField(max_digits=14, decimal_places=2)
    bank_account = models.ForeignKey(
        BankAccount,
        related_name="transactions",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.transaction_type} on A/C {self.bank_account.account_number}"

    def save(self, *args, **kwargs):
        self.createdAt = timezone.now()
        super().save(*args, **kwargs)

        # Update the balance of the associated bank account
        if self.transaction_type == "deposit":
            self.bank_account.balance += self.transactin_amount
        elif self.transaction_type == "withdrawal":
            self.bank_account.balance -= self.transactin_amount
        else:
            raise ValueError("Invalid transaction type")
        self.bank_account.save()
