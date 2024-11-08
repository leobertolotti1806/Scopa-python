import customtkinter
from PIL import Image

BACK_COLOR = "#70b87b"
GREY = "#525252"
DARK_GRAY = "#2b2b2b"
WHITE = "#FFFFFF"
RED = "#ff7d7d"

def default_font():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=12, weight="normal")

def default_font_bold():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=12, weight="bold")

def default_font_medium():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=18, weight="normal")

def default_font_title():
    return customtkinter.CTkFont(family="Microsoft YaHei", size=40, weight="bold")

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



        