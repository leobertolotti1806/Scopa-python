import socket
import threading
import json
from itertools import permutations
from card import *

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

Host = "192.168.178.24"
Host = socket.gethostbyname(socket.gethostname())
Porta = 9999
Indirizzo = (Host, Porta)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

waitMoveThread = threading.Thread()
data = {}
turn = False
startingTurn = False
#variabili per i punteggi
pickedCards = []
nScope = 0
setteBello = False
nDenari = 0
puntiTotali = 0
lastPlay = False
nScopeAvversario = 0

def waitForGame(nickname, resolver, error):
    threading.Thread(target=connect, args=(nickname, resolver, error)).start()

def connect(nickname, resolver, error):
    canIPlay = True
    try:
        # Prova a connettersi al server
        client.connect(Indirizzo)
    except:
        # Gestisce errori di connessione
        canIPlay = False
        error(f'Mi spiace ma è impossibile collegarsi al Server!!')
    
    if canIPlay:
        #il server non è avviato
        inviaJSON({"nome": nickname})
        resolver(riceviJson())

lock = threading.Lock()

def calculatePoints():
    global nDenari
    global puntiTotali
    card = "pari"
    denari = "pari"

    #controllo numero carte
    if len(pickedCards) > 20:
        puntiTotali += 1
        carte = True
    elif len(pickedCards) < 20:
        carte = False

    if nDenari > 5:
        puntiTotali += 1
        denari = True
    elif nDenari < 5:
        denari = False

    puntiTotali += nScope
    #FAI CONTROLLO VITTORIA
    #FAI CONTROLLO VITTORIA
    #FAI CONTROLLO VITTORIA
    #FAI CONTROLLO VITTORIA


def waitMove(game):
    global data
    global nScopeAvversario
    global turn
    global startingTurn
    global setteBello
    endThread = False

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
                
                tableCardsPicked = [c for c in game.table.cards if c.value in data["tableCardsPicked"]] # carte prese dall' avversario

                if len(game.table.cards) - len(tableCardsPicked):
                    nScopeAvversario += 1

                game.space2.cards[0].value = data["cardPlayed"]
                removedCard = game.space2.cards.pop(0)
                game.space2.calculate()
                
                if len(tableCardsPicked) == 0:
                    game.table.addCard(removedCard) 
                else:
                    game.execMove(
                        removedCard, # carta giocata dall'avversario
                        tableCardsPicked
                    )

                if data["cardPlayed"] == "D7" or "D7" in data["tableCardsPicked"]:
                    setteBello = True
                      
            elif data["request"] == "newCards":
                stopAnimations.clear()

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
                calculatePoints()
                print(f"[{game.user}]: ORA FACCIO CALCULATEPOINTS()")
                #showPoints()
                #showPoints()
                #showPoints()
                #showPoints()
                #showPoints()
            elif data["request"] == "endGameError":
                turn = False#rendo le carte NON cliccabili
                endThread = True
                inviaJSON({"request": "confirmedForceQuit"})

                stopAnimations.clear()
                if len(stop) != 0:
                    stopAnimations.wait()
                msgBox = MessageBox(
                    root=game.frame, 
                    msg="L'avversario è uscito dal gioco",
                    color=RED, 
                    btn = {    
                        "text": "Torna alla home",
                        "fg_color": RED,
                        "text_color": WHITE,
                        "command": 
                        """ lambda: print("BTN TORNA HOME")
                        lambda: game.frame.destroy()
                        lambda: vadoAlLogin() """
                        """ lambda: print("BTN TORNA HOME")
                        lambda: game.frame.destroy()
                        lambda: vadoAlLogin() """
                        """ lambda: print("BTN TORNA HOME")
                        lambda: game.frame.destroy()
                        lambda: vadoAlLogin() """
                        """ lambda: print("BTN TORNA HOME")
                        lambda: game.frame.destroy()
                        lambda: vadoAlLogin() """
                        """ lambda: print("BTN TORNA HOME")
                        lambda: game.frame.destroy()
                        lambda: vadoAlLogin() """
                        """ lambda: print("BTN TORNA HOME")
                        lambda: game.frame.destroy()
                        lambda: vadoAlLogin() """
                        """ lambda: print("BTN TORNA HOME")
                        lambda: game.frame.destroy()
                        lambda: vadoAlLogin() """
                        """ lambda: print("BTN TORNA HOME")
                        lambda: game.frame.destroy()
                        lambda: vadoAlLogin() """
                        
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
    global nDenari
    global turn

    tableCardsPicked = [c.value for c in move]

    inviaJSON({
        "request": "move",
        "tableCardsPicked" : tableCardsPicked,
        "cardPlayed": card
        })

    if len(move) != 0:
        pickedCards.append(card)

        for c in tableCardsPicked:
            pickedCards.append(c)

            if c[0] == "D":
                nDenari += 1

        if card[0] == "D":
            nDenari += 1

def getNumber(card):
    return int(card[1:])

def getMoves(card, table):
    possibilities = []
    numCarta = getNumber(card)
    somma = 0
    tableCards = [c.value for c in table]

    for i in range(len(table)):
        n = getNumber(table[i].value)

        if n == numCarta:
            #possibilities.append([c])
            possibilities.append([i])

        somma += n

    if len(possibilities) == 0:
        if somma == numCarta:
            #prendo tutte le carte del tavolo
            possibilities.append(range(len(table)))
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
                possibilities[i] = [index for index, c in enumerate(table) if c.value in possibilities[i]]
            #includo nell array non solo i .value ma tutto l'oggetto grafico
    return possibilities