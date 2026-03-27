import logging
import httpx
from mcp.server.fastmcp import FastMCP

from utils import (
    get_persons_count,
    search_persons_by_name,
    search_persons_by_country,
    get_all_accounts_for_person,
)


# Initialize FastMCP server
mcp = FastMCP("bank")
mcp.settings.host = "0.0.0.0"   # for Docker, change to 127.0.0.1 for non-Docker setup
mcp.settings.port = 5002


@mcp.tool()
def get_persons_count_tool() -> int:
    """Get the total count of persons."""
    return get_persons_count()


@mcp.tool()
def search_persons_by_name_tool(search_str: str) -> list[dict]:
    """Search for persons matching the search string."""
    return search_persons_by_name(search_str)


@mcp.tool()
def search_persons_by_country_tool(country: str) -> list[dict]:
    """Search for persons from a specific country."""
    return search_persons_by_country(country)


@mcp.tool()
def get_all_accounts_for_person_tool(person_id: str) -> list[dict]:
    """Get all accounts for a specific person."""
    return get_all_accounts_for_person(person_id)


@mcp.tool()
def get_balance_for_person_tool(person_id: str) -> float:
    """Get the total balance for all accounts for a specific person."""
    accounts = get_all_accounts_for_person(person_id)
    return [
        {
            "iban": account["iban"],
            "currency": account["currency_code"],
            "total_balance": account["balance"],
        }
        for account in accounts
    ]


def main():
    # Initialize and run the server
    logging.info("Starting MCP server...")
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()