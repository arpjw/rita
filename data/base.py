from abc import ABC, abstractmethod
from typing import Any
import time

class DataConnector(ABC):
    _cache: dict[str, tuple[Any, float]] = {}
    TTL: int = 900

    def _get_cached(self, key: str) -> Any | None:
        if key in self._cache:
            value, ts = self._cache[key]
            if time.time() - ts < self.TTL:
                return value
        return None

    def _set_cached(self, key: str, value: Any) -> None:
        self._cache[key] = (value, time.time())

    @abstractmethod
    async def fetch(self) -> dict[str, Any]:
        pass
