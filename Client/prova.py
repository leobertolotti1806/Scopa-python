import customtkinter
from config import *
from animation import Rect
import time

root = customtkinter.CTk()
root.geometry(f'{R_WIDTH}x{R_HEIGHT}')

canvas = customtkinter.CTkCanvas(master=root)
canvas.pack(fill='both', expand=True)
native = Image.open("media/cards/D7.png")
native = native.resize(CARDS_HAND_SIZE)
img = ImageTk.PhotoImage(native)
x = 0
y = 0
def move(obj, x, y, i):
    #print("image:", canvas.coords(obj))
    canvas.move(obj, 0.1, 0)
    canvas.after(1, lambda : move(obj, x, y, i))

def place():
    x = canvas.winfo_width() / 2
    y = canvas.winfo_height() / 2
    print(x , y)
    obj = canvas.create_image(x, y, anchor='center', image=img)
    obj = canvas.create_image(x + 1, y + 1, anchor='center', image=img)
    time.sleep(1)
    move(obj, 500, 200, 1)

root.after(100, place)
root.mainloop()
