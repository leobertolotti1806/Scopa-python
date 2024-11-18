import json
import socket
import threading
import random

# DA OGGETTO A STRINGA
def stringifyObject(obj):
    try:
        stringa_json = json.dumps(obj)
        return stringa_json
    except (TypeError, ValueError) as e:
        print(f"Errore nella conversione dell'oggetto in stringa: {e}")
        return None

# DA STRINGA A OGGETTO
def parseObject(stringa):
    try:
        obj = json.loads(stringa)
        return obj
    except  (json.JSONDecodeError, TypeError) as e:
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
    if client:
        return parseObject(client.recv(qta).decode("utf-8"))
    else:
        return {"request": ""}


def inviaJSON(messaggio, client):
    messaggio = stringifyObject(messaggio).encode()

    if isinstance(client, list):
        # Invia msg a tutti i client
        for c in client:
            c.send(messaggio)
    else:
        # Invia al SINGOLO client
        client.send(messaggio)

def checkClosureClient(client):
    obj = {}
    endThread = False

    while not endThread:
        obj = riceviJSON(client["client"])

        if obj["request"] == "closingClient" or obj["request"] == "stopWaiting" or obj["request"] == "move":
            endThread = True

    if obj["request"] == "stopWaiting":
        print(f"chiudo il client [{client["nome"]}] e rimuovo la connessione al server")
        with lock:
            clients.remove(client)
            client["client"].close()


def matchClient(client, addr):
    nome = riceviJSON(client)['nome']
    print("Si è connesso " + nome)

    clientObj = {"client": client, "addr": addr, "nome": nome}
    #THREAD CHE CONTROLLA LA CHIUSURA DEI CLIENT E CORREGGE IL FUNZIONAMENTO

    threading.Thread(target=checkClosureClient, args = (clientObj,)).start()

    with lock:
        clients.append(clientObj)

    if len(clients) % 2 == 0:
        if len(clients) > 1:
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
        "cards": pesca(mazzo, 3),
        "user2": client2['nome']
        }, c1)

    inviaJSON({
        "request": "startGame",
        "startingTurn": False,
        "table": tavolo,
        "cards": pesca(mazzo, 3),
        "user2": client1['nome']
        }, c2)

    t1 = threading.Thread(target=mosse, args=(c1, client2, nMosse, mazzo, score1, client1['nome']))
    t2 = threading.Thread(target=mosse, args=(c2, client1, nMosse, mazzo, score2, client2['nome']))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    if score1 and score2:
        #ho dei punteggi senza aver avuto errori / chiusure
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

        clients.remove(client1)
        clients.remove(client2)

    print("FINISCO THREAD PARTITA")

def pesca(mazzo, nCarte):
    carteScelte = random.sample(mazzo, nCarte)

    for carta in carteScelte:
        mazzo.remove(carta)

    return carteScelte

def mosse(client, cAvversario, nMosse, mazzo, score, nome):
    err = False

    clientAvversario = cAvversario["client"]

    while not err and nMosse[0] < 30:
        # Riceve la mossa dal giocatore attuale
        print("avvio mossa")
        mossa = riceviJSON(client)
        print(f"Mossa ricevuta: {mossa}")

        if mossa["request"] != "closingClient":
            # Invia la mossa all'altro giocatore
            if len(mossa["tableCardsPicked"]) > 0:
                inviaJSON({
                    "request": "move",
                    "cardPlayed": mossa["cards"], #CARD GIOCATA
                    "tableCardsPicked" : mossa["tableCardsPicked"], #CARDS O CARD PRESA DAL TAVOLO,
                    "msg": mossa["msg"] #variabile per far vedere lato client se l'avversario ha fatto scopa/settebello
                    }, clientAvversario)

            with lock:
                nMosse[0] += 1

            # Ogni 6 mosse termina il round
            if nMosse % 6 == 0:
                inviaJSON({
                    "request": "newCards",
                    "cards": pesca(mazzo, 3),
                    "msg": mossa["msg"] #variabile per far vedere lato client se l'avversario ha fatto scopa/settebello
                    }, client)
        else:
            print(f"Il client [{nome}] ha chiuso la finestra")
            err = True
            inviaJSON({"request": "endGameError"}, clientAvversario)
            with lock:
                clientAvversario.close()
                clients.remove(cAvversario)
                

    if not err:
        inviaJSON({"request": "calculatePoints"}, client)
        score = riceviJSON(client)

avviaServer()