import discord
import json
from pathlib import Path

# Directory principale del progetto
BASE_DIR = Path(__file__).resolve().parent
# Percorso del file di configurazione
CONFIG_PATH = BASE_DIR / "config" / "config.json"
# Lettura configurazione
with CONFIG_PATH.open("r", encoding="utf-8") as file:
    config = json.load(file)
# Configurazione degli Intents
intents = discord.Intents.default()
#L'intent message_content serve per inviare il messaggio in chat
intents.message_content = True
# L'intent presences serve per "vedere" lo stato e le attività degli utenti
intents.presences = True
# L'intent members serve per assicurarsi che il bot conosca tutti i membri del server
intents.members = True

#Variabili globali

#token per accedere al bot, UNIVOCO
token = config["credenziali"]["token"]
#id del canale dove inviare il messaggio di notifica quando un utente cambia gioco
#ATTENZIONE: l'id del canale corrisponde a un int, per ottenere l'indirizzo del canale bisogna utilizzare client.get_cannel()
CANALE_GENERALE = config["credenziali"]["CANALE_GENERALE"]
ID_CANALE_ATTIVITA = config["credenziali"]["ID_CANALE_ATTIVITA"]

#definizione della classe MyClient che estende discord.Client
class MyClient(discord.Client):
    #definizione del metodo on_ready, appena il client è pronto esegue l'azione
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        canale = self.get_channel(CANALE_GENERALE)
        if canale:
            await canale.send("Bot connesso")
        else:
            print("Impossibile trovare il canale! Controlla l'ID o i permessi del bot.")

        #lista di tutti gli utenti conosciuti dal bot
        #per accedere a guild.members, devo prima assegnatre la variabile guild, che contiene u riferimento a un server discord
        #attraverso self.guilds ottengo la lista dei server a cui il bot è connesso. iterando lo scorrimento della lista
        #posso associare alla variabile guild , puntatore a un server discord, gli indirizzi dei server a cui il bot è connesso e recuperare le informazioni desiderate.
        for guild in self.guilds:
            print(f'Guild: {guild.name} (ID: {guild.id})')
            utenti = guild.members
            for member in guild.members:
                print('------------------------------')
                print(f'Utente: {member.name}')
                print(f'ID: {member.id}')
                print(f'Bot: {member.bot},')



#invocazione del client con gli intents definiti
client = MyClient(intents=intents, status = discord.Status.online, activity = discord.Game(name = "still developping"))
utenti = client.users
print(utenti)
#Decoratore per gli eventi al'interno del client
#client.event ricerca un evento che deve essere una co\routine (funzione asincrona) e lo registra come listener per quell'evento
#on ready è chiamato quando il client è pronto e connesso a Discord


@client.event
async def on_message(message):
        print(f'{message.author}: "{message.content}" --> **{message.channel}**')
        # don't respond to ourselves
        if message.author == client.user:
            return
        if message.content == ('juve'):
            await message.channel.send('Forza Juve! ⚪⚫')
        if message.content.strip().casefold() == "played game rn":
            guild = message.guild

            # Il messaggio potrebbe arrivare in DM, dove non esiste una guild.
            if guild is None:
                return

            giochi = {}
            for membro in guild.members:
                for attivita in membro.activities:
                    if attivita.type == discord.ActivityType.playing:
                        giochi.setdefault(attivita.name, []).append(membro.display_name)

            if giochi:
                elenco = "\n".join(
                    f"• {gioco}: {', '.join(giocatori)}"
                    for gioco, giocatori in giochi.items()
                )
                await message.channel.send(f"Giochi giocati ora nel server:\n{elenco}")
            else:
                await message.channel.send("Al momento non vedo nessun gioco in corso.")

@client.event
# onPresenceUpdate is called when a Member updates their presence --> activity and status
async def on_presence_update(before, after):
    #recupero il gioco precedente
    #utilizzo next --> next() restituisce il primo elemento di un iteratore che soddisfa una condizione, in questo caso il nome del gioco precedente
    #SINTASSI DI NEXT
    #next((expression for item in iterable if condition), default)
    #(cosa deve restituire ciclo di ricerca condizione da soddisfare), default se non trova nulla
    gioco_precedente = next(
        (
            activity.name
            for activity in before.activities
            if getattr(activity, 'type', None) == discord.ActivityType.playing
        ),
        None
    )
    gioco_attuale = next(
        (
            activity.name
            for activity in after.activities
            if getattr(activity, 'type', None) == discord.ActivityType.playing
        ),
        None
    )
    #verifico che sia effettivamente cambiato il gioco
    if(gioco_attuale is None or gioco_precedente == gioco_attuale):
        return
    #invio il messaggio nel canale specificato
    #per inviarlo prima devo recuperare il canale con l'ID specificato
    canale = client.get_channel(ID_CANALE_ATTIVITA)
    if canale:
        await canale.send(f"🎮 {after.display_name} ha aperto **{gioco_attuale}**!")

#esecuzione del client con il token specificato
client.run(token)
