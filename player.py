import dragon

r1 = 90      #by beginning corner
r2 = 190
r3 = 290
r4 = 390
r5 = 490

c1 = 200 
c2 = 300
c3 = 420
c4 = 560
c5 = 660

class Player:
    def __init__(self, grilled=5, lives=5, current_level=1, drags=0):
        self.grilled = grilled
        self.lives = lives
        self.current_level = current_level
        self.drags = drags
        self.mapDrags = []
 
        self.mapDrags = [dragon.Dragon(10, c1, r1, 76, 72, 1, 1), dragon.Dragon(4, c4, r2, 76, 72, 2, 4)]    #need change width and height

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



