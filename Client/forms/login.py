# config contiene customtkinter
from config import *
from forms.game import *


class Login:
    def __init__(self, root : customtkinter.CTk):
        self.root = root
        self.frame = customtkinter.CTkFrame(master=root, bg_color=BACK_COLOR, corner_radius=15)
        self.frame.pack(padx=50, pady=50, expand=True)
        self.build()
    
    def build(self):
        image = customtkinter.CTkImage(Image.open("media/logo.png"), size=(200, 55))
        self.lbl = customtkinter.CTkLabel(
            master=self.frame, 
            image=image, 
            text=""
        )
        self.lbl.pack(pady=(100, 20), padx= 50)

        self.lbl2 = customtkinter.CTkLabel(
            master=self.frame, 
            text="Benvenuto", 
            font=default_font_medium(), 
            justify="left", 
            width=250, 
            anchor="w",
            text_color=GREY
        )
        self.lbl2.pack(pady= (0, 5), padx=50)

        self.txt1 = customtkinter.CTkEntry(
            master=self.frame, 
            placeholder_text="inserisci il Nickname", 
            width=250,
            height=50, 
            font=default_font()
        )
        self.txt1.pack(pady= 5, padx= 50)

        self.btnLogin = customtkinter.CTkButton(
            master=self.frame, 
            text="GIOCA", 
            width=250, 
            height=50,
            anchor="center", 
            font=default_font_bold(),
            command= self.Enter
        )

        self.btnLogin.pack(pady= (5, 100), padx = 50)

    def Enter(self):
        if(self.txt1.get() != ""):
            self.StartGame(self.txt1.get())

    def StartGame(self, user):
        self.frame.destroy()
        Game(self.root, user)

