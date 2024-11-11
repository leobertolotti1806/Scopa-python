import customtkinter
from PIL import Image, ImageTk

#palette
BACK_COLOR = "#70b87b"
DARK_GREEN = "#3c6f44"
GREY = "#525252"
DARK_GRAY = "#2b2b2b"
WHITE = "#FFFFFF"
RED = "#ff7d7d"

#sizes
R_WIDTH = 950
R_HEIGHT = 650
CARDS_HAND_SIZE = (125, 220)

def default_font():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=12, weight="normal")

def default_font_bold():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=12, weight="bold")

def default_font_medium():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=18, weight="normal")

def default_font_title():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=40, weight="bold")

def default_font_subtitle():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=32, weight="bold")

def centerX():
    return R_WIDTH / 2

def centerY():
    return R_HEIGHT / 2

#y carte mano 1
CARDS_HAND_Y = R_HEIGHT - (CARDS_HAND_SIZE[1] / 2) - 10

class MessageBox:

    color = WHITE

    def __init__(self, root, msg='', color=WHITE):
        self.frame = customtkinter.CTkFrame(master=root)
        self.lbl = customtkinter.CTkLabel(
            master=self.frame,
            text=msg, 
            text_color=color,
            wraplength=400,
            font=default_font_bold(),
        )
        self.lbl.pack(pady=20, padx=20)
        self.frame.grid(row=1, column=1)
    
    def error(self, msg):
        self.lbl.configure(text=msg, text_color=RED)

    def close(self):
        self.frame.destroy()
        



        