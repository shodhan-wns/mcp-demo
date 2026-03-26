"""Store all utility and helper functions to be used in MCP tools."""

import json
from pathlib import Path
from uuid import UUID


BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / "data"
PERSONS_DATA = json.load(open(DATA_PATH / "persons.json", "r"))
ACCOUNTS_DATA = json.load(open(DATA_PATH / "accounts.json", "r"))
TRANSACTIONS_DATA = json.load(open(DATA_PATH / "transactions.json", "r"))


def get_persons_count():
    return len(PERSONS_DATA)


def search_persons_by_name(search_str: str) -> list[dict]:
    """Search for persons matching their names."""
    return [
        person for person in PERSONS_DATA
        if search_str.lower() in person["name"].lower()
    ]


def search_persons_by_country(country: str) -> list[dict]:
    """Search for persons matching the country."""
    return [
        person for person in PERSONS_DATA
        if country.lower() in person["country"].lower()
    ]

def get_all_accounts_for_person(person_id: UUID) -> list[dict]:
    """Get all accounts for a specific person."""
    return [
        account for account in ACCOUNTS_DATA
        if account["person_id"] == person_id
    ]
