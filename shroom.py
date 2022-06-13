import player
import pygame
#import main

class Shrooms(object):
    walkLeft = [pygame.image.load("mushroom1.png"), pygame.image.load("mushroom2.png"), pygame.image.load("mushroom1.png"), pygame.image.load("mushroom4.png")]
    #to make a shroom = Shrooms(5, 100, 410, 64, 64, 450)
    def __init__(self, hp, x, y, width, height, end):
        self.hp = hp
        self.x = x     #xy coordinates of shroom
        self.y = y    
        self.width = width        #of shroom 77x54
        self.height = height
        self.end = end
        self.path = [x, end]
        self.vel = -2      #moving left
        self.walkCount = 0    #for animation

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 28:
            self.walkCount = 0
        if self.vel != 0:
            win.blit(self.walkLeft[self.walkCount // 7], (self.x, self.y)) #change 10 dependent on number of sprites = 3*numSprites
            self.walkCount = self.walkCount + 1
        else:
            win.blit(self.walkLeft[0], (self.x, self.y))
        self.walkCount += 1

    def move(self):    #need to add if collide with a draggo
        if self.x + self.vel > self.path[1]:
            self.x += self.vel
        else:
            self.vel = 0     #reach end of map, need life decrease