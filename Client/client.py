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
        inviaJSON({"request": "closingClient"})
        print("SONO in una partita e chiudo il client")
        root.destroy()
    else:
        #NON SONO ANCORA IN UNA PARTITA
        print("non sono in una partita e chiudo il client")
        inviaJSON({"request": "stopWaiting"})
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

    inviaJSON({
        "primiera": True,
        "carte": carte,
        "denari": denari,
        "nScope": nScope,
        "setteBello": setteBello,
        "win": win
    })


def waitMove():
    global data
    stop = False

    while not stop:
        with lock:
            data = riceviJson()
            turn = True

            match data["request"]:
                case "move":
                    turn = True
                    
                    if data["msg"] != None:
                        pass
                        #L'AVVERSARIO HA FATTO SCOPA O HA PRESO SETTE BELLO
                        #ANIMAZIONE QUI??
                        #ANIMAZIONE QUI??
                

                    if len(data["tableCardsPicked"]) == 0:
                        #non si è presa NESSUNA carta dal tavolo => aggiungo la carta al tavolo
                        table.append(data["cardPlayed"])
                        #ANIMAZIONE QUI??
                        #ANIMAZIONE QUI??
                        #ANIMAZIONE QUI??
                    else:
                        #si sono prese 1 o più carte dal tavolo => le tolgo dal tavolo
                        for c in data["tableCardsPicked"]:
                            table.remove(c)
                            #ANIMAZIONE QUI??
                            #ANIMAZIONE QUI??
                            #ANIMAZIONE QUI??
                            #ANIMAZIONE QUI??


                    """ showPickCards(cardGiocata, cardDaPrendereDalTavolo)
                    cardGiocata è data["cardPlayed"]
                    cardDaPrendereDalTavolo è data["tableCardsPicked"] """
                    break

                case "newCards":
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
                    stop = True
                    
                    calculateAndSendPoints()
                    
                    #showPoints()
                    #showPoints()
                    #showPoints()
                    #showPoints()
                    #showPoints()
                    break
                case "endGameError":
                    stop = True
                    #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                    #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                    #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                    break

turn = False
waitMoveThread = threading.Thread(target=waitMove)
data = {}

#variabili per la gestione della mossa
deck = []
selectedCards = []
cardToPlay = ""

#variabili per i punteggi
pickedCard = []
nScope = 0
setteBello = False

def getNumber(card):
    return int(card[1:])

def clickCard(card):
    # SE GIOCO UN 8 
    print(card.value)
    card

    if turn:
        if card in deck:
            #ho schiacciato una carta del mio mazzo => cancello le eventuali carte
            #selezionate prima e setto la carta selezionata dal deck
            cardToPlay = card
            selectedCards = []
        else:
            deckCardNumber = getNumber(cardToPlay)
            selectedCards.append(card)
            somma = 0

            for c in selectedCards:
                somma += getNumber(c)

            if somma == deckCardNumber:
                #EFFETTUO LA MOSSA

                if utenteConfermaMossa:
                    #L'UTENTE HA CONFERMATO LA MOSSA E LA GIOCA
                    pickedCard += selectedCards
                    msg = None
                    
                    for c in selectedCards:
                        table.remove(c)
                        #ANIMAZIONE QUI????
                        #ANIMAZIONE QUI????
                        #ANIMAZIONE QUI????
                        #ANIMAZIONE QUI????
                        #ANIMAZIONE QUI????

                    deck.remove(cardToPlay)
                    #ANIMAZIONE QUI????
                    #ANIMAZIONE QUI????
                    #ANIMAZIONE QUI????
                    #ANIMAZIONE QUI????
                    #ANIMAZIONE QUI????


                    if "D7" in selectedCards:
                        msg = Game.user + " ha preso il sette bello!!!"
                        setteBello = True
                    elif len(table) == 0:
                        msg = Game.user + " ha fatto scopa!!!"
                        nScope += 1

                    inviaJSON({
                        "request": "move",
                        "cardPlayed": cardToPlay,
                        "tableCardsPicked": selectedCards,
                        "msg": msg
                    })

                    selectedCards = []
                    cardToPlay = ""
                    turn = False
                else:
                    #L'UTENTE HA !NON! HA CONFERMATO LA MOSSA E RESETTO TUTTO
                    selectedCards = []
                    cardToPlay = ""

            elif somma < deckCardNumber:
                #FORSE FORSE potrei fare ancora una mossa (NON ASSICURATO)
                #NON POSSO TERMINARE LA MOSSA E NON POSSO INVIARE LA MOSSA
                pass
            else:
                #LE CARTE SELEZIONATE SONO OLTRE IL NUMERO DELLA CARTA DA GIOCARE
                #DESELEZIONO LE CARTE DEL TAVOLO
                
                selectedCards = []
                alert("Il numero delle carte selezionate supera quello della carta da giocare")

        #TUTTO IL CODICE STA DENTRO SE E' IL MIO TURNO

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