import discord
import asyncio
import fitz
from discord import app_commands
from discord.ext import commands
from intelligence.analyst import analyze, clear_session

SESSIONS: dict[str, asyncio.TimerHandle] = {}
SESSION_TIMEOUT = 1800

def _session_key(user_id: int, channel_id: int) -> str:
    return f"{user_id}:{channel_id}"

class Analyze(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="analyze", description="Q&A on a macro document. Paste text or attach a .txt/.pdf file.")
    @app_commands.describe(
        question="Your question about the document",
        text="Paste document text directly (optional if attaching a file)",
    )
    async def analyze_cmd(
        self,
        interaction: discord.Interaction,
        question: str,
        text: str = None,
    ):
        await interaction.response.defer(thinking=True)

        document = text or ""

        if not document and interaction.message and interaction.message.attachments:
            attachment = interaction.message.attachments[0]
            raw = await attachment.read()
            if attachment.filename.endswith(".pdf"):
                doc = fitz.open(stream=raw, filetype="pdf")
                document = "\n".join(page.get_text() for page in doc)
            else:
                document = raw.decode("utf-8", errors="ignore")

        key = _session_key(interaction.user.id, interaction.channel_id)

        if key in SESSIONS:
            SESSIONS[key].cancel()

        loop = asyncio.get_event_loop()
        SESSIONS[key] = loop.call_later(
            SESSION_TIMEOUT,
            lambda: clear_session(interaction.user.id, interaction.channel_id),
        )

        reply = await analyze(interaction.user.id, interaction.channel_id, document, question)
        await interaction.followup.send(reply)

async def setup(bot):
    await bot.add_cog(Analyze(bot))
