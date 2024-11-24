import threading
import sys
from time import *

class Rect:

    m = None
    q = None

    def __init__(self, p1, p2):
        self.error = False
        self.getMQ(p1, p2)

    def getMQ(self, p1, p2):
        self.error = False
        if(p1[0] - p2[0] != 0):
            self.m = (p1[1] - p2[1]) / (p1[0] - p2[0])
            self.q = p1[1] - (self.m * p1[0])
        else :
            self.error = True

    def getY(self, x):
        return (x * self.m) + self.q

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
        else:
            #HO FATTO COME MI DICEVI NEL VIDEO
            #guarda commento riga 165 circa client.py e dimmi se
            #va bene oppure no
            try:
                self.lbl.configure(text="")
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
            
        
