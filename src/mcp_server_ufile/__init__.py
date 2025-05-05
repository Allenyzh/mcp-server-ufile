from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from . import playwright_starter

# Initialize FastMCP server
mcp = FastMCP("mcp-server-ufile")

WEB_URL = "https://www.ufile.ca"
USER_AGENT = "mcp-server-ufile/1.0"

@mcp.tool()
async def open_url(url: str) -> str:
    """
    Opens a URL in the browser.

    Args:
        url (str): The URL to open.
    """
    return await playwright_starter.run(url)


def main():
    print("Hello from mcp-server-ufile!")

if __name__ == "__main__":
    main()
