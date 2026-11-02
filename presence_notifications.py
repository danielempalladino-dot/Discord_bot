import discord
import json
from pathlib import Path

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
CANALE_ID = credenziali["ID_CANALE_ATTIVITA"]

# Configurazione Intents
intents = discord.Intents.default()
# L'intent message_content serve per inviare il messaggio in chat
intents.message_content = True
# L'intent presences serve per "vedere" lo stato e le attività degli utenti
intents.presences = True
# L'intent members serve per assicurarsi che il bot conosca tutti i membri del server
intents.members = True

# Inizializzazione del client
client = discord.Client(intents=intents)

# Inserisci qui l'ID del canale testuale dove vuoi che il bot scriva il messaggio
# Puoi ottenere l'ID cliccando col tasto destro sul canale in Discord e selezionando "Copia ID"

@client.event
async def on_ready():
    print(f'Bot connesso come {client.user}')

@client.event
async def on_presence_update(before, after):
    # Controlliamo se l'attività è cambiata
    if before.activity != after.activity:
        # Verifichiamo se l'utente ha iniziato a giocare a qualcosa di nuovo
        # (after.activity non è None e before.activity era None oppure era un gioco diverso)
        if after.activity is not None and getattr(after.activity, 'type', None) == discord.ActivityType.playing:

            # Per evitare spam se l'utente cambia stato ma era già in gioco
            if before.activity is None or getattr(before.activity, 'name', None) != after.activity.name:

                # Cerchiamo il canale specifico usando l'ID
                canale = client.get_channel(CANALE_ID)

                if canale:
                    # Inviamo il messaggio in chat
                    # after.display_name prende il nickname dell'utente sul server
                    # after.activity.name prende il nome del gioco (es. "Fortnite")
                    await canale.send(f"🎮 {after.display_name} ha aperto **{after.activity.name}**!")

# Avvio del bot
client.run(token)
