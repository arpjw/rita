import discord
from discord import app_commands
from discord.ext import commands
from data.fred import FREDConnector
from data.kalshi import KalshiConnector
from intelligence.brief_composer import compose_brief

fred = FREDConnector()
kalshi = KalshiConnector()

class Brief(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="brief", description="Morning macro snapshot — rates, FX, credit, prediction markets, Fed posture.")
    async def brief(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            fred_data = await fred.fetch()
            kalshi_data = await kalshi.fetch()
            embed = await compose_brief(fred_data, kalshi_data)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"Rita encountered an error pulling the brief: `{e}`")

async def setup(bot):
    await bot.add_cog(Brief(bot))
