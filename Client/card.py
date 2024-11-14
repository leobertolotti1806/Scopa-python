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
            root : customtkinter.CTk,
            onclick = None,
            **args
        ):
        super().__init__(**args)
        self.root = root
        self.pos = pos
        self.value = value
        self.eventAnimation = threading.Event()
        self.waitBeforeAnimation = 0
        if(onclick != None):
            self.bind("<Button-1>", lambda event, e=self: onclick(e))
        self.place(x=self.pos[0], y=self.pos[1], anchor="center")
        self.render = threading.Thread(target=self.waitAnimation)
        self.render.start()

    def waitAnimation(self):
        x = self.pos[0]
        y = self.pos[1]
        self.eventAnimation.wait()
        if(self.waitBeforeAnimation):
            time.sleep(self.waitBeforeAnimation)
            self.waitBeforeAnimation = 0
        self.animation(x, y, Rect((x, y), self.pos))
        self.eventAnimation.clear()
        self.waitAnimation()

    def animation(self, x, y, rect : Rect):
        if(not rect.error):
            index = 0
            while x != self.pos[0]:
                #print(x)
                index += 1
                if(self.pos[0] < x):
                    x -= 0.25
                    x = round(x, 2)
                else:
                    x += 0.25
                    x = round(x, 2)

                y = rect.getY(x)
                self.place(x=x, y=y, anchor="center")
                #self.update()
                if(index == 2):
                    time.sleep(0.0000001)
                    index = 0

    def move(self, p2, timeW = 0):
        self.pos = p2
        if(not self.eventAnimation.is_set()):
            self.waitBeforeAnimation = timeW
            self.eventAnimation.set()

class HandSpace:

    def __init__(
        self,
        root,
        master,
        cards,
        size,
        pos,
        yStart,
        onclick
    ):
        self.root = root
        self.cards = []
        self.size = size
        if(pos == "end"):
            self.x = R_WIDTH + self.size[0]
        elif(pos == "start"):
            self.x = - self.size[0]
        self.y = yStart
        for i in range(len(cards)):
            img = customtkinter.CTkImage(Image.open(f"media/cards/{cards[i]}.png"), size=self.size)
            self.cards.append(
                Card(
                    root= self.root,
                    master=master,
                    text="",
                    image = img,
                    anchor = "center",
                    pos = (self.x, self.y),
                    value=cards[i],
                    onclick=onclick
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
                ),
                timeW=(1 * i)
            )
            
class TableSpace:

    def __init__(
        self,
        root,
        master,
        cards,
        size,
        pos,
        yStart
    ):
        self.root = root
        self.cards = []
        self.size = size
        if(pos == "end"):
            self.x = R_WIDTH + self.size[0]
        elif(pos == "start"):
            self.x = - self.size[0]
        self.y = yStart
        for i in range(len(cards)):
            img = customtkinter.CTkImage(Image.open(f"media/cards/{cards[i]}.png"), size=self.size)
            self.cards.append(
                Card(
                    root= self.root,
                    master=master,
                    text="",
                    image = img,
                    anchor = "center",
                    pos = (self.x, self.y),
                    value=cards[i],
                )
            )
        self.calculate()
    
    def calculate(self):
        spaceSize = (len(self.cards) * self.size[0]) + (len(self.cards) * 10)
        #            spazio occuppato dalle carte    spazio margini
        x = 0
        xstart = centerX() - (spaceSize / 2)

        for i in range(len(self.cards)):
            x = xstart + (self.size[0] / 2) + ((self.size[0] + 10) * i)
            self.cards[i].move(
                (
                    x,
                    self.y
                )
            )
        return x # ultima posizione dove inserire la carta
    
    def addCard(self, card : Card):
        self.cards.append(card)
        x = self.calculate()
        card.move(
            (
                x,
                self.y
            )
        )


            
            


        


    
    

