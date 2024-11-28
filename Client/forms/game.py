#debug
from os import system

from config import *
# modulo con le funzioni per il funzionamento del gioco
import client
import animation
from card import *

class Game:

    space1 = None
    space2 = None
    table = None

    def __init__(self, root : customtkinter.CTk, user):
        system(f"title Prompt {user}")
        self.user = user
        self.root = root
        self.frame = customtkinter.CTkFrame(master=root,  fg_color=BACK_COLOR)
        self.frame.grid(row = 0, column = 0)
        self.frame.pack(fill="both", expand=True)
        """ self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1) """
        
        self.msgBox = MessageBox(root=self.frame)
        client.waitForGame(self.user, self.InitGame, self.Error)
        self.animation = animation.AnimationText(self.root, self.msgBox.lbl, 300, [
            "In attesa di un giocatore.  ",
            "In attesa di un giocatore.. ",
            "In attesa di un giocatore..."
        ])
        root.master.protocol("WM_DELETE_WINDOW", lambda: client.chiusura(root.master))

    #questo significa che sto definendo la funzione da eseguire prima di fare l'init game
    def InitGame(self, obj):
        self.animation.waitStop()
        self.msgBox.close()

        self.user2 = obj["user2"]

        image = customtkinter.CTkImage(Image.open("media/logoBack.png"), size=(140, 40))
        self.lbl = customtkinter.CTkLabel(
            master=self.frame,
            image=image,
            text=""
        )
        self.lbl.place(x=centerX(), y=LOGO_Y, anchor="center")

        self.lbluser1 = customtkinter.CTkLabel(master=self.frame, text=self.user, text_color=WHITE, font=default_font_subtitle())
        self.lbluser1.place(x=30, y=R_HEIGHT - 50, anchor="sw")
        self.lblstatus1 = customtkinter.CTkLabel(master=self.frame, text_color=DARK_GRAY, font=default_font_medium())
        self.lblstatus1.place(x = 30, y = R_HEIGHT - 20, anchor="sw")

        self.lbluser2 = customtkinter.CTkLabel(master=self.frame, text=self.user2, text_color=WHITE, font=default_font_subtitle())
        self.lbluser2.place(x= R_WIDTH - 30, y= 10, anchor="ne")
        self.lblstatus2 = customtkinter.CTkLabel(master=self.frame, text_color=DARK_GRAY, font=default_font_medium())
        self.lblstatus2.place(x = R_WIDTH - 30, y = 60, anchor="ne")

        #set turno
        with client.lock:
            client.turn = obj["startingTurn"]
            client.startingTurn = obj["startingTurn"]

        self.BuildTable(obj["table"])
        self.BuildDrawCard(obj["cards"])
        self.setStatus()
        client.waitMoveThread = threading.Thread(target=client.waitMove, args=(self,))
        client.waitMoveThread.start()

        client.deck = obj["cards"]
            
    def Error(self, msg):
        self.animation.stop = True
        self.msgBox.error(msg)

    def BuildDrawCard(self, card):
        self.space1 = HandSpace(
            self.root,
            self.frame,
            card,
            CARDS_HAND_SIZE,
            player=1,
            pos= "end",
            yStart= CARDS_HAND_Y,
            onclick=self.clickCard
        )

        self.space2 = HandSpace(
            self.root,
            self.frame,
            ["back", "back", "back"],
            CARDS_HAND_OPPONENT_SIZE,
            player=2,
            pos= "start",
            yStart = CARDS_HAND_OPPONENT_Y,
            onclick=self.clickCard
        )

    def BuildTable(self, card):
        self.table = TableSpace(
            self.root,
            self.frame,
            card,
            CARDS_TABLE_SIZE,
            pos="start",
            yStart=CARDS_TABLE_Y
        )

    def clickCard(self, card : Card):
        #INGLOVA FUNZIONAMENTO MOSSE / GIOCO DA CLIENT.CLICKCARD
        if client.turn and len(stop) == 0:
            #array table solo con i .value delle card
            print(f"[{self.user}]: card di click card è : {card}")
            possibleMoves = client.getMoves(card.value, self.table.cards) #tipo per sapere la mossa da fare
            
            if(len(possibleMoves) == 0):
                #aggiungo la carta al tavolo
                client.sendMove(card.value, [])
                
                if(card.space == 1):
                    self.space1.cards.remove(card)
                    self.space1.calculate()
                else:
                    self.space2.cards.remove(card)
                    self.space2.calculate()
                self.table.addCard(card)
            elif (len(possibleMoves) == 1):
                #posso fare SOLO una (1) mossa
                #prendo la/le carta/carte di possibleMoves[0]
                client.sendMove(card.value, possibleMoves[0])

                if(card.space == 1):
                    self.space1.cards.remove(card)
                    self.space1.calculate()
                else:
                    self.space2.cards.remove(card)
                    self.space2.calculate()
                    
                self.execMove(card, possibleMoves[0])
            else:
                #posso fare 2 o 2+ mosse
                self.chooseMove(card, possibleMoves)

            if not client.lastPlay and len(self.table.cards) == 0:
                #se è l'ultima mossa e NON E' L'ULTIMA MOSSA
                #aggiungo un punto
                client.nScope += 1

            with client.lock:
                client.turn = False

            self.setStatus()

            
    def execMove(self, card : Card, pickCard):
        # ora la carte che voglio giocare per proseguire devono aspettare lo stop
        pickCard.append(card)
        self.table.cards.append(card)
        self.table.rmCards = pickCard
        print(f"{Back.RED} {Fore.BLACK} Carte da rimuovere: {self.table.rmCards} {Back.BLACK} {Fore.WHITE}")

        """for i in self.table.rmCards:
            i.waitStop = True
        self.table.cards.append(card)
        pickCard.append(card)
        self.table.removeCards(pickCard)"""
        threading.Thread(target=self.renderMove).start()
        #merge del vettore delle carta più la carta stessa

    def renderMove(self):
        for i in self.table.rmCards:
            i.move(
                (
                    self.table.rmCards[0].pos[0],
                    self.table.rmCards[0].pos[1]
                ),
                size=CARDS_TABLE_SIZE
            )
        #self.table.waitForRemove(card, pickCard)
        #self.table.waitAnimations()
        #waitAnimations() # aspetto la fine di tutte le animazioni
        stopAnimations.clear() # resetto lo stop
        stopAnimations.wait() # aspetto che mi arriva da qualche carta che sa di essere ultima un evento
        self.table.removeCards()
        stopAnimations.clear()
        stopAnimations.wait()
        self.table.destroyPickedCards()
    
    def chooseMove(self, card, possibleMoves):
        #creare bottoni
        self.currentMove = 0
        self.btnMove = customtkinter.CTkButton(
            master=self.frame, 
            text="OK", 
            height=40, 
            width=100,
            bg_color=BACK_COLOR,
            fg_color=WHITE, 
            text_color=DARK_GRAY, 
            font=default_font_medium_bold(),
            command= lambda m=possibleMoves, c=card: self.confirmMove(c, m)
        )
        self.btnMove.place(x=centerX(), y=LOGO_Y + 100, anchor="center")

        imageL = customtkinter.CTkImage(Image.open("media/arrowL.png"), size=(40, 40))
        self.arrowL = customtkinter.CTkLabel(
            master=self.frame,
            image=imageL,
            text=""
        )
        self.arrowL.place(x=centerX() - 60, y=LOGO_Y + 100, anchor="center")
        self.arrowL.bind("<Button-1>", lambda event, m=possibleMoves: self.scrollMove(-1, m))

        imageR = customtkinter.CTkImage(Image.open("media/arrowR.png"), size=(40, 40))
        self.arrowR = customtkinter.CTkLabel(
            master=self.frame,
            image=imageR,
            text=""
        )
        self.arrowR.place(x=centerX() + 60, y=LOGO_Y + 100, anchor="center")
        self.arrowR.bind("<Button-1>", lambda event, m=possibleMoves: self.scrollMove(1, m))
        
        self.displayPossibleMove(possibleMoves)

    def scrollMove(self, change, possibleMoves):
        print("scrolla")
        self.currentMove += change

        self.displayPossibleMove(possibleMoves)

    def displayPossibleMove(self, possibleMoves): 
        self.clearCardsBackground()
        
        for i in possibleMoves[abs(self.currentMove) % len(possibleMoves)]:
            i.configure(bg_color=RED)

    def confirmMove(self, card, possibleMoves):
        mossa = possibleMoves[abs(self.currentMove) % len(possibleMoves)]

        client.sendMove(card.value, mossa)

        if(card.space == 1):
            self.space1.cards.remove(card)
            self.space1.calculate()
        else:
            self.space2.cards.remove(card)
            self.space2.calculate()
        self.execMove(card, mossa)

        self.btnMove.destroy()
        self.arrowL.destroy()
        self.arrowR.destroy()

        self.clearCardsBackground()

    def clearCardsBackground(self):
        for i in self.table.cards:
            i.configure(bg_color="transparent")

    
    def setStatus(self):
        print(f"[{self.user}]: client.turn: {client.turn}")
        if(self.animation.thread.is_alive()):
            self.animation.waitStop()
        if(client.turn):
            self.lblstatus2.configure(text="")
            self.animation = animation.AnimationText(self.root, self.lblstatus1, 300, [
                "Fai la tua mossa.  ",
                "Fai la tua mossa.. ",
                "Fai la tua mossa..."
            ])
        else:
            self.lblstatus1.configure(text="")
            self.animation = animation.AnimationText(self.root, self.lblstatus2, 300, [
                "Sta pensando 😐",
                "Sta pensando 🤨",
                "Sta pensando 🤔"
            ])