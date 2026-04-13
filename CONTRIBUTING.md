# Contributing to Rita

The most impactful contribution is adding a new data connector. Rita's connector architecture is intentionally minimal — any source that returns a structured dict can be plugged in.

## Adding a Data Connector

1. Create a new file in `data/` (e.g., `data/coinglass.py`)
2. Subclass `DataConnector` from `data/base.py`
3. Implement the `async def fetch(self) -> dict` method
4. Use `_get_cached` / `_set_cached` for TTL-based caching
5. Register your connector in the relevant command file

```python
from data.base import DataConnector

class MyConnector(DataConnector):
    TTL = 900

    async def fetch(self) -> dict:
        cached = self._get_cached("my_source")
        if cached:
            return cached
        # ... fetch data ...
        self._set_cached("my_source", result)
        return result
```

## Guidelines

- All connectors must be async
- API keys must be read from environment variables, never hardcoded
- Connectors must degrade gracefully on network failure
- Add your connector's required env vars to `.env.example` with a comment

## Roadmap

Open issues are tracked in the [Linear project](https://linear.app/monolithsystematicllc/project/rita-macro-research-discord-bot-577cc7bbfb2d).
Priority areas for community contributions:
- COT (Commitments of Traders) positioning connector
- Bloomberg / Refinitiv adapter (for users with terminal access)
- Norgate futures pricing connector
- ECB / BOJ / BOE data adapters
