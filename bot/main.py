import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from alerts.watcher import start_watcher

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    await bot.load_extension("bot.commands.brief")
    await bot.load_extension("bot.commands.regime")
    await bot.load_extension("bot.commands.analyze")
    await bot.load_extension("bot.commands.watch")
    await bot.tree.sync()
    start_watcher(bot)
    print(f"Rita is online — logged in as {bot.user}")

bot.run(os.environ["DISCORD_TOKEN"])
