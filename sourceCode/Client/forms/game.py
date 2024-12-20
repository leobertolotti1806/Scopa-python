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

    def __init__(self, root : customtkinter.CTk, user, ip):
        system(f"title Prompt {user}")
        self.user = user
        self.root = root
        self.renderingMove = False
        self.frame = customtkinter.CTkFrame(master=root,  fg_color=BACK_COLOR)
        self.frame.grid(row = 0, column = 0)
        self.frame.pack(fill="both", expand=True)
        """ self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1) """
        
        self.msgBox = MessageBox(root=self.frame)
        self.msgBox.show()
        client.waitForGame(self.user, ip, self.InitGame, self.Error)
        self.animation = animation.AnimationText(self.root, self.msgBox.lbl, 300, [
            "In attesa di un giocatore.  ",
            "In attesa di un giocatore.. ",
            "In attesa di un giocatore..."
        ])
        root.master.protocol("WM_DELETE_WINDOW", lambda: client.chiusura(root.master))

    #questo significa che sto definendo la funzione da eseguire prima di fare l'init game
    def InitGame(self, obj):
        print(self.user, "connesso!!")
        self.animation.stopAnimation()
        self.msgBox.close()
        self.user2 = obj["user2"]

        image = customtkinter.CTkImage(Image.open("media/logoBack.png"), size=(140, 40))
        self.lbl = customtkinter.CTkLabel(
            master=self.frame,
            image=image,
            text=""
        )

        self.lbl.place(x=centerX(), y=LOGO_Y, anchor="center")

        # setting name and turn animation of p1
        self.lbluser1 = customtkinter.CTkLabel(master=self.frame, text=self.user, text_color=WHITE, font=default_font_subtitle())
        self.lbluser1.place(x=30, y=R_HEIGHT - 50, anchor="sw")
        self.lblstatus1 = customtkinter.CTkLabel(master=self.frame, text_color=DARK_GRAY, font=default_font_medium())
        self.lblstatus1.place(x = 30, y = R_HEIGHT - 20, anchor="sw")

        # setting name and turn animation of p2
        self.lbluser2 = customtkinter.CTkLabel(master=self.frame, text=self.user2, text_color=WHITE, font=default_font_subtitle())
        self.lbluser2.place(x= R_WIDTH - 30, y= 10, anchor="ne")
        self.lblstatus2 = customtkinter.CTkLabel(master=self.frame, text_color=DARK_GRAY, font=default_font_medium())
        self.lblstatus2.place(x = R_WIDTH - 30, y = 60, anchor="ne")

        # setting lbl deck card
        self.frameDeck = customtkinter.CTkFrame(master=self.frame)
        customtkinter.CTkLabel(
            master=self.frameDeck,
            text="CARTE\nRIMASTE",
            text_color=WHITE,
            font=default_font_bold()
        ).pack(padx=10, pady=(10, 1))
        self.lbldeck = customtkinter.CTkLabel(
            master=self.frameDeck,
            text="30",
            text_color=WHITE,
            font=default_font_subtitle()
        )
        self.lbldeck.pack(padx=10, pady=(1, 10))
        self.frameDeck.place(x=R_WIDTH - 10, y=R_HEIGHT - 10, anchor="se")

        #set turno
        with client.lock:
            client.turn = obj["startingTurn"]
            client.startingTurn = obj["startingTurn"]

        self.BuildTable(obj["table"])
        self.BuildDrawCard(obj["cards"])
        self.setStatus()
        client.waitMoveThread = threading.Thread(target=client.waitMove, args=(self,))
        client.waitMoveThread.start()
            
    def Error(self, msg):
        self.animation.stopAnimation()
        self.msgBox.error(
            msg, 
            {
                "text": "Torna alla home",
                "fg_color": RED,
                "text_color": WHITE,
                "command": lambda: client.home(self.frame, self.user)
            })

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
        if client.turn and len(stop) == 0:
            possibleMoves = client.getMoves(card.value, self.table.cards) #tipo per sapere la mossa da fare
                  
            if(len(possibleMoves) == 0):
                #aggiungo la carta al tavolo
                if(card.space == 1):
                    self.space1.cards.remove(card)
                    self.space1.calculate()
                else:
                    self.space2.cards.remove(card)
                    self.space2.calculate()
                self.table.addCard(card)

                client.sendMove(card.value, [])

            elif (len(possibleMoves) == 1):
                #posso fare SOLO una (1) mossa
                #prendo la/le carta/carte di possibleMoves[0]
                client.lastTake = True

                if(card.space == 1):
                    self.space1.cards.remove(card)
                    self.space1.calculate()
                else:
                    self.space2.cards.remove(card)
                    self.space2.calculate()
                
                self.execMove(card, possibleMoves[0], 1)
                client.sendMove(card.value, self.getCardsFromIndices(possibleMoves[0]))
            else:
                client.lastTake = True
                #posso fare 2 o 2+ mosse
                self.chooseMove(card, possibleMoves)

            if not client.lastPlay and len(self.table.cards) == 0:
                #se è l'ultima mossa e NON E' L'ULTIMA MOSSA
                #aggiungo un punto
                client.points["Scope1"] += 1

            with client.lock:
                client.turn = False

            self.setStatus()

            
    def execMove(self, card, pickCard, player):
        # ora la carte che voglio giocare per proseguire devono aspettare lo stop

        self.table.rmCards = pickCard

        print(f"{Back.RED} {Fore.BLACK} Carte da rimuovere: {self.table.rmCards} {Back.BLACK} {Fore.WHITE}")

        threading.Thread(target=self.renderMove, args=(card, player, "eseguo mossa")).start()
        #merge del vettore delle carta più la carta stessa

    def renderMove(self, card, player, msg=""):
        self.renderingMove = True
        print(msg)
        for i in self.table.rmCards:
            self.table.cards[i].move(
                (
                    self.table.cards[self.table.rmCards[0]].pos[0],
                    self.table.cards[self.table.rmCards[0]].pos[1]
                ),
                0.5,
                size=CARDS_TABLE_SIZE
            )

        if card != None:
            card.move(
                (
                    self.table.cards[self.table.rmCards[0]].pos[0],
                    self.table.cards[self.table.rmCards[0]].pos[1]
                ),
                0.5,
                size=CARDS_TABLE_SIZE
            )
        stopAnimations.clear() # resetto lo stop
        stopAnimations.wait() # aspetto che mi arriva da qualche carta che sa di essere ultima un evento
        
        engagedCards = client.getValues(self.getCardsFromIndices(self.table.rmCards))
        #ANIMAZIONE
        
        self.table.removeCards(card, player)
    
        tableCardValues = client.getValues(self.table.cards)

        if card != None:
            if ("D7" in engagedCards or
                "D7" == card.value) and len(tableCardValues) == 0:
                self.table.cards = []
                #scopa con settebello
                if player == 1:
                    client.points["Sette bello"] = "Sì"
                    client.points["Scope1"] += 1
                else:
                    client.points["Scope2"] += 1

                MessageBox(self.frame, "Scopa con sette bello!",
                    WHITE, default_font_subtitle()).show(2)

            elif len(tableCardValues) == 0:
                self.table.cards = []
                #scopa
                if player == 1:
                    client.points["Scope1"] += 1
                else:
                    client.points["Scope2"] += 1

                MessageBox(self.frame, "Scopa!",
                    WHITE, default_font_subtitle()).show(2)
                
            elif ("D7" in engagedCards or
                "D7" == card.value):
                #setteBello
                if player == 1:
                    client.points["Sette bello"] = "Sì"

                MessageBox(self.frame, "Sette bello!",
                    WHITE, default_font_subtitle()).show(2)

            #self.table.destroyPickedCards(card)

            print("mando la calculatepoints?", client.waitingFinish, len(self.space1.cards) == 0, len(self.space2.cards) == 0)
            if(client.waitingFinish and len(self.space1.cards) == 0 and len(self.space2.cards) == 0):
                if(len(stop) != 0):
                    stopAnimations.clear()
                    stopAnimations.wait()
                client.waitFinishGame.set()
            self.renderingMove = False
            self.setStatus()
    
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
        #possibleMovesInCards = self.getCardsFromIndices(possibleMoves)
        #prendo le carte del tavolo in base agli indici
        for i in possibleMoves[abs(self.currentMove) % len(possibleMoves)]:
            #i.configure(bg_color=RED)
            self.table.cards[i].configure(bg_color=RED)

    def confirmMove(self, card, possibleMoves):
        mossa = possibleMoves[abs(self.currentMove) % len(possibleMoves)]

        if(card.space == 1):
            self.space1.cards.remove(card)
            self.space1.calculate()
        else:
            self.space2.cards.remove(card)
            self.space2.calculate()

        self.execMove(card, mossa, 1)
        client.sendMove(card.value, self.getCardsFromIndices(mossa))

        self.btnMove.destroy()
        self.arrowL.destroy()
        self.arrowR.destroy()

        self.clearCardsBackground()

    def clearCardsBackground(self):
        for i in self.table.cards:
            i.configure(bg_color="transparent")

    
    def setStatus(self, cancelText = False):
        self.animation.stopAnimation()

        if not cancelText:
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
        else:
            self.lblstatus1.configure(text = "")
            self.lblstatus2.configure(text = "")

    def getCardsFromIndices(self, indices):
        if isinstance(indices[0], list):
            return [self.table.cards[i] for group in indices for i in group]
        else: 
            #Lista normale
            return [self.table.cards[i] for i in indices]