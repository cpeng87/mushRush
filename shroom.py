import player
import pygame
import main

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
        self.vel = -3      #moving left
        self.walkCount = 0    #for animation

    def draw(self, win):
        self.move()
        if self.walkCount + 1 <= 12:      #change 10 dependent on number of sprites = 3*numSprites
            self.walkCount = 0
        main.screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
        self.walkCount += 1

    def move(self):    #need to add if collide with a draggo
        if self.x - self.vel > self.path[0]:
            self.x += self.vel
        else:
            self.vel = 0     #reach end of map, need life decrease