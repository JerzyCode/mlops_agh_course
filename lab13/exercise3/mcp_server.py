from datetime import datetime

from fastmcp import FastMCP

mcp = FastMCP("date_time_server")


@mcp.tool(
    description="Get the current date. You MUST call this tool before request to establish what's current date."
)
def get_current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


@mcp.tool(
    description="Returns current date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS) You MUST call this tool before request to establish 'date'."
)
def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)
