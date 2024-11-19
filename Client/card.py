from customtkinter import CTkLabel
from config import *
#import client
import threading
from animation import Rect
import time

semaphore = threading.Semaphore()
eventStop = threading.Event()
stop = []

class Card(CTkLabel):

    def __init__(
            self,
            value,
            pos,
            cardImg,
            size,
            root : customtkinter.CTk,
            onclick = None,
            **args
        ):
        image = customtkinter.CTkImage(cardImg, size=size)
        super().__init__(**args, image=image)
        self.root = root
        self.pos = pos
        self.value = value
        self.img = cardImg
        self.size = size
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
        sizeX = self.size[0]
        sizeY = self.size[1]
        self.eventAnimation.wait()
        semaphore.acquire()
        stop.append(True)
        semaphore.release()
        if(self.waitBeforeAnimation != 0):
            time.sleep(self.waitBeforeAnimation)
            self.waitBeforeAnimation = 0
        if(sizeX != self.size):
            image = customtkinter.CTkImage(self.img, size=self.size)
            self.configure(image=image)
        self.animation(x, y, Rect((x, y), self.pos))
        self.eventAnimation.clear()
        semaphore.acquire()
        stop.remove(True)
        semaphore.release()
        eventStop.set()
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
                self._update_image()
                if(index == 2):
                    time.sleep(0.0000005)
                    index = 0

    def move(self, p2, timeW = 0, size = "NaN"):
        self.pos = p2
        if(size != "NaN"):
            self.size = size
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
            self.cards.append(
                Card(
                    root= self.root,
                    master=master,
                    text="",
                    cardImg = Image.open(f"media/cards/{cards[i]}.png"),
                    size = self.size,
                    anchor = "center",
                    pos = (self.x, self.y),
                    value=cards[i],
                    onclick=onclick
                )
            )
        self.calculate(True)
    
    def calculate(self, delay=0):
        spaceSize = (len(self.cards) * self.size[0]) + (len(self.cards) * 10)
        #            spazio occuppato dalle carte    spazio margini
        xstart = centerX() - (spaceSize / 2)
        time = 0

        for i in range(len(self.cards)):
            if(delay != 0):
                time = i
            self.cards[i].move(
                (
                    xstart + (self.size[0] / 2) + ((self.size[0] + 10) * i),
                    self.y
                ),
                timeW = time
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
        self.rmCards = []
        self.finshAnimation = 0
        self.root = root
        self.cards = []
        self.size = size
        if(pos == "end"):
            self.x = R_WIDTH + self.size[0]
        elif(pos == "start"):
            self.x = - self.size[0]
        self.y = yStart
        for i in range(len(cards)):
            self.cards.append(
                Card(
                    root= self.root,
                    master=master,
                    text="",
                    cardImg= Image.open(f"media/cards/{cards[i]}.png"),
                    size = self.size,
                    anchor = "center",
                    pos = (self.x, self.y),
                    value=cards[i],
                )
            )
        self.calculate(True)
    
    def calculate(self, delay = 0):
        spaceSize = (len(self.cards) * self.size[0]) + (len(self.cards) * 10)
        #            spazio occuppato dalle carte    spazio margini
        x = 0
        xstart = centerX() - (spaceSize / 2)
        time = 0

        for i in range(len(self.cards)):
            x = xstart + (self.size[0] / 2) + ((self.size[0] + 10) * i)
            if(delay != 0):
                time = (1 * i)
            self.cards[i].move(
                (
                    x,
                    self.y
                ),
                timeW=time
            )
        return x # ultima posizione dove inserire la carta
    
    def addCard(self, card : Card):
        self.cards.append(card)
        x = self.calculate()
        card.move(
            (
                x,
                self.y
            ),
            size= CARDS_TABLE_SIZE
        )

    def removeCards(self):
        for card in self.rmCards:
            rm = self.indexRm(card)
            if(rm):
                rm.move(
                    (
                        R_WIDTH + self.size[0],
                        self.y
                    )
                )
        self.calculate()

    def indexRm(self, card):
        for i in range(len(self.cards)):
            if(self.cards[i].value == card.value):
                return self.cards.pop(i)
            
    def waitAnimations(self):
        eventStop.wait()
        eventStop.clear()
        if(len(stop) != 0):
            self.waitAnimations()
        

            
            


        


    
    

