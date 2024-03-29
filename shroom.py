import pygame
import time
from Buttons import imageButton
import random

class Shrooms(object):
    walkLeft = [pygame.image.load("./images/shroom/mushroom1.png"), pygame.image.load("./images/shroom/mushroom2.png"), pygame.image.load("./images/shroom/mushroom1.png"), pygame.image.load("./images/shroom/mushroom4.png")]
    m1 = pygame.image.load("./images/shroom/mushAttack1.png")
    m2 = pygame.image.load("./images/shroom/mushAttack2.png")
    m3 = pygame.image.load("./images/shroom/mushAttack3.png")
    m4 = pygame.image.load("./images/shroom/mushAttack4.png")
    m5 = pygame.image.load("./images/shroom/mushAttack5.png")
    m6 = pygame.image.load("./images/shroom/mushAttack6.png")
    mushAttack = [m1,m1,m1,m1,m1,m1,m1,m1,m2,m3,m3,m4,m5,m6,m4,m3,m3,m2]
    mushFreeze = pygame.image.load("./images/shroom/mushroomFroze.png")
    #^18sprites 

    #to make a shroom = Shrooms(5, 100, 410, 64, 64, 450)
    def __init__(self, x, y, width, height, row):
        self.hp = 8
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
        self.frozen = False
        self.miniFreeze = False
        self.freezeTime = -1

    def draw(self, win):
        self.move()
        if self.frozen or self.miniFreeze:
            win.blit(self.mushFreeze, (self.x, self.y))
            return
        if self.walkCount + 1 >= self.aniMultiWalk * 4:    #x*numSprites, x is how many times a frame is played
            self.walkCount = 0
        if self.attackCount + 1 >= 126:
            self.attackCount = 0
        if self.vel != 0:
            win.blit(self.walkLeft[self.walkCount // self.aniMultiWalk], (self.x, self.y)) #x
            self.walkCount = self.walkCount + 1
            return
        elif self.attacking:
            win.blit(self.mushAttack[self.attackCount // 7], (self.x - 12, self.y -35))
            self.attackCount = self.attackCount + 1
        else:
            self.vel = -0.25
        self.walkCount += 1

    def move(self):
        if self.miniFreeze == True and int((time.time() - self.freezeTime) * 100) > 50:
            self.miniFreeze = False
            self.vel = -0.25
        if self.x + self.vel > self.path[1]:
            self.x += self.vel
        else:
            self.vel = 0     #reach end of map, need life decrease

    def loseHp(self):
        self.hp = self.hp - 1

    def attackPlayer(self, player1):
        player1.loseLife()

    def attackDrag(self, dragon, level):
        if self.frozen or self.miniFreeze:
            return
        elif dragon != None and dragon.hp > 0:
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

class special(Shrooms):
    def __init__(self, x, y, width, height, row):
        Shrooms.__init__(self, x, y, width, height, row)

# class bigBoy(special):
#     bigWalkLeft = [pygame.image.load("./images/shroom/bigBoy1.png")]
#     def __init__(self, x, y, width, height, row):
#         self.hp = 4
#         self.cap = bigBoy2(x, y - 100, width, height, row - 1)
#         self.vel = -0.15
#         Shrooms.__init__(self, x, y, width, height, row)

#     def draw(self, win):
#         print("big boy his here!")
#         print(self.hp)
#         self.move()
#         self.update()
#         win.blit(self.bigWalkLeft[0], (self.x, self.y - 125))

#     def loseHp(self):
#         self.hp -= 1

#     def update(self):
#         if self.cap.hp != 1000:
#             self.hp -= 1000 - self.cap.hp

# class bigBoy2(Shrooms):
#     def __init__(self, x, y, width, height, row):
#         self.hp = 1000
#         Shrooms.__init__(self, x, y, width, height, row)

#     def draw(self, win):
#         print("i have a hat")
#         return

#     def loseHp(self):
#         print("MYHAT!!")
#         self.hp -= 1

# class Sparky(special):
#     sparkyWalkLeft = [pygame.image.load("./images/shroom/sparky1.png"), pygame.image.load("./images/shroom/sparky2.png"), pygame.image.load("./images/shroom/sparky1.png"), pygame.image.load("./images/shroom/sparky4.png"),]
#     s1 = pygame.image.load("./images/shroom/sparky1.png")
#     s2 = pygame.image.load("./images/shroom/sparkyAttack2.png")
#     s3 = pygame.image.load("./images/shroom/sparkyAttack3.png")
#     s4 = pygame.image.load("./images/shroom/sparkyAttack4.png")
#     sparkyAttack = [s1,s1,s1,s1,s1,s1,s2,s3,s4,s3,s4,s3,s2]
#     sparkyRing = pygame.image.load("./images/shroom/sparkyRing.png")
#     #^^^^13frames

#     def __init__(self, x, y, width, height, row):
#         self.hp = 5
#         self.targetArr = []
#         Shrooms.__init__(self, x, y, width, height, row)
    
#     def draw(self, win):
#         self.move()
#         if self.walkCount + 1 >= self.aniMultiWalk * 4:    #x*numSprites, x is how many times a frame is played
#             self.walkCount = 0
#         if self.attackCount + 1 >= 91:
#             self.attackCount = 0
#         if self.vel != 0:
#             win.blit(self.sparkyWalkLeft[self.walkCount // self.aniMultiWalk], (self.x, self.y - 35)) #x
#             self.walkCount = self.walkCount + 1
#         elif self.attacking:
#             win.blit(self.sparkyAttack[self.attackCount // 7], (self.x-5, self.y -35))
#             self.attackCount = self.attackCount + 1
#         else:
#             win.blit(self.sparkyWalkLeft[0], (self.x, self.y - 35))
#         self.walkCount += 1

#     def move(self):    #need to add if collide with a draggo
#         if self.x + self.vel > self.path[1]:
#             self.x += self.vel
#         else:
#             self.vel = 0     #reach end of map, need life decrease

#     def attackDrag(self, dragon, level):
#         if self.frozen:
#             return
#         if dragon != None and dragon.hp > 0:
#             if (int((time.time() - level.startTime)) - self.lastAttackTime) > 2:       #set time delay here, change the 1
#                 dragon.loseLife()     #attacks all drags in a row once collided
#                 print("YOUVE BEEN zAPPED")
#                 self.lastAttackTime = int((time.time() - level.startTime))
#         else:
#             self.vel = -0.25
#             self.attacking = False
#             self.targetArr = []

#     def collisionWithDrag(self, player1):
#         print("detecting")
#         #if self.attacking and len(self.targetArr) == 0:
#             #for dragon in player1.mapDrags:
                
#         for dragon in player1.mapDrags:
#             if(dragon.row == self.row):
#                 self.targetArr.append(dragon)
#                 if((dragon.x + 10) < self.x and (dragon.x + dragon.width - 5) > self.x):
#                     self.vel = 0
#                     self.attacking = True
#                     self.target = dragon
#                     return dragon
                
class disguisedShroom(special):
    disWalkLeft = [pygame.image.load("./images/shroom/disguisedShroom1.png"), pygame.image.load("./images/shroom/disguisedShroom2.png"), pygame.image.load("./images/shroom/disguisedShroom1.png"), pygame.image.load("./images/shroom/disguisedShroom4.png")]
    disFreeze = pygame.image.load("./images/shroom/disguisedShroomFroze.png")
    undisFreeze = pygame.image.load("./images/shroom/mushroomFroze.png")
    def __init__(self, x, y, width, height, row):
        self.disguised = True
        self.hp = 20
        Shrooms.__init__(self, x, y, width, height, row)

    def attackDrag(self, dragon, level):
        if self.frozen:
            return
        if dragon != None and dragon.hp > 0:
            if (int((time.time() - level.startTime)) - self.lastAttackTime) > 1:       #set time delay here, change the 1
                dragon.loseLife()
                self.lastAttackTime = int((time.time() - level.startTime))
        else:
            self.attacking = False

    def collisionWithDrag(self, player1):
        for dragon in player1.mapDrags:
            if self.disguised:
                if((dragon.x + 10) < self.x and (dragon.x + dragon.width - 5) > self.x and dragon.row == self.row):
                    if self.x < dragon.x + 11:    
                        self.disguised = False
            else:
                if((dragon.x + 11) < self.x and (dragon.x + dragon.width - 5) > self.x and dragon.row == self.row):
                    self.vel = 0
                    self.attacking = True
                    self.target = dragon
                    return dragon

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= self.aniMultiWalk * 4:    #x*numSprites, x is how many times a frame is played
            self.walkCount = 0
        if self.attackCount + 1 >= 126:
            self.attackCount = 0
        if self.disguised:
            if self.frozen or self.miniFreeze:
                win.blit(self.disFreeze, (self.x, self.y))
            elif self.vel != 0:
                win.blit(self.disWalkLeft[self.walkCount // self.aniMultiWalk], (self.x, self.y)) #x
                self.walkCount = self.walkCount + 1
            else:
                self.vel = -0.25
            self.walkCount += 1
        else:
            if self.frozen or self.miniFreeze:
                win.blit(self.undisFreeze, (self.x, self.y))
            elif self.vel != 0:
                win.blit(self.walkLeft[self.walkCount // self.aniMultiWalk], (self.x, self.y)) #x
                self.walkCount = self.walkCount + 1
            elif self.attacking:
                win.blit(self.mushAttack[self.attackCount // 7], (self.x - 12, self.y -35))
                self.attackCount = self.attackCount + 1
            else:
                self.vel = -0.25
            self.walkCount += 1

class ninjaShroom(special):    #it still attacks after it has been manually removed haha, need new method
    t1= pygame.image.load("./images/shroom/ninjaShroomTele1.png")
    t2 = pygame.image.load("./images/shroom/ninjaShroomTele2.png")
    t3 = pygame.image.load("./images/shroom/ninjaShroomTele3.png")   #resting
    ninjaTele = [t1,t2,t3,t3,t3,t3,t3]
    #^ origin: 7
    ns1 = pygame.image.load("./images/shroom/ninjaShroomCombo1.png")
    ns2 = pygame.image.load("./images/shroom/ninjaShroomCombo2.png")
    ns3 = pygame.image.load("./images/shroom/ninjaShroomCombo3.png")
    #^4 + 7 = 11 frames
    ninjaSlash = [ns1,ns2,ns3,t3,t3,t3,t3,t3,t3,t3,t3]
    
    ninjaFreeze = pygame.image.load("./images/shroom/ninjaShroomFroze.png")
    def __init__(self, x, y, width, height, row):
        self.hp = 10
        self.vel = 0
        self.teleporting = True
        self.teleCount = 0
        self.teleFactor = 10
        self.target = None
        self.final = 0
        Shrooms.__init__(self, x, y, width, height, row)

    def collisionWithDrag(self, player1):
        if self.target not in player1.mapDrags:
            self.teleporting = True
            self.target = None
        if self.teleporting:   #probs causes the glitching in the beginning
            if len(player1.mapDrags) == 0 and self.target == None:     #player attack
                self.move()
                self.attackPlayer()
                return None
            elif self.target == None or self.target not in player1.mapDrags:    #no target, now randomize new one
                rand = random.randint(0, len(player1.mapDrags) - 1)
                newTarget = player1.mapDrags[rand]
                self.target = newTarget
                self.move()
                return newTarget
        else:     #in front of drag and attack it
            if(self.x == self.target.x + 86 and self.row):
                self.vel = 0
                self.attacking = True

    def move(self):
        #rando and tele
        if self.x == 152:  #do nothing
            return
        elif self.target == None:    #start timer for final attack
            self.x = 152
            self.final = time.time()
        elif self.target.x + 86 != self.x or self.target.y != self.y:    #autual teleport
            self.x = self.target.x + 86
            self.row = self.target.row
            self.y = self.target.y + 10

    def draw(self, win):
        if self.frozen:
            win.blit(self.ninjaFreeze, (self.x, self.y))
            return
        elif self.teleporting:
            if self.teleCount + 1 >= 7 * self.teleFactor:
                self.teleCount = 0
                self.teleporting = False
            win.blit(self.ninjaTele[self.teleCount // self.teleFactor], (self.x - 50, self.y))
            self.teleCount += 1
            return
        if self.attackCount + 1 >= 77:
            self.attackCount = 0
        elif self.attacking:
            win.blit(self.ninjaSlash[self.attackCount // 7], (self.x - 50, self.y))
            self.attackCount = self.attackCount + 1
        else:
            win.blit(self.t3, (self.x, self.y))
            self.attacking = True
        self.walkCount += 1

    def attackDrag(self, dragon, level):
        if self.frozen:
            return
        if self.target == None:
            self.attacking = False
            self.teleporting = True
        elif self.target.hp == 1:
            self.target.loseLife()
            self.attacking = False
            self.teleporting = True
            self.target = None
        elif self.target != None and self.target.hp > 0:
            if(int((time.time() - level.startTime)) - self.lastAttackTime) > 1:
                self.target.loseLife()
                self.lastAttackTime = int((time.time() - level.startTime))
        else:
            self.attacking = False
            self.teleporting = True
            self.target = None

    def attackPlayer(self):
        if(int((time.time() - self.final) * 10)) >= 7:
            self.x = 148

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

class specialShroom(imageButton):
    def __init__(self, x, y):
        specialShroom = pygame.image.load('./images/shroom/specialMush.png')
        specialShroomBig = pygame.image.load('./images/shroom/specialMushBig.png')
        imageButton.__init__(self, specialShroom, specialShroomBig, x, y)

    def update(self, mouse_pos, mouse_up, player1, level):   #currently producing infinite mushrooms
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                player1.buffing = True
                player1.usingShroom = self
                level.removeShroomDrop(self)
        else:
            self.mouse_over = False