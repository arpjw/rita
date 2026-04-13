from data.base import DataConnector

class NorgateConnector(DataConnector):
    """
    Stub adapter for Norgate futures pricing.
    Requires a local Norgate Data subscription and the norgatedata Python package.
    Not required for v1 — /brief and /regime function without this connector.

    To implement:
      1. pip install norgatedata
      2. Configure NORGATE_DATA_PATH in .env
      3. Implement fetch() to return a dict of {symbol: {price, volume, open_interest}}
    """
    TTL = 3600

    async def fetch(self) -> dict:
        return {"error": "Norgate connector not yet implemented. See CONTRIBUTING.md."}
