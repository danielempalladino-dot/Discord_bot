import asyncio

async def prepara_caffe():
    print("1. Avvio la macchina del caffè...")
    # asyncio.sleep simula un'operazione di rete o I/O (NON bloccante)
    await asyncio.sleep(3)
    print("3. Caffè pronto! ☕")

async def rispondi_messaggio():
    print("2. Sto rispondendo a un utente su Discord...")

async def main():
    # Eseguiamo i due compiti
    # create_task avvia il caffè in background nell'Event Loop
    task_caffe = asyncio.create_task(prepara_caffe())

    # Eseguiamo l'altra funzione mentre il caffè si prepara
    await rispondi_messaggio()

    # Attendiamo che il caffè sia completato prima di chiudere
    await task_caffe

asyncio.run(main())
