import threading
import sys
from time import *

class Rect:

    m = None
    q = None
    imp = False

    def __init__(self, p1, p2):
        self.error = False
        self.getMQ(p1, p2)

    def getMQ(self, p1, p2):
        self.error = False
        if(p1[0] - p2[0] != 0):
            eq = (p1[0] - p2[0])
            if eq != 0:
                self.m = (p1[1] - p2[1]) / eq
                self.q = p1[1] - (self.m * p1[0])
            else:
                self.imp = True
        else :
            self.error = True

    def getY(self, x):
        return (x * self.m) + self.q

class AnimationText:

    index = 0
    stop = False
    thread = None

    def __init__(self, root, lbl, duration, frames):
        self.closeAnimation = threading.Event()
        self.stop = False
        self.finish = [False]
        self.root = root
        self.lbl = lbl
        self.duration = duration
        self.frames = frames
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()

    def animate(self):
        if(self.stop):
            self.closeAnimation.set()
            return
        
        self.lbl.configure(text=self.frames[self.index])

        self.index += 1
        if(self.index == len(self.frames)):
            self.index = 0
        self.root.after(self.duration, self.animate)
        
    def stopAnimation(self):
        self.stop = True
        if(self.thread.is_alive()):
            self.closeAnimation.wait()
        self.closeAnimation.clear()
            
        
