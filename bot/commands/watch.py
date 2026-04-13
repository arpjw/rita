import discord
from discord import app_commands
from discord.ext import commands
from alerts.watcher import add_alert, remove_alert, list_alerts, SUPPORTED_VARIABLES

class Watch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="watch", description="Subscribe to macro variable threshold alerts delivered via DM.")
    @app_commands.describe(
        variable=f"Variable to watch: {', '.join(SUPPORTED_VARIABLES)}",
        direction="Trigger when value goes above or below threshold",
        threshold="Threshold value to trigger the alert",
    )
    @app_commands.choices(direction=[
        app_commands.Choice(name="above", value="above"),
        app_commands.Choice(name="below", value="below"),
    ])
    async def watch(self, interaction: discord.Interaction, variable: str, direction: str, threshold: float):
        result = add_alert(interaction.user.id, variable, direction, threshold)
        if isinstance(result, str):
            await interaction.response.send_message(f"⚠️ {result}", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"✅ Alert set — Rita will DM you when `{variable}` goes **{direction}** `{threshold}`.\nAlert ID: `{result.id}`",
                ephemeral=True,
            )

    @app_commands.command(name="watchlist", description="View your active Rita alerts.")
    async def watchlist(self, interaction: discord.Interaction):
        active = list_alerts(interaction.user.id)
        if not active:
            await interaction.response.send_message("No active alerts.", ephemeral=True)
            return
        lines = "\n".join(f"`{a.id}` — {a.variable} {a.direction} {a.threshold}" for a in active)
        await interaction.response.send_message(f"**Your active alerts:**\n{lines}", ephemeral=True)

    @app_commands.command(name="watchcancel", description="Cancel an active Rita alert by ID.")
    @app_commands.describe(alert_id="Alert ID from /watchlist")
    async def watchcancel(self, interaction: discord.Interaction, alert_id: str):
        removed = remove_alert(interaction.user.id, alert_id)
        if removed:
            await interaction.response.send_message(f"✅ Alert `{alert_id}` cancelled.", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ No alert found with ID `{alert_id}`.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Watch(bot))
