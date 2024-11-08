import threading
import sys
from time import *

class AnimationCard:

    thread = None
    card = None
    m = None
    q = None
    x = 0
    duration = 100,

    def __init__(self, card, p1, p2):
        self.card = card
        self.getMQ(p1, p2)

    def getMQ(self, p1, p2):
        self.m = (p1[0] - p2[1]) / (p1[1] - p2[1])
        self.q = p1[1] - (self.m * p1[0])

    def Start(self):
        self.thread = threading.Thread(target=self.Move, args=(self)).start()
        
    def Move():
        while True:
            sleep(10)

class AnimationText:

    index = 0
    stop = False
    thread = None

    def __init__(self, root, lbl, duration, frames):
        self.stop = False
        self.finish = [False]
        self.root = root
        self.lbl = lbl
        self.duration = duration
        self.frames = frames
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()

    def animate(self):
        if(self.stop == False):
            try:
                self.lbl.configure(text=self.frames[self.index])
            except:
                self.finish = [True]
                return
        self.index += 1
        if(self.index == len(self.frames)):
            self.index = 0
        if(self.stop == False):
            self.root.after(self.duration, self.animate)
        else:
            self.finish = [True]
            return

    def waitStop(self):
        self.stop = True
            
        
