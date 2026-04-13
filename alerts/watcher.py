import asyncio
import discord
from dataclasses import dataclass, field
from typing import Literal
from data.fred import FREDConnector
from data.kalshi import KalshiConnector
from intelligence.analyst import complete
from intelligence.prompts import ALERT_CONTEXT_PROMPT

fred = FREDConnector()
kalshi = KalshiConnector()

SUPPORTED_VARIABLES = ["10y_yield", "2s10s", "dxy", "fed_funds", "cpi_yoy"]
MAX_ALERTS = 10
POLL_INTERVAL = 900

@dataclass
class Alert:
    id: str
    user_id: int
    variable: str
    direction: Literal["above", "below"]
    threshold: float
    triggered: bool = False

alerts: dict[str, list[Alert]] = {}

def _user_key(user_id: int) -> str:
    return str(user_id)

def add_alert(user_id: int, variable: str, direction: str, threshold: float) -> Alert | str:
    key = _user_key(user_id)
    user_alerts = alerts.setdefault(key, [])
    if len(user_alerts) >= MAX_ALERTS:
        return f"Alert limit reached ({MAX_ALERTS} max). Cancel an existing alert first."
    if variable not in SUPPORTED_VARIABLES:
        return f"Unsupported variable. Choose from: {', '.join(SUPPORTED_VARIABLES)}"
    alert_id = f"{variable}_{direction}_{threshold}_{user_id}"
    alert = Alert(id=alert_id, user_id=user_id, variable=variable, direction=direction, threshold=threshold)
    user_alerts.append(alert)
    return alert

def remove_alert(user_id: int, alert_id: str) -> bool:
    key = _user_key(user_id)
    before = len(alerts.get(key, []))
    alerts[key] = [a for a in alerts.get(key, []) if a.id != alert_id]
    return len(alerts[key]) < before

def list_alerts(user_id: int) -> list[Alert]:
    return alerts.get(_user_key(user_id), [])

async def _poll(bot: discord.Client):
    try:
        fred_data = await fred.fetch()
        kalshi_data = await kalshi.fetch()
    except Exception:
        return

    data_map = {
        "10y_yield": fred_data.get("10y_yield", {}).get("value"),
        "2s10s":     fred_data.get("2s10s", {}).get("value"),
        "dxy":       fred_data.get("dxy", {}).get("value"),
        "fed_funds": fred_data.get("fed_funds", {}).get("value"),
        "cpi_yoy":   fred_data.get("cpi_yoy", {}).get("value"),
    }

    for user_key, user_alerts in alerts.items():
        for alert in user_alerts:
            val = data_map.get(alert.variable)
            if val is None:
                continue
            breached = (alert.direction == "above" and val > alert.threshold) or \
                       (alert.direction == "below" and val < alert.threshold)
            if breached and not alert.triggered:
                alert.triggered = True
                context = await complete(
                    ALERT_CONTEXT_PROMPT.format(
                        variable=alert.variable,
                        value=val,
                        direction=alert.direction,
                        threshold=alert.threshold,
                    )
                )
                user = await bot.fetch_user(alert.user_id)
                if user:
                    await user.send(
                        f"🔔 **Rita Alert** — `{alert.variable}` is {alert.direction} `{alert.threshold}`\n"
                        f"Current: **{val:.4f}**\n{context.strip()}"
                    )
            elif not breached:
                alert.triggered = False

def start_watcher(bot: discord.Client):
    async def loop():
        while True:
            await _poll(bot)
            await asyncio.sleep(POLL_INTERVAL)
    asyncio.create_task(loop())
