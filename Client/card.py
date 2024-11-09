from customtkinter import CTkLabel
from config import *
import client
import threading
from animation import Rect
import time

class Card(CTkLabel):

    def __init__(
            self,
            root,
            value,
            pos = (R_WIDTH + 10, centerY()),
            **args
        ):
        super().__init__(**args)
        self.root = root
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
        if(not rect.error):
            if(self.pos[0] < x):
                x -= 2
            else:
                x += 2
            y = rect.getY(x)
            self.place(x=x, y=y, anchor="center")
            if(x != self.pos[0]):
                self.root.after(5, self.animation, x, y, rect)
                #self.animation(x, y, rect)

    def move(self, p2):
        self.pos = p2
        if(not self.eventAnimation.is_set()):
            self.eventAnimation.set()


    
    

