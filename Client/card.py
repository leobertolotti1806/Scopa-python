from customtkinter import CTkLabel
from config import *
#import client
import threading
from animation import Rect
import time

semaphore = threading.Semaphore()

stopAnimations = threading.Event()
stop = []

class Card(CTkLabel):

    def __init__(
            self,
            value,
            pos,
            size,
            space, # hand1 (1) / hand2 (2) / table (3)
            root : customtkinter.CTk,
            onclick = None,
            **args
        ):
        image = Image.open(f"media/cards/{value}.png")
        super().__init__(**args, image=customtkinter.CTkImage(image, size=size))
        self.root = root
        self.pos = pos
        self.value = value
        self.img = image
        self.size = size
        self.space = space
        self.stopCard = False
        self.closedCard = threading.Event()
        self.eventAnimation = threading.Event()

        self.waitBeforeAnimation = 0
        if(onclick != None):
            self.bind("<Button-1>", lambda event, e=self: onclick(e))
        self.place(x=self.pos[0], y=self.pos[1], anchor="center")
        self.render = threading.Thread(target=self.waitAnimation)
        self.render.start()

    def waitAnimation(self):
        while True:
            x = round(self.pos[0])
            y = round(self.pos[1])
            sizeX = self.size[0]
            value = self.value
            print(Back.WHITE + Fore.BLUE + f"{self.value}:" + Fore.BLACK + " sono pronto a partire" + Back.BLACK + Fore.WHITE, end="\n")

            #if(self.waitStop):
                # faccio partire lo stopper che entra in un loop che aspetta si svuoti il vettore stop
                # e poi breakka il ciclo
                #self.stopper()
            self.eventAnimation.wait()
            if(self.stopCard):
                self.closedCard.set()
                break

            print(Back.LIGHTBLACK_EX + Fore.BLUE + f"{self.value}:" + Fore.BLACK + " animazione verso" + Fore.GREEN + f" {x};{y}" + Fore.WHITE +" partita" + Back.BLACK + Fore.WHITE, end="\n")

            #eventStartAnimation.set()

            semaphore.acquire()
            stop.append(True)
            semaphore.release()

            if(self.waitBeforeAnimation != 0):
                time.sleep(self.waitBeforeAnimation)
                self.waitBeforeAnimation = 0

            if(value != self.value):
                self.img = Image.open(f"media/cards/{self.value}.png")

            if(sizeX != self.size):
                image = customtkinter.CTkImage(self.img, size=self.size)
                self.configure(image=image)

            self.animation(x, y, Rect((x, y), self.pos))
            self.eventAnimation.clear()

            # aspetto che waitAnimations mi dia il via per fare uno stop
            semaphore.acquire()
            stop.remove(True)
            semaphore.release()
            # aspetto che nessuno stia gestendo già un controllo di stop
            # PROVA 1 #sendStop.wait()
            # ora scateno un evento in modo tale che tutti coloro che aspettavano di partire se stop[] è vuoto possono farlo
            # PROVA 1 # eventContinueAnimation.set()
            self.checkStop()
            #self.waitStop = False
            # in sostanza io non posso iniziare la prossima animazione se non ho stoppato quella precedente

    def animation(self, x, y, rect : Rect):
        print(Back.CYAN + Fore.BLUE + f"{self.value}:" + Fore.WHITE + f" ha iniziato a percorrere la retta:" + Fore.GREEN + f" y = {rect.m}x + {rect.q}" + Fore.WHITE + Back.BLACK, end="\n")
        if(not rect.error):
            index = 0
            posX = round(self.pos[0])
            posY = round(self.pos[1])
            while x != posX:
                #print(x)
                index += 1
                if(not rect.imp):
                    if(posX < x):
                        x -= 1
                    else:
                        x += 1
                    y = rect.getY(x)
                else:
                    if(posY < y):
                        y -= 1
                    else:
                        y += 1

                self.place(x=x, y=y, anchor="center")
                #self._update_image()
                if(index == 2):
                    time.sleep(0.0025)
                    index = 0

    def move(self, p2, timeW = 0, size = "NaN", newValue=""):
        self.pos = p2
        if(newValue != ""):
            self.value = newValue
        if(size != "NaN"):
            self.size = size
        if(not self.eventAnimation.is_set()):
            self.waitBeforeAnimation = timeW
            self.eventAnimation.set()

    def checkStop(self):
        print(Fore.RED + "controllo la fine stop..." + Fore.WHITE)
        if(len(stop) == 0):
            print(Back.WHITE + Fore.BLUE + f"{self.value}:" + Back.BLACK + Fore.GREEN + " mando la fine stop" + Fore.WHITE)
            stopAnimations.set()

    def destroyCard(self):
        self.stopCard = True
        self.eventAnimation.set()
        self.closedCard.wait()
        self.destroy()

class HandSpace:

    def __init__(
        self,
        root,
        master,
        cards,
        size,
        player,
        pos,
        yStart,
        onclick
    ):
        self.root = root
        self.cards = []
        self.size = size
        self.player = player
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
                    size = self.size,
                    space = self.player,
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
                    size = self.size,
                    space = 3,
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
            
    def destroyPickedCards(self):
        if(len(stop) == 0):
            for i in self.rmCards:
                if(i):
                    i.destroyCard()
        

            
            


        


    
    

