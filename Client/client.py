import socket
import threading
import json

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

def waitMove():
    global enemyMove
    stop = False

    while not stop:
        with lock:
            enemyMove = riceviJson()

            match enemyMove["request"]:
                case "endGameError":
                    stop = True
                    #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                    #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                    #MOSTRA ERRORE CHE L'ALTRO GIOCATORE HA QUITTATO
                    break
                case "closeWindow":
                    stop = True
                    client.close()
                    break
                case "calculatePoints":
                    stop = True
                        #showPoints()
                        #showPoints()
                        #showPoints()
                        #showPoints()
                        #showPoints()
                        #showPoints()
                    break
                case "ALTRI CASI DOVE IL GIOCO FUNZIONA":
                    turn = True
                    mainGame()
                    break

turn = False
waitMoveThread = threading.Thread(target=waitMove)
enemyMove = {}

def mainGame():
    #carte.cliccabili = turn so che fa schifo ma è per fare la struttura
    if turn:
        pass
        #faccio mossa


def clickCard(card):
    print(card.value)
    card.move((90, 300))

    if turn:
        """ if possofaremossa:
            turn = False
            mossa = {"C1","C2","C3"}#metti poi le carte che si seleziona
            inviaJSON({mossa}) """
        #TUTTO IL CODICE STA DENTRO SE E' IL MIO TURNO
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP
        #FAI FUNZIONE CHE CERCA E TROVA TUTTE LE COMBINAZIONI DELLE MOSSE POSSIBILI CON LA CARTA CHE SELEZIONI DAL TUO MAZZP