# config contiene customtkinter
from config import *

# import Forms
from forms.login import *

from animation import *

customtkinter.set_appearance_mode("dark") # dark, system
#customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.title("Scopa")
root.iconbitmap("media/icon.ico")
root.geometry(f"{R_WIDTH}x{R_HEIGHT}")
root.maxsize(width=R_WIDTH, height=R_HEIGHT)
root.minsize(width=R_WIDTH, height=R_HEIGHT)

frame = customtkinter.CTkFrame(master=root, bg_color=BACK_COLOR, fg_color=BACK_COLOR)
frame.pack(fill='both', expand=True)

# il gioco parte dal login
Login(frame)

root.mainloop()