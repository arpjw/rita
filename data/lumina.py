import os
import httpx
from data.base import DataConnector

class LuminaConnector(DataConnector):
    TTL = 300

    def __init__(self):
        self._base_url = os.environ.get("LUMINA_API_URL")

    def is_configured(self) -> bool:
        return bool(self._base_url)

    async def fetch(self) -> dict:
        if not self.is_configured():
            return {"error": "Lumina backend not configured. Set LUMINA_API_URL in .env."}

        cached = self._get_cached("lumina_regime")
        if cached:
            return cached

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self._base_url}/regime/current", timeout=5)
                resp.raise_for_status()
                result = resp.json()
                self._set_cached("lumina_regime", result)
                return result
        except httpx.TimeoutException:
            return {"error": "Lumina backend timed out."}
        except Exception as e:
            return {"error": str(e)}
