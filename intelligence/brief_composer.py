import discord
import json
from datetime import datetime, timezone
from intelligence.analyst import complete
from intelligence.prompts import BRIEF_FED_POSTURE_PROMPT

REGIME_COLORS = {
    "hawkish":  0xE53E3E,
    "neutral":  0xECC94B,
    "dovish":   0x38A169,
}

def _delta_str(delta: float | None, unit: str = "") -> str:
    if delta is None:
        return "n/a"
    sign = "+" if delta > 0 else ""
    return f"{sign}{delta:.2f}{unit}"

def _bar(value: float, max_val: float = 5.0, length: int = 10) -> str:
    filled = min(int((value / max_val) * length), length)
    return "█" * filled + "░" * (length - filled)

async def compose_brief(fred: dict, kalshi: dict) -> discord.Embed:
    data_summary = json.dumps({k: v for k, v in fred.items()}, indent=2)
    fed_posture_raw = await complete(BRIEF_FED_POSTURE_PROMPT.format(data=data_summary))
    fed_posture = fed_posture_raw.strip()

    posture_lower = fed_posture.lower()
    color = REGIME_COLORS.get(
        "hawkish" if "hawkish" in posture_lower else
        "dovish" if "dovish" in posture_lower else "neutral",
        0xA0AEC0
    )

    embed = discord.Embed(
        title="Rita — Morning Macro Brief",
        color=color,
        timestamp=datetime.now(timezone.utc),
    )

    rates = fred
    embed.add_field(
        name="📈 Rates",
        value=(
            f"**10Y UST** {rates.get('10y_yield', {}).get('value', 'n/a'):.2f}% "
            f"({_delta_str(rates.get('10y_yield', {}).get('delta'), '%')})\n"
            f"**2s10s** {rates.get('2s10s', {}).get('value', 'n/a'):.0f}bps "
            f"({_delta_str(rates.get('2s10s', {}).get('delta'), 'bps')})\n"
            f"**Real Yield** {rates.get('real_yield', {}).get('value', 'n/a'):.2f}% "
            f"({_delta_str(rates.get('real_yield', {}).get('delta'), '%')})"
        ),
        inline=True,
    )

    embed.add_field(
        name="💱 FX",
        value=(
            f"**DXY** {rates.get('dxy', {}).get('value', 'n/a'):.2f} "
            f"({_delta_str(rates.get('dxy', {}).get('delta'))})\n"
            f"**EURUSD** {rates.get('eurusd', {}).get('value', 'n/a'):.4f} "
            f"({_delta_str(rates.get('eurusd', {}).get('delta'))})\n"
            f"**USDJPY** {rates.get('usdjpy', {}).get('value', 'n/a'):.2f} "
            f"({_delta_str(rates.get('usdjpy', {}).get('delta'))})"
        ),
        inline=True,
    )

    embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.add_field(
        name="🏦 Credit",
        value=(
            f"**IG Spread** {rates.get('ig_spread', {}).get('value', 'n/a'):.0f}bps "
            f"({_delta_str(rates.get('ig_spread', {}).get('delta'), 'bps')})\n"
            f"**HY Spread** {rates.get('hy_spread', {}).get('value', 'n/a'):.0f}bps "
            f"({_delta_str(rates.get('hy_spread', {}).get('delta'), 'bps')})"
        ),
        inline=True,
    )

    markets = kalshi.get("top_markets", [])[:3]
    kalshi_lines = "\n".join(
        f"**{m['title'][:40]}** — {m['yes_bid']:.0%}" for m in markets
    ) or "No active markets"
    embed.add_field(name="🎲 Prediction Markets", value=kalshi_lines, inline=True)

    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="🏛 Fed Posture", value=fed_posture, inline=False)
    embed.set_footer(text="Rita by Monolith Systematic LLC — arpjw/rita")

    return embed
