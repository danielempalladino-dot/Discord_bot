import json
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

CONFIG_PATH = Path(__file__).resolve().parent / "config" / "config.json"
if not CONFIG_PATH.is_file():
    raise FileNotFoundError(
        "File config/config.json mancante. Copia config/config.example.json "
        "in config/config.json e inserisci i tuoi dati."
    )

with CONFIG_PATH.open("r", encoding="utf-8") as file:
    config = json.load(file)

credenziali = config["credenziali"]
token = credenziali["token"]
CANALE_ID = credenziali["CANALE_GENERALE"]

# Gli intent indicano quali eventi il bot può ricevere da Discord.
intents = discord.Intents.default()
intents.message_content = True


class IlMioBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # setup_hook attende il caricamento del Cog prima di sincronizzare i comandi.
        await self.load_extension("cogs.moderazione")
        synced = await self.tree.sync()
        print(f"Sincronizzati {len(synced)} comandi Slash.")

    numero_di_comandi = 0


bot = IlMioBot()


@bot.event
async def on_ready():
    print(f"Bot dislocato con successo come {bot.user} (ID: {bot.user.id})")
    channel = bot.get_channel(CANALE_ID)
    if channel:
        await channel.send("bot connessi")
    else:
        print("Impossibile trovare il canale! Controlla l'ID o i permessi del bot.")


@bot.tree.command(name="ping", description="Risponde con Pong e mostra la latenza del bot")
async def ping(interaction: discord.Interaction):
    latency_ms = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! 🏓 Latenza: {latency_ms}ms")


@bot.tree.command(name="saluta", description="Invia un saluto personalizzato")
@app_commands.describe(utente="L'utente da salutare", messaggio="Messaggio opzionale")
async def saluta(interaction: discord.Interaction, utente: discord.Member, messaggio: str = "Benvenuto!"):
    await interaction.response.send_message(f"Ciao {utente.mention}! {messaggio}")


@bot.event
async def on_message(message: discord.Message):
    bot.numero_di_comandi += 1
    print(f"[{bot.numero_di_comandi}] Messaggio ricevuto: {message.content} da {message.author} nel canale {message.channel} (ID: {message.channel.id})")
    if message.author == bot.user:
        return

    if message.content.lower() == "ciao bot":
        await message.channel.send(f"Ciao {message.author.mention}!")

    if (bot.numero_di_comandi % 10) == 0:
        await message.channel.send(f"decimo comando ricevuto! Totale comandi: {bot.numero_di_comandi}")

    await bot.process_commands(message)


bot.run(token)