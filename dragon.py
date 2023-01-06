import pygame
import time

from shroom import ninjaShroom

rowPix = [75,175,275,375,475]
colPix = [180,300,420,540,660]

class Projectile(object):
    def __init__(self, x, y, width, height, row):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.row = row
        self.path = [x, 800]

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
            win.blit(self.animation[self.animationCount // self.multiplier], (self.x, self.y)) #x
            self.animationCount = self.animationCount + 1
        else:
            win.blit(self.animation[0], (self.x, self.y))
        self.animationCount += 1

class Fireball(Projectile):
    fireballAnimation = [pygame.image.load('./images/dragon/fireball1.png'),
        pygame.image.load('./images/dragon/fireball2.png'),
        pygame.image.load('./images/dragon/fireball3.png'),
        pygame.image.load('./images/dragon/fireball4.png')]
    def __init__(self, x, y, width, height, row):
        self.vel = 2
        self.animationCount = 0
        Projectile.__init__(self, x, y, width, height, row)
    
    def fireballAttack(self, shroom):
        if(self.x < shroom.x + 10 and self.x > shroom.x - 10 and self.row == shroom.row):
            shroom.loseHp()
            return True

    def draw(self, win):
        self.move()
        if self.animationCount + 1 >= 80:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        if self.vel != 0:
            win.blit(self.fireballAnimation[self.animationCount // 20], (self.x, self.y)) #x
            self.animationCount = self.animationCount + 1
        else:
            win.blit(self.fireballAnimation[0], (self.x, self.y))
        self.animationCount += 1

class Iceball(Projectile):
    iceballAnimation = [pygame.image.load('./images/dragon/iceball1.png'),
        pygame.image.load('./images/dragon/iceball2.png'),
        pygame.image.load('./images/dragon/iceball3.png'),
        pygame.image.load('./images/dragon/iceball2.png')]
    def __init__(self, x, y, width, height, row):
        self.vel = 2
        self.animationCount = 0
        self.freezeTime = 0
        Projectile.__init__(self, x, y, width, height, row)
    
    def iceballAttack(self, shroom):
        if(self.x < shroom.x + 10 and self.x > shroom.x - 10 and self.row == shroom.row):
            shroom.loseHp()
            if shroom.frozen == False:
                shroom.vel = 0
                shroom.miniFreeze = True
                shroom.freezeTime = time.time()
            return True
        # elif shroom.frozen == True and int((time.time() - self.freezeTime)) > 1:
        #     shroom.frozen = False
        #     shroom.vel = -0.25
        #     self.freezeTime = 0

    def draw(self, win):
        self.move()
        if self.animationCount + 1 >= 60:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        if self.vel != 0:
            win.blit(self.iceballAnimation[self.animationCount // 20], (self.x, self.y - 15)) #x
            self.animationCount = self.animationCount + 1
        else:
            win.blit(self.iceballAnimation[0], (self.x, self.y - 15))
        self.animationCount += 1

class Laser(Projectile):
    laserAnimation = [pygame.image.load('./images/dragon/laserStill.png')]    #need actual animation later
    def __init__(self, x, y, width, height, row, level):
        self.vel = 0
        self.startTime = time.time()
        self.lastAttackTime = 0
        self.level = level
        Projectile.__init__(self, x, y, width, height, row)

    def laserAttack(self, shroom):
        if shroom != None and shroom.hp > 0:
            if(int(((time.time() - self.startTime)) - self.lastAttackTime) * 10) > 5: #passes this if statement
                for otherShroom in self.level.listShroom:
                    if otherShroom.x >= shroom.x and otherShroom.row == shroom.row:
                        otherShroom.loseHp()
                shroom.loseHp()
                self.lastAttackTime = int((time.time() - self.startTime))

    def draw(self, win):
        win.blit(self.laserAnimation[0], (self.x, self.y - 10))

class RedLaser(Laser):
    redLaserAnimation = [pygame.image.load('./images/dragon/laserStillRed.png')]
    redLaserAnimationr0 = [pygame.image.load('./images/dragon/laserStillRed0.png')]
    def __init__(self, x, y, width, height, row, level):
        self.hitRows = []
        if row == 0:
            self.hitRows = [0, 1]
        elif row == 5:
            self.hitRows = [5, 4]
        else:
            self.hitRows = [row - 1, row, row + 1]
        Laser.__init__(self, x, y, width, height, row, level)

    def laserAttack(self, shroom):
        if(int(((time.time() - self.startTime)) - self.lastAttackTime) * 10) > 5:
            for otherShroom in self.level.listShroom:
                if otherShroom.x >= self.x and otherShroom.row in self.hitRows:
                    otherShroom.loseHp()
            self.lastAttackTime = int((time.time() - self.startTime))

    def draw(self, win):
        if self.row == 0:
            win.blit(self.redLaserAnimationr0[0], (self.x, self.y - 90))
        else:
            win.blit(self.redLaserAnimation[0], (self.x, self.y - 90))

class Dragon(object):
    def __init__(self, row, col, width, height, cost):
        self.x = colPix[col]     
        self.y = rowPix[row] 
        self.width = width        #of dragon- bounds 120 x 100
        self.height = height
        self.row = row
        self.col = col
        self.attacking = False
        self.cost = cost
        self.skill = False
        self.skillStart = -1

    def attackChecker(self, level):    #edit to fit drag
        if len(level.listShroom) == 0:
            self.attacking = False
        else:
            rtnShroom = None
            minx = 801
            for shroom in level.listShroom:
                if(shroom.row == self.row and shroom.x < minx):
                    minx = shroom.x
                    rtnShroom = shroom
            if rtnShroom != None:
                self.attacking = True
                return rtnShroom
            self.attacking = False

    def loseLife(self):
        self.hp = self.hp - 1

    def defeatedCheck(self):
        if self.hp <= 0:
            return True
        return False

    def attack(self, level, shroom):
        return

class Puffs(Dragon):    #fireball drag
    puffs1 = pygame.image.load('./images/dragon/puffs1.png')
    puffs2 = pygame.image.load('./images/dragon/puffs2.png')
    puffs3 = pygame.image.load('./images/dragon/puffs3.png')
    puffs4 = pygame.image.load('./images/dragon/puffs4.png')
    #15frames
    def __init__(self, row, col, width, height, cost):
        self.hp = 10
        self.fireballs = []
        self.lastAttackTime = 0
        self.animationCount = 0
        self.fireballCd = 150
        Dragon.__init__(self, row, col, width, height, cost)
    
    def fireballSpawn(self, level):
        if (int((time.time() - level.startTime) * 100) - self.lastAttackTime) > self.fireballCd and self.hp > 0:       #set time delay here, change the 1
            self.fireballs.append(Fireball(self.x + 85, self.y + 50, 25, 19, self.row))
            self.lastAttackTime = int((time.time() - level.startTime) * 100)
            self.launching = True
            return self.fireballs[0]
        else:
            self.launching = False

    def draw(self, win, level):
        timeTicker = int((time.time() - level.startTime) * 100) - self.lastAttackTime
        if timeTicker > self.fireballCd - 10 and timeTicker < self.fireballCd + 10:   # attack anim
            win.blit(self.puffs4, (self.x, self.y))
        elif timeTicker > self.fireballCd - 20 and timeTicker < self.fireballCd + 20: #puff 3
            win.blit(self.puffs3, (self.x, self.y))
        elif timeTicker > self.fireballCd - 30 and timeTicker < self.fireballCd + 30: #puff 2
            win.blit(self.puffs2, (self.x, self.y))
        else:
            win.blit(self.puffs1, (self.x, self.y))
        # if self.animationCount + 1 >= 450:    #x*numSprites, x is how many times a frame is played
        #     self.animationCount = 0
        # win.blit(self.chilling[self.animationCount // 30], (self.x, self.y)) #x
        # self.animationCount = self.animationCount + 1
        # self.animationCount += 1
        for fireball in self.fireballs:
            fireball.draw(win)

    def attack(self, level, shroom):
        if self.attacking:
            self.fireballSpawn(level)
            for fireball in self.fireballs:
                if(shroom != None):
                    if(fireball.fireballAttack(shroom)):
                        self.fireballs.remove(fireball)
    def skillUp(self, level):
        if self.skill and self.skillStart == -1:
            self.fireballCd = 75
            self.skillStart = time.time()
        elif int((time.time() - self.skillStart)) > 5: 
            self.skill = False
            self.skillStart = -1
            self.fireballCd = 150
            
class Kaboomo(Dragon):    #suicide draggo
    flyAni = [pygame.image.load('./images/dragon/kaboomo1.png'), pygame.image.load('./images/dragon/kaboomo2.png'), pygame.image.load('./images/dragon/kaboomo3.png'), pygame.image.load('./images/dragon/kaboomo2.png'), pygame.image.load('./images/dragon/kaboomo5.png')]
    explodeAni = [pygame.image.load('./images/dragon/explode1.png'), pygame.image.load('./images/dragon/explode2.png'), pygame.image.load('./images/dragon/explode3.png'), pygame.image.load('./images/dragon/explode4.png'), pygame.image.load('./images/dragon/explode5.png'), pygame.image.load('./images/dragon/explode6.png'), pygame.image.load('./images/dragon/explode7.png'), ]
    #^7 frames
    def __init__(self, row, col, width, height, cost):
        self.hp = 1000
        self.animationCount = 0
        Dragon.__init__(self, row, col, width, height, cost)
        self.attacking = False

    def draw(self, win, level):
        if self.attacking == False:
            if self.animationCount + 1 >= 125:    #x*numSprites, x is how many times a frame is played
                self.animationCount = 0
            win.blit(self.flyAni[self.animationCount // 25], (self.x, self.y)) #x
            self.animationCount = self.animationCount + 1
            self.animationCount += 1
        else:
            if self.animationCount + 1 >= 175:    #x*numSprites, x is how many times a frame is played
                self.hp = 0
            win.blit(self.explodeAni[self.animationCount // 25], (self.x, self.y)) #x
            self.animationCount = self.animationCount + 1
            self.animationCount += 1

    def attack(self, level, triggerShroom):
        if self.attacking and triggerShroom != None:
            for shroom in level.listShroom:
                if shroom.x < self.x - 100 and self.x > triggerShroom.x + 100:
                    shroom.hp -= 5
            triggerShroom.hp = 0

    def attackChecker(self, level):
        if self.hp < 1000:
            self.attacking = True
            for shroom in level.listShroom:
                if shroom.target == self:
                    return shroom

    def loseLife(self):
        if self.hp == 1000:
            self.animationCount = 0
            self.hp -= 1

    def skillUp(self, level):
        return

class Snailey(Dragon):    #lazer go brrr
    s1 = pygame.image.load('./images/dragon/snailey1.png')
    s2 = pygame.image.load('./images/dragon/snailey2.png')
    s3 = pygame.image.load('./images/dragon/snailey3.png')
    s4 = pygame.image.load('./images/dragon/snailey4.png')
    #15 frames
    def __init__(self, row, col, width, height, cost):
        self.hp = 10
        self.animationCount = 0
        self.laser = None
        self.laserStop = 0
        Dragon.__init__(self, row, col, width, height, cost)

    def draw(self, win, level):
        timeTicker = int(time.time() - self.laserStop)
        if self.laser != None:   # attack anim
            win.blit(self.s4, (self.x, self.y))
        # elif self.laser == None and timeTicker > 4 and timeTicker < 6:  #puff 3
        #     win.blit(self.s3, (self.x, self.y))
        elif self.laser == None and timeTicker > 5 and timeTicker < 7: #puff 2
            win.blit(self.s2, (self.x, self.y))
        else:
            win.blit(self.s1, (self.x, self.y))

        # if self.animationCount + 1 >= 450:    #x*numSprites, x is how many times a frame is played
        #     self.animationCount = 0
        # win.blit(self.chilling[self.animationCount // 30], (self.x, self.y + 5)) #x
        # self.animationCount = self.animationCount + 1
        # self.animationCount += 1
        if self.laser != None:
            self.laser.draw(win)

    def attack(self, level, firstShroom):          #i hate this method but its fine
        if self.skill:
            if isinstance(self.laser, RedLaser) == False or self.laser == None:
                self.laserSpawn(level)
                self.laserStart = time.time()
        if self.attacking:
            if self.laser == None and int(time.time() - self.laserStop) > 5:    #change cd of laser
                self.laserStart = time.time()   #fix timer
                self.laserSpawn(level)
            elif self.laser != None:
                if (int((time.time() - self.laserStart)) > 2 or self.hp <= 0):   #laser duration
                    self.laser = None
                    self.laserStop = time.time()     #time when the laser stops
        if self.laser != None:
            self.laser.laserAttack(firstShroom)

    def laserSpawn(self, level):
        if self.skill:
            self.laser = RedLaser(self.x + 120, self.y + 30, 800 - self.x + 95, 50, self.row, level)
        else:
            self.laser = Laser(self.x + 120, self.y + 30, 800 - self.x + 95, 50, self.row, level)

    def skillUp(self, level):
        if self.skill and self.skillStart == -1:
            self.laserLength = 10
            self.skillStart = time.time()
        elif int((time.time() - self.skillStart)) > 5 and self.skill:
            self.skill = False
            self.skillStart = -1
            self.laser = None

class Pebble(Dragon):     #tanky tank is tanky
    chill = pygame.image.load('./images/dragon/pebble.png')
    invulnerable = pygame.image.load('./images/dragon/pebbleInvul.png')
    def __init__(self, row, col, width, height, cost):
        self.hp = 15
        self.damageTaken = 1
        Dragon.__init__(self, row, col, width, height, cost)
        self.attacking = False

    def draw(self, win, level):
        if (self.damageTaken == 0):
            win.blit(self.invulnerable, (self.x, self.y))
        else:
            win.blit(self.chill, (self.x, self.y))

    def loseLife(self):
        self.hp = self.hp - self.damageTaken

    def skillUp(self, level):
        if self.skill and self.skillStart == -1:
            self.skillStart = time.time()
            self.damageTaken = 0
        elif int((time.time() - self.skillStart)) > 10:
            self.skill = False
            self.skillStart = -1
            self.damageTaken = 1

class Lani(Dragon):    #fireball drag
    l1 = pygame.image.load('./images/dragon/lani1.png')
    l2 = pygame.image.load('./images/dragon/lani2.png')
    l3 = pygame.image.load('./images/dragon/lani3.png')
    chilling = [l1,l1,l1,l1,l1,l1,l2,l3,l3,l3,l2,]
    #11frames
    def __init__(self, row, col, width, height, cost):
        self.hp = 10
        self.iceballs = []
        self.lastAttackTime = 0
        self.animationCount = 0
        self.timeTicker = -1
        Dragon.__init__(self, row, col, width, height, cost)
    
    def iceballSpawn(self, level):
        self.timeTicker = int((time.time() - level.startTime)) - self.lastAttackTime
        if (int((time.time() - level.startTime)) - self.lastAttackTime) > 2 and self.hp > 0:       #set time delay here, change the 1
            self.iceballs.append(Iceball(self.x + 85, self.y + 50, 25, 19, self.row))
            self.lastAttackTime = int((time.time() - level.startTime))
            return self.iceballs[0]

    def draw(self, win, level):
        if self.skill:
            win.blit(self.l3, (self.x, self.y))
            return
        if self.timeTicker > 0 and self.timeTicker < 4:   # attack anim
            win.blit(self.l1, (self.x, self.y))
        else:
            win.blit(self.l3, (self.x, self.y))

        # if self.animationCount + 1 >= 330:    #x*numSprites, x is how many times a frame is played
        #     self.animationCount = 0
        # if self.skill:
        #     win.blit(self.chilling[8], (self.x, self.y))
        # else:
        #     win.blit(self.chilling[self.animationCount // 30], (self.x, self.y)) #x
        # self.animationCount = self.animationCount + 1
        # self.animationCount += 1
        for iceball in self.iceballs:
            iceball.draw(win)

    def attack(self, level, shroom):
        if self.skill:
            return
        if self.attacking:
            self.iceballSpawn(level)
            for iceball in self.iceballs:
                if(shroom != None):
                    if(iceball.iceballAttack(shroom)):
                        self.iceballs.remove(iceball)

    def skillUp(self, level):
        if self.skill and self.skillStart == -1:
            self.skillStart = time.time()
            for shroom in level.listShroom:
                shroom.vel = 0
                shroom.frozen = True
        elif int((time.time() - self.skillStart)) > 3 and self.skill:     #3sec board freeze
            self.skill = False
            self.skillStart = -1
            for shroom in level.listShroom:
                if isinstance(shroom, ninjaShroom):
                    shroom.vel = 0     #this might make all the mushrooms pacifist
                else:
                    shroom.vel = -0.25
                shroom.frozen = False