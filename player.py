import dragon
import pygame

r1 = 75      #by beginning corner
r2 = 175
r3 = 275
r4 = 375
r5 = 475

c1 = 180 
c2 = 300
c3 = 420
c4 = 540
c5 = 660

class Player:
    def __init__(self, grilled=5, lives=5, current_level=1, drags=0):
        self.grilled = grilled
        self.lives = lives
        self.current_level = current_level
        self.drags = drags
        self.mapDrags = []
 
        self.mapDrags = [dragon.Puffs(c1, r1, 120, 72, 1, 1), dragon.Kaboomo(c4, r2, 76, 72, 2, 4)]    #need change width and height

    def buy(self, shroomCost):
        if self.drags >= 25:
            print("too many dragons on the field. they like their personal space")
        else:
            self.grilled = self.grilled - shroomCost

    def sell(self, dragCost):
        self.grilled = self.grilled + (dragCost / 2)

    def loseLife(self):
        self.lives = self.lives - 1

    def collectShroom(self):
        self.grilled = self.grilled + 1

    def removeDrag(self): 
        for dragons in self.mapDrags:
            if(dragons.defeatedCheck()):
                self.mapDrags.remove(dragons)

    def gameOverChecker(self):
        if self.lives <= 0:
            return True
        return False
    
    def shop(self, dragonNum):
        if dragonNum == 0:
            self.mapDrags.append(dragon.Puffs(c2, r2, 120, 72, 2, 2))   #change c1 and r1 and row = 1, col = 1 
        elif dragonNum == 1:
            self.mapDrags.append(dragon.Kaboomo(c2, r3, 76, 72, 3, 2))



