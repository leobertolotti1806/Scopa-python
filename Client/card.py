from customtkinter import CTkLabel
from config import *
import client
import threading
from animation import Rect
import time

class Card(CTkLabel):

    def __init__(
            self,
            value,
            pos,
            **args
        ):
        super().__init__(**args)
        self.pos = pos
        self.value = value
        self.eventAnimation = threading.Event()
        self.bind("<Button-1>", lambda event, e=self: client.clickCard(e))
        self.place(x=self.pos[0], y=self.pos[1], anchor="center")
        self.render = threading.Thread(target=self.waitAnimation)
        self.render.start()

    def waitAnimation(self):
        x = self.pos[0]
        y = self.pos[1]
        self.eventAnimation.wait()
        self.animation(x, y, Rect((x, y), self.pos))
        self.eventAnimation.clear()
        self.waitAnimation()

    def animation(self, x, y, rect : Rect):
        index = 0
        if(not rect.error):
            while x != self.pos[0]:
                print(x)
                index += 1
                if(self.pos[0] < x):
                    x -= 0.1
                    x = round(x, 1)
                else:
                    x += 0.1
                    x = round(x, 1)

                y = rect.getY(x)
                self.place(x=x, y=y, anchor="center")
                time.sleep(0.001)

    def move(self, p2):
        self.pos = p2
        if(not self.eventAnimation.is_set()):
            self.eventAnimation.set()

class HandSpace:

    def __init__(
        self,
        master,
        cards,
        size,
        y
    ):
        self.cards = []
        self.size = size
        self.y = y
        for i in range(len(cards)):
            img = customtkinter.CTkImage(Image.open(f"media/cards/{cards[i]}.png"), size=self.size)
            self.cards.append(
                Card(
                    master=master,
                    text="",
                    image = img,
                    anchor = "center",
                    pos = (R_WIDTH + self.size[0], self.y),
                    value=cards[i],
                )
            )
        self.calculate()
    
    def calculate(self):
        spaceSize = (len(self.cards) * self.size[0]) + (len(self.cards) * 10)
        #            spazio occuppato dalle carte    spazio margini
        xstart = centerX() - (spaceSize / 2)

        for i in range(len(self.cards)):
            self.cards[i].move(
                (
                    xstart + (self.size[0] / 2) + ((self.size[0] + 10) * i),
                    self.y
                )
            )
            
            


        


    
    

