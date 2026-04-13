import discord
from discord import app_commands
from discord.ext import commands
from data.lumina import LuminaConnector
from intelligence.analyst import complete
from intelligence.prompts import REGIME_INTERPRETATION_PROMPT

lumina = LuminaConnector()

REGIME_COLORS = {
    "Risk-On":          0x38A169,
    "Risk-Off":         0xE53E3E,
    "Stagflationary":   0xED8936,
    "Disinflationary":  0x4299E1,
    "Transitional":     0xA0AEC0,
}

def _confidence_bar(score: float) -> str:
    filled = int(score / 10)
    return "█" * filled + "░" * (10 - filled) + f" {score:.0f}%"

class Regime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="regime", description="Current macro regime classification powered by the Lumina backend.")
    async def regime(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        data = await lumina.fetch()

        if "error" in data:
            await interaction.followup.send(f"⚠️ {data['error']}")
            return

        label = data.get("label", "Unknown")
        confidence = data.get("confidence", 0)
        signals = data.get("top_signals", [])

        interpretation = await complete(
            REGIME_INTERPRETATION_PROMPT.format(
                label=label,
                confidence=confidence,
                signals=", ".join(f"{s['name']} {s['direction']}" for s in signals),
            )
        )

        color = REGIME_COLORS.get(label, 0xA0AEC0)
        embed = discord.Embed(title="Rita — Macro Regime", color=color)
        embed.add_field(name="Regime", value=f"**{label}**", inline=True)
        embed.add_field(name="Confidence", value=_confidence_bar(confidence), inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)

        signal_lines = "\n".join(
            f"{'↑' if s['direction'] == 'positive' else '↓'} **{s['name']}** — {s.get('value', '')}"
            for s in signals[:3]
        )
        embed.add_field(name="Top Signals", value=signal_lines or "n/a", inline=False)
        embed.add_field(name="Interpretation", value=interpretation.strip(), inline=False)
        embed.set_footer(text="Rita by Monolith Systematic LLC — Powered by Lumina")

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Regime(bot))
