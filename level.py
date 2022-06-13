import random
import pygame
import shroom
import player
from pygame.sprite import RenderUpdates

r1 = 140      #hold center location of the row
r2 = 240
r3 = 340
r4 = 440
r5 = 540
end = 170

class Level():
    def __init__(self, levelNum, mushNumber, timeLimit, startTime):
        self.mushNumber = mushNumber
        self.timeLimit = timeLimit
        self.levelNum = levelNum
        self.listShroom = []       #holds all the shrooms
        self.timeRemaining = timeLimit
        self.startTime = startTime
        self.completed = False

        self.listShroom = [shroom.Shrooms(5, 600, r1, 64, 64, end)]       #holds all the shrooms

    def timerCountdown(self):
        seconds = (pygame.time.get_ticks() - self.startTime)/1000      #calculates how many seconds
        if(seconds > self.timeLimit):
            self.completed = True

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
