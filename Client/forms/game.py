from config import *
# modulo con le funzioni per il funzionamento del gioco
import client
import animation
from card import *

class Game:

    cards_hand = []
    cards_table = []

    def __init__(self, root : customtkinter.CTk, user):
        self.cards_hand = []
        self.cards_table = []
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

        self.lbl.place(x=centerX(), y=centerY(), anchor="center")
        
        self.msgBox = MessageBox(root=self.frame)
        client.waitForGame(self.user, self.InitGame, self.Error)
        self.animation = animation.AnimationText(self.root, self.msgBox.lbl, 300, [
            "In attesa di un giocatore.  ",
            "In attesa di un giocatore.. ",
            "In attesa di un giocatore..."
        ])
        """ self.InitGame(
            {
                "request": "startGame",
                "user2" : "ciasky",
                "startingTurn": True,
                "table": [],
                "cards": ["C1", "B2", "D4"]
            }
        )
 """
        root.master.protocol("WM_DELETE_WINDOW", lambda: client.chiusura(root.master))

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
        self.setStatus()

        self.BuildDrawCard(obj['cards'])
        #self.BuildTable(obj['table'])
        #client.clickCard(obj)
        client.waitMoveThread.start()
        
        client.mainGame()
            
    def Error(self, msg):
        self.animation.stop = True
        self.msgBox.error(msg)

    def BuildDrawCard(self, card):
        for i in range(len(card)):
            img = customtkinter.CTkImage(Image.open(f"media/cards/{card[i]}.png"), size=CARDS_HAND_SIZE)
            w_card = Card(
                master=self.frame,
                text="",
                image = img,
                anchor = "center",
                value=card[i],
                root=self.root
            )
            self.cards_hand.append(
                w_card
            )

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
            



    
