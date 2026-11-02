# cogs/moderazione.py
import discord
from discord import app_commands
from discord.ext import commands

class Moderazione(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Espelle un utente dal server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, utente: discord.Member, motivo: str = "Nessun motivo fornito"):
        await utente.kick(reason=motivo)
        await interaction.response.send_message(f"{utente.mention} è stato espulso. Motivo: {motivo}")

async def setup(bot):
    await bot.add_cog(Moderazione(bot))