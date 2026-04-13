import os
import httpx
from data.base import DataConnector

KALSHI_BASE = "https://trading-api.kalshi.com/trade-api/v2"

MACRO_TAGS = ["fed", "inflation", "gdp", "unemployment", "rates"]

class KalshiConnector(DataConnector):
    TTL = 900

    def __init__(self):
        self._api_key = os.environ["KALSHI_API_KEY"]

    async def fetch(self) -> dict:
        cached = self._get_cached("kalshi")
        if cached:
            return cached

        headers = {"Authorization": f"Token {self._api_key}"}
        markets = []

        async with httpx.AsyncClient() as client:
            for tag in MACRO_TAGS:
                try:
                    resp = await client.get(
                        f"{KALSHI_BASE}/markets",
                        headers=headers,
                        params={"tag": tag, "status": "open", "limit": 5},
                        timeout=10,
                    )
                    resp.raise_for_status()
                    for m in resp.json().get("markets", []):
                        markets.append({
                            "title": m.get("title"),
                            "slug": m.get("ticker"),
                            "yes_bid": m.get("yes_bid", 0) / 100,
                            "volume": m.get("volume", 0),
                        })
                except Exception:
                    continue

        markets.sort(key=lambda x: x["volume"], reverse=True)
        result = {"top_markets": markets[:5]}
        self._set_cached("kalshi", result)
        return result
