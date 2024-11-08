import json
import socket
import threading
import random

# DA OGGETTO A STRINGA
def stringifyObject(obj):
    try:
        # Converte l'oggetto in una stringa JSON
        stringa_json = json.dumps(obj)
        return stringa_json
    except (TypeError, ValueError) as e:
        print(f"Errore nella conversione dell'oggetto in stringa: {e}")
        return None

# DA STRINGA A OGGETTO
def parseObject(stringa):
    try:
        # Converte la stringa JSON in un oggetto Python
        obj = json.loads(stringa)
        return obj
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Errore nella conversione della stringa in oggetto: {e}")
        return None

Host = socket.gethostbyname(socket.gethostname())
Porta = 9999
Indirizzo = (Host, Porta)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(Indirizzo)

lock = threading.Lock()

# Lista dei CLIENT
clients = []
matches = []

mazzoOrdinato = [
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10",
    "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10" 
]

def riceviJSON(client, qta = 1024):
    return parseObject(client.recv(qta).decode("utf-8"))

def inviaJSON(messaggio, client):
    messaggio = stringifyObject(messaggio).encode()

    if isinstance(client, list):
        # Invia msg a tutti i client
        for c in client:
            c.send(messaggio)
    else:
        # Invia al SINGOLO client
        client.send(messaggio)

def matchClient(client, addr):
    nome = riceviJSON(client)['nome']
    print("Si è connesso " + nome)

    with lock:
        clients.append({"client": client, "addr": addr, "nome": nome})

    if (len(clients) > 1 and len(clients) % 2 == 0):
            #si collegano 2 giocatori
            # Avvio un Nuovo THREAD per la gestione della partita
            
            threadPartita = threading.Thread(target=partita,
                            args = (clients[-1], clients[-2], 
                            random.sample(mazzoOrdinato, len(mazzoOrdinato))))

            threadPartita.start()

    print(f"Connessioni Attive " + str(len(clients)))

    


# Avvio il SERVER
def avviaServer():
    print("[SERVER] avviato su " , Indirizzo)
    print("\n")

    # Imposto il SERVER in ascolto
    server.listen()    
    while True:
        #accetto la connessione
        client, addr = server.accept()

        threading.Thread(target=matchClient, args = (client, addr)).start()

        
        
# Metodo per Gestire i Messaggi in Arrivo dal CLIENT
def partita(client1, client2, mazzo):

    print(f"Partita avviata tra [{client1['nome']}] - [{client2['nome']}]")

    c1 = client1['client']
    c2 = client2['client']
    tavolo = pesca(mazzo, 4)
    nMosse = [0]
    score1 = {}
    score2 = {}

    inviaJSON({
        "request": "startGame",
        "startingTurn": True,
        "table": tavolo,
        "cards": pesca(mazzo, 3)
        }, c1)

    inviaJSON({
        "request": "startGame",
        "startingTurn": False,
        "table": tavolo,
        "cards": pesca(mazzo, 3)
        }, c2)

    t1 = threading.Thread(target=mosse, args=(c1, c2, nMosse, mazzo, score1))
    t2 = threading.Thread(target=mosse, args=(c2, c1, nMosse, mazzo, score2))

    t1.start()
    t2.start()

    # Attendi che i thread completino
    t1.join()
    t2.join()

    if score1["win"]:
        vincitore = "Giocatore 1 ha vinto!"
    elif score2["win"]:
        vincitore = "Giocatore 2 ha vinto!"
    else:
        vincitore = "Pareggio!"

    inviaJSON({
        "request": "endGame", 
        "msg": vincitore
        }, [c1, c2])

    c1.close()
    c2.close()

def pesca(mazzo, nCarte):
    carteScelte = random.sample(mazzo, nCarte)

    for carta in carteScelte:
        mazzo.remove(carta)

    return carteScelte

def mosse(client, clientAvversario, nMosse, mazzo, score):
    
    while nMosse[0] < 30:
        # Riceve la mossa dal giocatore attuale
        mossa = riceviJSON(client)
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        #FAI TRY PARSE IN RICEVI JSON COSI SE CHIUDI IL CLIENT NON SI PIANTA
        print(f"Mossa ricevuta: {mossa}")

        # Invia la mossa all'altro giocatore
        inviaJSON({
            "request": "enemyMove",
            "move": mossa["carta"]
            }, clientAvversario)

        with lock:
            nMosse[0] += 1

            # Ogni 6 mosse termina il round
            if nMosse % 6 == 0:
                inviaJSON({
                    "request": "newCards",
                    "carte": pesca(mazzo, 3)
                    }, client)

    inviaJSON({"request": "calculatePoints"}, client)

    score = riceviJSON(client)

avviaServer()