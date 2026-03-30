import httpx

DJANGO_API_BASE = "http://127.0.0.1:8000/api"


async def make_request(method, url, **params):
    """Make generic HTTP request."""
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, **params)
        response.raise_for_status()
        return response.json()


async def get_persons_count() -> int:
    """Get the total count of persons."""
    resp = await make_request("GET", f"{DJANGO_API_BASE}/persons/")
    return len(resp)


async def search_persons_by_name(search_str: str) -> list[dict]:
    """Search for persons matching the search string."""
    resp = await make_request("GET", f"{DJANGO_API_BASE}/persons/", params={"search": search_str})
    return resp


async def get_person_detail(person_id: str) -> dict:
    """Get a person's details including their accounts."""
    resp = await make_request("GET", f"{DJANGO_API_BASE}/persons/{person_id}/")
    return resp


async def get_all_accounts_for_person(person_id: str) -> list[dict]:
    """Get all accounts for a specific person."""
    resp = await make_request("GET", f"{DJANGO_API_BASE}/accounts/", params={"person_id": person_id})
    return resp


async def get_balance_for_person(person_id: str) -> dict:
    """Get balances for all accounts of a person.

    Returns a dict with account numbers as keys and balance as values,
    plus a 'total' key with the sum of all balances.
    """
    accounts = await get_all_accounts_for_person(person_id)
    result = {account["account_number"]: float(account["balance"]) for account in accounts}
    result["total"] = sum(result.values())
    return result


async def get_transactions_for_account(account_id: str, last_n: int = 10) -> list[dict]:
    """Get the last N transactions for a specific account."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DJANGO_API_BASE}/transactions/",
            params={"account_id": account_id, "last_n": last_n},
        )
        response.raise_for_status()
        return response.json()
