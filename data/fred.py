import os
from fredapi import Fred
from data.base import DataConnector

SERIES = {
    "10y_yield":    "DGS10",
    "2y_yield":     "DGS2",
    "real_yield":   "DFII10",
    "2s10s":        None,
    "dxy":          "DTWEXBGS",
    "eurusd":       "DEXUSEU",
    "usdjpy":       "DEXJPUS",
    "ig_spread":    "BAMLC0A0CM",
    "hy_spread":    "BAMLH0A0HYM2",
    "fed_funds":    "FEDFUNDS",
    "cpi_yoy":      "CPIAUCSL",
}

class FREDConnector(DataConnector):
    TTL = 900

    def __init__(self):
        self._fred = Fred(api_key=os.environ["FRED_API_KEY"])

    async def fetch(self) -> dict:
        cached = self._get_cached("fred")
        if cached:
            return cached

        result = {}
        for key, series_id in SERIES.items():
            if series_id is None:
                continue
            try:
                s = self._fred.get_series(series_id, observation_start="2020-01-01")
                latest = float(s.dropna().iloc[-1])
                prev = float(s.dropna().iloc[-2])
                result[key] = {"value": latest, "delta": round(latest - prev, 4)}
            except Exception:
                result[key] = {"value": None, "delta": None}

        if result.get("2y_yield") and result.get("10y_yield"):
            spread = round(result["10y_yield"]["value"] - result["2y_yield"]["value"], 4)
            prev_spread = round(
                (result["10y_yield"]["value"] - result["10y_yield"]["delta"]) -
                (result["2y_yield"]["value"] - result["2y_yield"]["delta"]), 4
            )
            result["2s10s"] = {"value": spread, "delta": round(spread - prev_spread, 4)}

        self._set_cached("fred", result)
        return result
