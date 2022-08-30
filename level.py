import random
import shroom
import time

rowPix = [105,205,305,405,505]
end = 150

class Level():
    def __init__(self, levelNum, mushNum, timeLimit):
        self.mushNum = mushNum
        self.timeLimit = timeLimit
        self.levelNum = levelNum
        self.listShroom = [shroom.disguisedShroom(10, 800, rowPix[0], 77, 54, 0), shroom.ninjaShroom(10, 800, rowPix[1], 77, 54, 1)]       #holds all the shrooms
        self.timeRemaining = timeLimit
        self.startTime = 0
        self.completed = False
        self.shroomDrops = []
        self.paused = False
        self.pauseStart = 0
        self.pauseTime = 0
        self.spawnTime = [60, 59, 58]
        self.coolShrooms = []  #

        self.shroomDrops= [shroom.droppedShroom(500,500)]

        while(mushNum > 0):   #change spawn array, possibly hard code?
           self.spawnTime.append(random.randint(0, self.timeLimit))
           mushNum -= 1

    def doneChecker(self):
        if(self.timeRemaining <= 0 and len(self.listShroom) == 0):
            self.completed = True
            return True
        return False

    def unpause(self):
        secsPaused = int((time.time() - self.pauseStart))
        self.pauseTime += secsPaused

    def timerMinSec(self):
        secsPast = int((time.time() - self.startTime))
        self.timeRemaining = self.timeLimit - secsPast
        if(self.timeRemaining <= 0):
            return "0:00"
        timeRemaining = self.timeLimit - secsPast + self.pauseTime
        minRemaining = int(timeRemaining / 60)
        secRemaining = int(timeRemaining - minRemaining*60)
        if(secRemaining < 10):
            return str(minRemaining) + ":0" + str(secRemaining)
        return str(minRemaining) + ":" + str(secRemaining)

    def mushSpawn(self):
        for time in self.spawnTime:
            if(self.timeRemaining == time):
                spawnRow = random.randint(0,4)
                mush = shroom.Shrooms(5, 800, rowPix[spawnRow], 77, 54, spawnRow)  #last is spawnrow
                self.spawnTime.remove(time)
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

