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

# Lista dei CLIENT con attributi necessari per controlli
clients = []
checkClientsThreadList = []

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

def checkClient(client):
    obj = {}
    endThread = False

    while not endThread:
        obj = riceviJSON(client["client"])

        if obj["request"] == "startGameOk" or obj["request"] == "stopWaiting":
            endThread = True

    if obj["request"] == "stopWaiting":
        print(f"[checkClient di {client['nome']}]: Chiudo il client [{client['nome']}] e rimuovo la connessione al server")

        client["client"].close()

        with lock:
            clients.remove(client)
            checkClientsThreadList.remove(threading.current_thread())

    
    print(f"[checkClient di {client['nome']}]: Completato!!!")


def matchClient(client, addr):
    nome = riceviJSON(client)["nome"]
    print("[matchClient]: Si è connesso " + nome)

    clientObj = {
        "client": client,
        "addr": addr,
        "nome": nome
        }

    #THREAD CHE CONTROLLA LA CHIUSURA DEI CLIENT E CORREGGE IL FUNZIONAMENTO
    checkClientThread = threading.Thread(target=checkClient, args = (clientObj,))
    checkClientThread.start()

    with lock:
        checkClientsThreadList.append(checkClientThread)
        clients.append(clientObj)
    
    if len(clients) % 2 == 0 and len(clients) > 1:
        #si collegano 2 giocatori
        # Avvio un Nuovo THREAD per la gestione della partita

        threading.Thread(target=partita, args = (clients[-1], clients[-2],
            checkClientsThreadList[-1], checkClientsThreadList[-2],
            random.sample(mazzoOrdinato, len(mazzoOrdinato)))).start()

    print(f"[matchClient]: Connessioni Attive {len(clients)}")


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
def partita(client1, client2, check1, check2, mazzo):
    game = {
        "nMosse": 0,
        "err": False,
        "mazzo": mazzo,
        "lock": threading.Lock()
    }

    tavolo = pesca(game, 4)

    inviaJSON({
        "request": "startGame",
        "startingTurn": True,
        "table": tavolo,
        "cards": pesca(game, 3),
        "user2": client2["nome"]
        }, client1["client"])

    inviaJSON({
        "request": "startGame",
        "startingTurn": False,
        "table": tavolo,
        "cards": pesca(game, 3),
        "user2": client1["nome"]
        }, client2["client"])

    #Aspetto che i due client mi confermino di avviare la partita
    check1.join()
    check2.join()

    with lock:
        checkClientsThreadList.remove(check1)
        checkClientsThreadList.remove(check2)

    print(f"[partita di {client1['nome']} - {client2['nome']}]: Avviata")
    
    t2 = threading.Thread()

    t1 = threading.Thread(target=mosse, args=(client1, client2, game, t2))
    t2 = threading.Thread(target=mosse, args=(client2, client1, game, t1))

    t1.name = client1["nome"]
    t2.name = client2["nome"]

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    if not game["err"]:
        inviaJSON({"request": "calculatePoints"}, [client1["client"], client2["client"]])

    client1["client"].close()
    client2["client"].close()

    with lock:
        clients.remove(client1)
        clients.remove(client2)

    print(f"[partita di {client1['nome']} - {client2['nome']}]: Client rimossi con successo e termino la partita")

def pesca(game, nCarte):
    carteScelte = random.sample(game["mazzo"], nCarte)

    with game["lock"]:
        for carta in carteScelte:
            game["mazzo"].remove(carta)

    return carteScelte

def mosse(client, cAvversario, game, threadAvversario):
    while not game["err"] and game["nMosse"] < 29:
        # Riceve la mossa dal giocatore attuale
        mossa = riceviJSON(client["client"])
        print(f"[{client['nome']}]: Mossa ricevuta: {mossa}")
        print(f"[{client['nome']}]: nMosse: {game['nMosse']}")

        if mossa["request"] == "move":
            # Invia la mossa all"altro giocatore

            if game["nMosse"] == 28:
                inviaJSON({"request": "viewLastPlay"}, 
                          [client["client"], cAvversario["client"]])
                
            inviaJSON(mossa, cAvversario["client"])

            with game["lock"]:
                game["nMosse"] += 1

            # Ogni 6 mosse termina il round
            if game["nMosse"] % 6 == 0 and game["nMosse"] != 30:
                for cli in [client["client"], cAvversario["client"]]:
                    inviaJSON({
                        "request": "newCards",
                        "cards": pesca(game, 3),
                    }, cli)

        elif mossa["request"] == "closingClient":
            with game["lock"]:
                game["err"] = True
            
            print(f"[{client['nome']}]: ho chiuso la finestra")

            inviaJSON({"request": "endGameError"}, cAvversario["client"])

        elif mossa["request"] == "confirmedForceQuit":
            with game["lock"]:
                game["err"] = True

            print(f"[{client['nome']}]: Il client avversario [{cAvversario['nome']}] ha terminato la partita e confermo l'uscita")

    if not game["err"]:
        print(f"[{client['nome']}]: threadAvversario.is_alive(): {threadAvversario.is_alive()}")
        
        if threadAvversario.is_alive():
            threadAvversario.join()

    print(f"[{client['nome']}]: FINISCO PARTITA")
avviaServer()