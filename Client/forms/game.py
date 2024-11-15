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
        self.user = user
        self.root = root
        self.frame = customtkinter.CTkFrame(master=root,  fg_color=BACK_COLOR)
        self.frame.grid(row = 0, column = 0)
        self.frame.pack(fill="both", expand=True)
        """ self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1) """

        image = customtkinter.CTkImage(Image.open("media/logoBack.png"), size=(140, 40))
        self.lbl = customtkinter.CTkLabel(
            master=self.frame,
            image=image,
            text=""
        )

        self.lbl.place(x=centerX(), y=LOGO_Y, anchor="center")
        
        self.msgBox = MessageBox(root=self.frame)
        #client.waitForGame(self.user, self.InitGame, self.Error)
        self.animation = animation.AnimationText(self.root, self.msgBox.lbl, 300, [
            "In attesa di un giocatore.  ",
            "In attesa di un giocatore.. ",
            "In attesa di un giocatore..."
        ])
        self.InitGame(
            {
                "request": "startGame",
                "user2" : "ciasky",
                "startingTurn": True,
                "table": ["D2", "C3", "D7", "S1"],
                "cards": ["C1", "B2", "D4"]
            }
        )
        #root.master.protocol("WM_DELETE_WINDOW", lambda: client.chiusura(root.master))

    #questo significa che sto definendo la funzione da eseguire prima di fare l'init game
    def InitGame(self, obj):
        self.animation.waitStop()
        self.msgBox.close()

        self.user2 = obj['user2']

        self.lbluser1 = customtkinter.CTkLabel(master=self.frame, text=self.user, text_color=WHITE, font=default_font_subtitle())
        self.lbluser1.place(x=30, y=R_HEIGHT - 50, anchor="sw")
        self.lblstatus1 = customtkinter.CTkLabel(master=self.frame, text_color=DARK_GRAY, font=default_font_medium())
        self.lblstatus1.place(x = 30, y = R_HEIGHT - 20, anchor="sw")

        self.lbluser2 = customtkinter.CTkLabel(master=self.frame, text=self.user2, text_color=WHITE, font=default_font_subtitle())
        self.lbluser2.place(x= R_WIDTH - 30, y= 10, anchor="ne")
        self.lblstatus2 = customtkinter.CTkLabel(master=self.frame, text_color=DARK_GRAY, font=default_font_medium())
        self.lblstatus2.place(x = R_WIDTH - 30, y = 60, anchor="ne")

        #set turno
        client.turn = obj['startingTurn']

        self.BuildDrawCard(obj['cards'])
        self.setStatus()
        self.BuildTable(obj['table'])
        #client.clickCard(obj)
        client.waitMoveThread.start()

        client.deck = obj['cards']
        client.table = obj['table']
            
    def Error(self, msg):
        self.animation.stop = True
        self.msgBox.error(msg)

    def BuildDrawCard(self, card):
        self.space1 = HandSpace(
            self.root,
            self.frame,
            card,
            CARDS_HAND_SIZE,
            pos= "end",
            yStart= CARDS_HAND_Y,
            onclick=self.clickCard
        )

        self.space2 = HandSpace(
            self.root,
            self.frame,
            ["back", "back", "back"],
            CARDS_HAND_OPPONENT_SIZE,
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
        pickCards = []
        # esempio
        pickCards = [
            [
                self.table.cards[0],
                self.table.cards[1]
            ]
        ]
        #pickCards = client.getMoves(card, self.table) tipo per sapere la mossa da fare
        """
            se si può fare una mossa sola avrò in pickCards tipo
            [
                [card1, card2] in questa mossa io prendo queste 2 carte
            ]

            se ci sono più mosse possibili io avrò pickCards come
            [
                [card1, card2],
                [card1, card3, card3]
            ]

            qui quindi dovrò chiedere all'utente di scegliere quale tra le mosse possibili vuole Fare
            dopo aver scelto la mossa semplicemente chiamo la funzione che esegue la mossa (graficamente)

            le card sono oggetti!!
        """
        if(len(pickCards) == 0):
            self.table.addCard(card)
        elif (len(pickCards) == 1):
            self.execMove(card, pickCards[0])
        else:
            #self.chooseMove(card, pickCards)
            pass

            

    def execMove(self, card, move):
        card.move(
            (
                move[0].pos[0],
                move[0].pos[1]
            ),
            size= CARDS_TABLE_SIZE
        )
        for i in move[1:]:
            i.move(
                (
                    move[0].pos[0],
                    move[0].pos[1]
                )
            )
        
        #self.table.waitAnimations(move)
        #self.table.removeCards(move + [card]) #merge del vettore delle carta più la carta stessa
        #client.sendMove(card, move)
                

    def setStatus(self):
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
            



    
