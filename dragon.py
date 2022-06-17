import pygame
import time

class Fireball(object):
    animation = [pygame.image.load('./images/dragon/fireball1.png'), pygame.image.load('./images/dragon/fireball2.png'), pygame.image.load('./images/dragon/fireball3.png'), pygame.image.load('./images/dragon/fireball4.png')]
    def __init__(self, x, y, width, height, row):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.row = row
        self.vel = 2
        self.end = 800
        self.path = [x, 800]
        self.animationCount = 0
    
    def fireballAttack(shroom):
        shroom.loseHp()
    
    def move(self):
        if self.x < self.path[1] + self.vel: # If we have not reached the furthest right point on our path.
            self.x += self.vel
        else:
            self.vel = 0

    def draw(self, win):
        self.move()
        if self.animationCount + 1 >= 160:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        if self.vel != 0:
            win.blit(self.animation[self.animationCount // 40], (self.x, self.y)) #x
            self.animationCount = self.animationCount + 1
        else:
            win.blit(self.animation[0], (self.x, self.y))
        self.animationCount += 1

class Dragon(object):
    def __init__(self, x, y, width, height, row, col):
        self.x = x     
        self.y = y    
        self.width = width        #of dragon- bounds 120 x 100
        self.height = height
        self.row = row
        self.col = col
        self.attacking = False

    def attackChecker(self, level):    #edit to fit drag
        if len(level.listShroom) == 0:
            self.attacking = False
        else:
            for shroom in level.listShroom:
                if(shroom.row == self.row):
                    self.attacking = True
                    return shroom
            self.attacking = False

    def loseLife(self):
        self.hp = self.hp - 1

    def defeatedCheck(self):
        if self.hp <= 0:
            return True
        return False

class Puffs(Dragon):    #fireball drag
    chilling = [pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs2.png'),pygame.image.load('./images/dragon/puffs3.png'),pygame.image.load('./images/dragon/puffs4.png'),pygame.image.load('./images/dragon/puffs4.png'),
    pygame.image.load('./images/dragon/puffs3.png'), pygame.image.load('./images/dragon/puffs2.png'),]
    #15frames
    def __init__(self, x, y, width, height, row, col):
        self.hp = 10
        self.fireballs = []
        self.lastAttackTime = 0
        self.animationCount = 0
        Dragon.__init__(self, x, y, width, height, row, col)
    
    def fireballSpawn(self, level):
        if (int((time.time() - level.startTime)) - self.lastAttackTime) > 1 and self.hp > 0:       #set time delay here, change the 1
            self.fireballs.append(Fireball(self.x + 85, self.y + 50, 25, 19, self.row))
            self.lastAttackTime = int((time.time() - level.startTime))
            return 

    def draw(self, win):
        if self.animationCount + 1 >= 525:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        win.blit(self.chilling[self.animationCount // 35], (self.x, self.y)) #x
        self.animationCount = self.animationCount + 1
        self.animationCount += 1
        for fireball in self.fireballs:
            fireball.draw(win)

    def attack(self, level, shroom):
        if self.attacking:
            self.fireballSpawn(level)
            for fireball in self.fireballs:
                if(shroom != None):
                    if(fireball.x < shroom.x + 10 and fireball.x > shroom.x - 10 and fireball.row == shroom.row):
                        shroom.loseHp()
                        self.fireballs.remove(fireball)

class Kaboomo(Dragon):    #suicide draggo
    flyAnimation = [pygame.image.load('./images/dragon/kaboomo1.png'), pygame.image.load('./images/dragon/kaboomo2.png'), pygame.image.load('./images/dragon/kaboomo3.png'), pygame.image.load('./images/dragon/kaboomo2.png'), pygame.image.load('./images/dragon/kaboomo5.png')]
    def __init__(self, x, y, width, height, row, col):
        self.hp = 3
        self.animationCount = 0
        Dragon.__init__(self, x, y, width, height, row, col)
        self.attacking = True

    def draw(self, win):
        if self.animationCount + 1 >= 125:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        win.blit(self.flyAnimation[self.animationCount // 25], (self.x, self.y)) #x
        self.animationCount = self.animationCount + 1
        self.animationCount += 1

    def attack(self, level, shroom):
        if self.attacking:
            if((self.x + self.width - 5) == shroom.x and self.row == shroom.row):
                shroom.hp = 0
                self.hp = 0
