from config import *
# modulo con le funzioni per il funzionamento del gioco
import client
import animation

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
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        image = customtkinter.CTkImage(Image.open("media/logoBack.png"), size=(140, 40))
        self.lbl = customtkinter.CTkLabel(
            master=self.frame,
            image=image,
            text=""
        )

        self.lbl.grid(row=1, column=1)
        
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
                "startingTurn": True,
                "table": [],
                "cards": ["C1", "B2", "D4"]
            }
        )

    #questo significa che sto definendo la funzione da eseguire prima di fare l'init game
    def InitGame(self, obj):
        self.animation.wait()
        self.msgBox.close()
        self.frameGame = customtkinter.CTkFrame(master=self.frame, bg_color='black', fg_color='transparent')
        self.frameGame.grid(row=1, column=1, sticky='w')
        client.turn = obj['startingTurn']
        #carte.cliccabili = client.turn #so che fa schifo ma è per fare la struttura
        self.BuildDrawCard(obj['cards'])
        #self.BuildTable(obj['table'])
        client.clickCard(obj)
            
    def Error(self, msg):
        self.animation.stop = True
        self.msgBox.error(msg)

    def BuildDrawCard(self, card):
        for i in range(len(card)):
            img = customtkinter.CTkImage(Image.open(f"media/cards/{card[i]}.png"), size=(75, 120))
            self.cards_hand.append(
                customtkinter.CTkLabel(
                    master=self.frameGame,
                    text="",
                    image = img,
                    anchor = "center",
                ).pack(padx=10, pady=10 )
            )



    
