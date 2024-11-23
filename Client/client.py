import socket
import threading
import json
from itertools import permutations

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
        root.destroy()
    else:
        #NON SONO ANCORA IN UNA PARTITA
        inviaJSON({"request": "stopWaiting"})
        print("non sono in una partita e chiudo il client")
        root.destroy()

#Host = "172.27.128.1" MAXWELL PC LEO
#Host = "192.168.178.24" PC LEO CASA
Host = "192.168.178.24"
Host = socket.gethostbyname(socket.gethostname())
Porta = 9999
Indirizzo = (Host, Porta)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def waitForGame(nickname, resolver, error):
    threading.Thread(target=connect, args=(nickname, resolver, error)).start()

def connect(nickname, resolver, error):
    try:
        # Prova a connettersi al server
        client.connect(Indirizzo)
        inviaJSON({"nome": nickname})
        resolver(riceviJson())
    except socket.error as e:
        # Gestisce errori di connessione
        client.close()
        error(f'Impossibile Collegarsi al Server\n\n({e})')


lock = threading.Lock()

def calculateAndSendPoints():
    #controllo numero carte
    if len(pickedCard) > 20:
        carte = True
    elif len(pickedCard) < 20:
        carte = False
    else:
        carte = "pari"

    #controllo dei denari
    nDenari = 0
    for c in pickedCard:
        if c.startswith("D"):
            d += 1

    if nDenari > 5:
        denari = True
    elif nDenari < 5:
        denari = False
    else:
        denari = "pari"

    #FAI CONTROLLO VITTORIA
    #FAI CONTROLLO VITTORIA
    #FAI CONTROLLO VITTORIA
    #FAI CONTROLLO VITTORIA


def waitMove(game):
    global data
    endThread = False

    inviaJSON({"request": "startGameOk"})

    while not endThread:
        with lock:
            data = riceviJson()
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON
        #CONTROLLA M0STRA MSG AVVERSARIO SCOPA / SETTE BELLO IN RICEVIJSON



        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
        #CONTROLLA SCOPE AVVERSARIO (GESTISCILO IN request == move) con scopeAvversario += 1
            turn = True

            if data != None:
                match data["request"]:
                    case "move":
                        #renderizzo mossa

                        if data["cardPlayed"] == "D7" or "D7" in data["tableCardsPicked"]:
                            alert(f"{game.user2} ha preso sette bello!!!")
                        
                        tableCardsPicked = [c for c in game.table.cards if c.value in data["tableCardsPicked"]] # carte prese dall' avversario

                        if len(game.table.cards) - len(tableCardsPicked):
                            nScopeAvversario += 1

                        game.space2.cards[0].value = data["cardPlayed"]
                        
                        game.execMove(
                            game.space2.cards[0], # carta giocata dall'avversario
                            tableCardsPicked
                        )                                
                        #L'AVVERSARIO HA FATTO SCOPA O HA PRESO SETTE BELLO
                        #ANIMAZIONE QUI??
                                
                        """ showPickCards(cardGiocata, cardDaPrendereDalTavolo)
                        cardGiocata è data["cardPlayed"]
                        cardDaPrendereDalTavolo è data["tableCardsPicked"] """
                        break

                    case "newCards":
                        #IL SERVER DISTRIBUISCE LE CARTE
                        if data["msg"] != None:
                            pass
                            #L'AVVERSARIO HA FATTO SCOPA O HA PRESO SETTE BELLO
                            #ANIMAZIONE QUI??
                            #ANIMAZIONE QUI??

                        cards = data["cards"]
                        #Game.BuildDrawCard(cards)
                        #QUI LE CARTE VENGONO CREATE ANCHE PER L'AVVERSARIO????
                        #QUI LE CARTE VENGONO CREATE ANCHE PER L'AVVERSARIO????
                        #QUI LE CARTE VENGONO CREATE ANCHE PER L'AVVERSARIO????
                        #QUI LE CARTE VENGONO CREATE ANCHE PER L'AVVERSARIO????
                        #QUI LE CARTE VENGONO CREATE ANCHE PER L'AVVERSARIO????
                        #QUI LE CARTE VENGONO CREATE ANCHE PER L'AVVERSARIO????
                        break
                    case "calculatePoints":
                        endThread = True
                        
                        calculateAndSendPoints()
                        
                        #showPoints()
                        #showPoints()
                        #showPoints()
                        #showPoints()
                        #showPoints()
                        break
                    case "endGameError":
                        endThread = True
                        inviaJSON({"request": "confirmedForceQuit"})
                        #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                        #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                        #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                        #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                        #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                        #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
            else:
                endThread = True

waitMoveThread = None
data = {}
turn = False
#variabili per i punteggi
pickedCard = []
nScope = 0
setteBello = False
nScopeAvversario = 0

def sendMove(card, move = []):

    pickedCards = [c.value for c in move]

    inviaJSON({
        "request": "move",
        "tableCardsPicked" : pickedCards,
        "cardPlayed": card
        })
    
    if len(move) == 0:
        #prendo delle carte    
        pickedCard.append(card)
        pickedCard.append(pickedCards)

def getNumber(card):
    return int(card[1:])

def getMoves(card, table):
    possibilities = []
    numCarta = getNumber(card)
    somma = 0
    tableCards = [c.value for c in table]

    for c in table:
        n = getNumber(c.value)

        if n == numCarta:
            possibilities.append([c])
            
        somma += n

    if len(possibilities) == 0:
        if somma == numCarta:
            #prendo tutte le carte del tavolo
            possibilities.append(table)
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
                possibilities[i] = [c for c in table if c.value in possibilities[i]]
            #includo nell array non solo i .value ma tutto l'oggetto grafico
    return possibilities