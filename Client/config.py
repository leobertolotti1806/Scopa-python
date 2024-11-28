import customtkinter
from colorama import Fore, Back, Style
from PIL import Image, ImageTk
#import io
import threading
import time

#palette
BACK_COLOR = "#70b87b"
DARK_GREEN = "#3c6f44"
GREY = "#525252"
DARK_GRAY = "#2b2b2b"
WHITE = "#FFFFFF"
DARK_WHITE = "#f0f0f0"
RED = "#ff7d7d"

#sizes
R_WIDTH = 950
R_HEIGHT = 650
CARDS_HAND_SIZE = (117, 195)
CARDS_HAND_OPPONENT_SIZE = (58.7, 97.5)
CARDS_TABLE_SIZE = CARDS_HAND_OPPONENT_SIZE

def default_font():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=12, weight="normal")

def default_font_bold():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=12, weight="bold")

def default_font_medium():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=18, weight="normal")

def default_font_medium_bold():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=18, weight="bold")

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
CARDS_HAND_OPPONENT_Y = (CARDS_HAND_OPPONENT_SIZE[1] / 2) + 10
LOGO_Y = centerY() - ((CARDS_HAND_SIZE[1] - CARDS_HAND_OPPONENT_SIZE[1]) / 2)
CARDS_TABLE_Y = LOGO_Y

class MessageBox:

    color = WHITE

    def __init__(self, root, msg='', color=WHITE, font = None, btn = None):
        self.frame = customtkinter.CTkFrame(master=root)
        self.lbl = customtkinter.CTkLabel(
            master=self.frame,
            text=msg, 
            text_color=color,
            wraplength=400,
            font = default_font_bold() if font == None else font,
        )
        self.lbl.pack(pady=20, padx=20)

        if btn != None:
            btn = customtkinter.CTkButton(self.frame, **btn)
            btn.pack(padx=10, pady=5)

    
    def error(self, msg):
        self.lbl.configure(text=msg, text_color=RED)

    def show(self, closingTime = 0):
        self.frame.place(x=centerX(), y=centerY(), anchor="center")

        if(closingTime != 0):
            threading.Thread(target=self.waitClose, args=(closingTime, )).start()

    def close(self):
        self.frame.destroy()
        
    def waitClose(self, closingTime):
        time.sleep(closingTime)
        self.close()