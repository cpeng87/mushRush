import pygame
import time
from Buttons import imageButton

class Shrooms(object):
    walkLeft = [pygame.image.load("./images/shroom/mushroom1.png"), pygame.image.load("./images/shroom/mushroom2.png"), pygame.image.load("./images/shroom/mushroom1.png"), pygame.image.load("./images/shroom/mushroom4.png")]
    m1 = pygame.image.load("./images/shroom/mushAttack1.png")
    m2 = pygame.image.load("./images/shroom/mushAttack2.png")
    m3 = pygame.image.load("./images/shroom/mushAttack3.png")
    m4 = pygame.image.load("./images/shroom/mushAttack4.png")
    m5 = pygame.image.load("./images/shroom/mushAttack5.png")
    m6 = pygame.image.load("./images/shroom/mushAttack6.png")
    mushAttack = [m1,m1,m1,m1,m1,m1,m1,m1,m2,m3,m3,m4,m5,m6,m4,m3,m3,m2]
    #^18sprites 

    #to make a shroom = Shrooms(5, 100, 410, 64, 64, 450)
    def __init__(self, hp, x, y, width, height, row):
        self.hp = hp
        self.x = x     #xy coordinates of shroom
        self.y = y    
        self.width = width        #of shroom 77x54
        self.height = height
        self.end = 150
        self.path = [x, self.end]
        self.vel = -0.25      #moving left 0.25
        self.walkCount = 0    #for animation
        self.row = row
        self.attacking = False
        self.lastAttackTime = 0     #at what second did the last attack occur
        self.attackCount = 0
        self.target = None
        self.aniMultiWalk = 30

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= self.aniMultiWalk * 4:    #x*numSprites, x is how many times a frame is played
            self.walkCount = 0
        if self.attackCount + 1 >= 126:
            self.attackCount = 0
        if self.vel != 0:
            win.blit(self.walkLeft[self.walkCount // self.aniMultiWalk], (self.x, self.y)) #x
            self.walkCount = self.walkCount + 1
        elif self.attacking:
            win.blit(self.mushAttack[self.attackCount // 7], (self.x - 12, self.y -35))
            self.attackCount = self.attackCount + 1
        else:
            win.blit(self.walkLeft[0], (self.x, self.y))
        self.walkCount += 1

    def move(self):    #need to add if collide with a draggo
        if self.x + self.vel > self.path[1]:
            self.x += self.vel
        else:
            self.vel = 0     #reach end of map, need life decrease

    def loseHp(self):
        self.hp = self.hp - 1

    def attackPlayer(self, player1):
        player1.loseLife()

    def attackDrag(self, dragon, level):
        if dragon != None and dragon.hp > 0:
            if (int((time.time() - level.startTime)) - self.lastAttackTime) > 1:       #set time delay here, change the 1
                dragon.loseLife()
                self.lastAttackTime = int((time.time() - level.startTime))
        else:
            self.vel = -0.25
            self.attacking = False

    def collisionWithDrag(self, player1):
        for dragon in player1.mapDrags:
            if((dragon.x + 10) < self.x and (dragon.x + dragon.width - 5) > self.x and dragon.row == self.row):
                self.vel = 0
                self.attacking = True
                self.target = dragon
                return dragon
                

class droppedShroom(imageButton):
    def __init__(self, x, y):
        grilledShroom = pygame.image.load('./images/shroom/shiitake.png')
        grilledShroomBig = pygame.image.load('./images/shroom/shiitakeBig.png')
        imageButton.__init__(self, grilledShroom, grilledShroomBig, x, y)

    def update(self, mouse_pos, mouse_up, player1, level):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                player1.collectShroom()
                level.removeShroomDrop(self)
        else:
            self.mouse_over = False
