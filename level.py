import random
import shroom
import time

r1 = 115      #hold center location of the row
r2 = 215
r3 = 315
r4 = 415
r5 = 515
end = 150

class Level():
    def __init__(self, levelNum, mushNumber, timeLimit):
        self.mushNumber = mushNumber
        self.timeLimit = timeLimit
        self.levelNum = levelNum
        self.listShroom = []       #holds all the shrooms
        self.timeRemaining = timeLimit
        self.startTime = 0
        self.completed = False
        self.shroomDrops = []


        self.shroomDrops= [shroom.droppedShroom(500,500)]
        self.listShroom = [shroom.Shrooms(5, 800, r1, 64, 64, end, 1), shroom.Shrooms(5, 800, r2, 64, 64, end, 2), shroom.Shrooms(5, 800, r3, 64, 64, end, 3), shroom.Shrooms(5, 800, r4, 64, 64, end, 4), shroom.Shrooms(5, 800, r5, 64, 64, end, 5)]       #holds all the shrooms

    def doneChecker(self):
        if(self.timeRemaining <= 0 and len(self.listShroom) == 0):
            self.completed = True
            return True
        return False

    def timerMinSec(self):
        secsPast = int((time.time() - self.startTime))
        self.timeRemaining = self.timeLimit - secsPast
        if(self.timeRemaining <= 0):
            return "0:00"
        timeRemaining = self.timeLimit - secsPast
        minRemaining = int(timeRemaining / 60)
        secRemaining = int(timeRemaining - minRemaining*60)
        if(secRemaining < 10):
            return str(minRemaining) + ":0" + str(secRemaining)
        return str(minRemaining) + ":" + str(secRemaining)

    def spawn(self):
        spawnRow = random.randint(1,6)
        if spawnRow == 1:
            mush = shroom.Shrooms(5, 800, r1, 77, 54, end)
        elif spawnRow == 2:
            mush = shroom.Shrooms(5, 800, r2, 77, 54, end)
        elif spawnRow == 3:
            mush = shroom.Shrooms(5, 800, r3, 77, 54, end)
        elif spawnRow == 4:
            mush = shroom.Shrooms(5, 800, r4, 77, 54, end)
        else:
            mush = shroom.Shrooms(5, 800, r5, 77, 54, end)
        self.listShroom.append(mush)
    
    def removeShroom(self, player1):    #via death or reach end of map
        for shroomo in self.listShroom:
            if shroomo.hp <= 0:
                self.shroomDrops.append(shroom.droppedShroom(shroomo.x + 20, shroomo.y + 40))
                self.listShroom.remove(shroomo)
            elif shroomo.x <= end + 1:
                self.listShroom.remove(shroomo)
                player1.loseLife()
    def removeShroomDrop(self, grilled):
        self.shroomDrops.remove(grilled)
