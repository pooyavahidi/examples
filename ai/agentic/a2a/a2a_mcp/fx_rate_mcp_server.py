from typing import Optional
import yfinance as yf
from mcp.server.fastmcp import FastMCP
from utils import setup_logger

logger = setup_logger(__name__, level="INFO")

mcp = FastMCP("fxrate")


@mcp.tool()
def fetch_exchange_rate(base: str, quote: str) -> Optional[float]:
    """fetch current exchange rate for foreign exchange pair.
    Args:
        base: Base currency code (e.g., "USD")
        quote: Quote currency code (e.g., "EUR")
    Returns:
        Current exchange rate as a float, or None if not available.
    """
    try:
        # Create Yahoo Finance symbol
        symbol = f"{base}{quote}=X"

        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")

        if not data.empty:
            # Get the most recent close price.
            return float(data["Close"].iloc[-1])
    except Exception as err:
        logger.error("Error fetching exchange rate: %s", err)

    return None


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
