import discord

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
token = 'MTU1ODE3Njc5NDk4MzUzMDYyNw.GfTXZs.LTa-RNJxckZFAc2d0LYkdxX7bUd3SOpIzOX0l0'
#id del canale dove inviare il messaggio di notifica quando un utente cambia gioco
#ATTENZIONE: l'id del canale corrisponde a un int, per ottenere l'indirizzo del canale bisogna utilizzare client.get_cannel()
CANALE_GENERALE = 1558169601576013877
ID_CANALE_ATTIVITA = 1559856685072261193

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


#invocazione del client con gli intents definiti
client = MyClient(intents=intents)

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

