import socket
import threading
import json
from itertools import permutations
from card import *
from os import path
import animation

# DA OGGETTO A STRINGA
def stringifyObject(obj):
    try:
        stringa_json = json.dumps(obj)
        return stringa_json
    except (TypeError, ValueError) as e:
        print(f"Errore nella conversione dell'oggetto in stringa: {e}")
        return None

def parseObject(stringa):
    try:
        obj = json.loads(stringa)
        return obj
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Errore nella conversione della stringa in oggetto: {e}")
        return None
    
def riceviJson(qta = 1024):
    return parseObject(client.recv(qta).decode("utf-8"))

def inviaJSON(messaggio):
    client.send(stringifyObject(messaggio).encode())

def getNumber(card):
    return int(card[1:])

def getValues(arr):
    return [c.value for c in arr]

def getIndexFromValues(table, cards):
    return [index for index, c in enumerate(table) if c.value in cards]

def chiusura(root):
    if waitMoveThread.is_alive():
        #HO ANCORA IL THREAD CONNESSO AL SERVER
        #SE HAI PROBLEMI E PER FACILITARTI LA VITA DEVI CAMBIARE QUESTA IF
        #PUOI VERIFICARE SE IL CLIENT E' ANCORA CONNESSO AL SERVER
        inviaJSON({"request": "closingClient"})
        print("SONO in una partita e chiudo il client")
        print('"request": "closingClient"')
    else:
        #NON SONO ANCORA IN UNA PARTITA
        try:
            inviaJSON({"request": "stopWaiting"})
            print("non sono in una partita e chiudo il client")
        except:
            pass
        print('"request": "stopWaiting"')

    root.destroy()

def home(root):
    root.destroy()
    from forms.login import Login
    Login(root.master)


def getHost():
    global Indirizzo
    global Host
    ip = Host
    if(path.exists('ip.txt')):
        data = open('ip.txt', 'r')
        ip = data.read()
        data.close()
    return ip

Host = socket.gethostbyname(socket.gethostname())
Porta = 9999
Indirizzo = (Host, Porta)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lock = threading.Lock()

waitMoveThread = threading.Thread()

turn = False
startingTurn = False
alreadyConnected = False
#variabili per i punteggi
pickedCards = []
enemyPickedCards = []
points = {
    "Scope1": 0,
    "Scope2": 0,
    "Sette bello": "No",
    "Denari1": 0,
    "Denari2": 0
}
lastPlay = False
lastTake = False


def waitForGame(nickname, ip, resolver, error):
    global Host
    global Indirizzo
    if(Host != ip):
        if(ip != ""):
            Host = ip
            Indirizzo = (Host, Porta)
        data = open('ip.txt', 'w')
        data.write(Host)
        data.close()

    threading.Thread(target=connect, args=(nickname, resolver, error)).start()

def connect(nickname, resolver, error):
    global alreadyConnected
    global client

    if not alreadyConnected:
        alreadyConnected = True
        canIPlay = True
        try:
            # Prova a connettersi al server
            client.connect(Indirizzo)
        except OSError as e:
            canIPlay = False
            error(f'Mi spiace ma è impossibile collegarsi al Server!!')
            # Gestisce errori di connessione
        
        if canIPlay:
            #il server non è avviato
            inviaJSON({"nome": nickname})
            resolver(riceviJson())
    else:
        #voglio rigiocare
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(Indirizzo)
        inviaJSON({"nome": nickname})
        print("HO MANDATO CON SUCCESSO")
        resolver(riceviJson())

def waitMove(game):
    global turn
    global startingTurn
    global lastTake
    endThread = False
    carteRimanenti = 30

    inviaJSON({"request": "startGameOk"})

    while not endThread:

        data = riceviJson()
        print(f"[{game.user}]: data = {data}")

        if data != None:
            if data["request"] == "move":
                with lock:
                    turn = True
                
                #renderizzo turno
                game.setStatus()
                
                # carte prese dall' avversario
                tableCardsPicked = getIndexFromValues(game.table.cards, data["tableCardsPicked"])
                
                game.space2.cards[0].value = data["cardPlayed"]
                removedCard = game.space2.cards.pop(0)
                game.space2.calculate()
                
                if len(tableCardsPicked) == 0:
                    game.table.addCard(removedCard) 
                else:
                    lastTake = False

                    game.execMove(
                        removedCard, # carta giocata dall'avversario
                        tableCardsPicked,
                        #tableCardsPicked carte prese dall'avversario
                        2
                    )
                    enemyPickedCards.append(data["cardPlayed"])

                    for c in game.getCardsFromIndices(tableCardsPicked):
                        enemyPickedCards.append(c.value)
                      
            elif data["request"] == "newCards":
                stopAnimations.clear()

                carteRimanenti -= 6

                game.lbldeck.configure(text = str(carteRimanenti))

                if len(stop) != 0:
                    stopAnimations.wait()

                game.BuildDrawCard(data["cards"])

                with lock:
                    turn = startingTurn

                #renderizzo mossa
                game.setStatus()
            elif data["request"] == "viewLastPlay":
                lastPlay = True
                MessageBox(game.frame,
                        "Ultima giocata!!!",
                    DARK_GREEN, default_font_subtitle()).show(2)
                
            elif data["request"] == "calculatePoints":
                endThread = True
                stopAnimations.clear()
                stopAnimations.wait()
                #aspetto tutte le animazioni
                game.setStatus(True)
                carteRimanenti = 0

                game.lbldeck.configure(text = str(carteRimanenti))

                if len(game.table.cards) != 0:
                    if lastTake:
                        #prendo le carte rimanenti
                        print(f"[{game.user}]: devo prendere tutte le carte rimanenti")
                        for c in game.table.cards:
                            pickedCards.append(c.value)
                    else:
                        #prende l'avversario le carte rimanenti
                        for c in game.table.cards:
                            enemyPickedCards.append(c.value)

                    game.table.rmCards = getIndexFromValues(game.table.cards, 
                                                            getValues(game.table.cards))
                    
                    game.renderMove(None, 1 if lastTake else 2)

                turn = False #rendo non cliccabili le carte
                from forms.points import PointTable
                
                print(f"[{game.user}]: points = {points}")
                print(f"[{game.user}]: pickedCard = {pickedCards}")
                

                tabella = PointTable(game.frame, pickedCards, enemyPickedCards, points,
                                     [game.user, game.user2], lambda: home(game.frame))
                
                tabella.place(relx=0.5, rely=0.5, anchor="center")



            elif data["request"] == "endGameError":
                turn = False #rendo le carte NON cliccabili
                endThread = True

                inviaJSON({"request": "confirmedForceQuit"})

                msgBox = MessageBox(
                    root=game.frame, 
                    msg="L'avversario è uscito dal gioco",
                    color=RED, 
                    btn = {
                        "text": "Torna alla home",
                        "fg_color": RED,
                        "text_color": WHITE,
                        "command": lambda: home(game.frame)
                    })

                msgBox.show()
                #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
        else:
            endThread = True

def sendMove(card, move):
    global turn

    move = getValues(move)

    inviaJSON({
        "request": "move",
        "tableCardsPicked" : move,
        "cardPlayed": card
        })

    if len(move) != 0:
        pickedCards.append(card)

        for c in move:
            pickedCards.append(c)

def getMoves(card, table):
    possibilities = []
    numCarta = getNumber(card)
    somma = 0
    tableCards = getValues(table)

    for i in range(len(table)):
        n = getNumber(table[i].value)

        if n == numCarta:
            #possibilities.append([c])
            possibilities.append([i])

        somma += n

    if len(possibilities) == 0:
        if somma == numCarta:
            #prendo tutte le carte del tavolo
            possibilities.append(list(range(len(table))))
        else:
            #NON HO CARTE DELLO STESSO VALORE SUL TAVOLO E CONTINUO A CERCARE COMBINAZIONI

            #tableCard = copia del table ma solo con i .value così
            for i in range(2, len(table)):
                #non si deve copiare l'intero oggetto grafico
                allPermutation = [list(perm) for perm in permutations(tableCards, i)]
                #ritorno una lista di permutazioni di tutte le permutazioni possibili
                for perm in allPermutation:
                    somma = 0
                    for singleCardperm in perm:
                        somma += getNumber(singleCardperm)

                    if somma == numCarta:
                        perm = sorted(perm)
                        if perm not in possibilities:
                            possibilities.append(perm)

            for i in range(len(possibilities)):
                #possibilities[i] = [c for c in table if c.value in possibilities[i]]
                possibilities[i] = getIndexFromValues(table, possibilities[i])
                
    return possibilities