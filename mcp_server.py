from pathlib import Path
import logging
from mcp.server.fastmcp import FastMCP

from mcp_utils import (
    get_persons_count,
    search_persons_by_name,
    get_person_detail,
    get_all_accounts_for_person,
    get_balance_for_person,
    get_transactions_for_account,
)


# Initialize FastMCP server
mcp = FastMCP("bank")
mcp.settings.host = "127.0.0.1"
# mcp.settings.host = "0.0.0.0"     # uncomment this for Docker setup
mcp.settings.port = 5002


@mcp.resource("resource://blacklisted_accounts")
async def get_blacklisted_accounts():
    """Return a list of blacklisted account numbers."""
    blacklisted_file = Path(__file__).parent / "blacklisted_accounts.txt"
    if not blacklisted_file.exists():
        return []
    with blacklisted_file.open() as f:
        return [line.strip() for line in f if line.strip()]


@mcp.tool()
async def get_persons_count_tool() -> int:
    """Get the total count of persons."""
    return await get_persons_count()


@mcp.tool()
async def search_persons_by_name_tool(search_str: str) -> list[dict]:
    """Search for persons matching the search string."""
    return await search_persons_by_name(search_str)


@mcp.tool()
async def get_person_detail_tool(person_id: str) -> dict:
    """Get a person's details including their accounts."""
    return await get_person_detail(person_id)


@mcp.tool()
async def get_all_accounts_for_person_tool(person_id: str) -> list[dict]:
    """Get all accounts for a specific person."""
    return await get_all_accounts_for_person(person_id)


@mcp.tool()
async def get_balance_for_person_tool(person_id: str) -> dict:
    """Get balances for all accounts of a person.

    Returns a dict with account numbers as keys and balance as values,
    plus a 'total' key with the sum of all balances.
    """
    return await get_balance_for_person(person_id)


@mcp.tool()
async def get_transactions_for_account_tool(account_id: str, last_n: int = 10) -> list[dict]:
    """Get the last N transactions for a specific account."""
    return await get_transactions_for_account(account_id, last_n)


def main():
    logging.info("Starting MCP server...")
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
