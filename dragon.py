import pygame
import time

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
    fireballAnimation = [pygame.image.load('./images/dragon/fireball1.png'), pygame.image.load('./images/dragon/fireball2.png'), pygame.image.load('./images/dragon/fireball3.png'), pygame.image.load('./images/dragon/fireball4.png')]
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
        if self.animationCount + 1 >= 160:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        if self.vel != 0:
            win.blit(self.fireballAnimation[self.animationCount // 40], (self.x, self.y)) #x
            self.animationCount = self.animationCount + 1
        else:
            win.blit(self.fireballAnimation[0], (self.x, self.y))
        self.animationCount += 1

class Iceball(Projectile):
    iceballAnimation = [pygame.image.load('./images/dragon/ice1.png'), pygame.image.load('./images/dragon/ice2.png'), pygame.image.load('./images/dragon/ice3.png')]
    def __init__(self, x, y, width, height, row):
        self.vel = 2
        self.animationCount = 0
        Projectile.__init__(self, x, y, width, height, row)
    
    def iceballAttack(self, shroom):
        if(self.x < shroom.x + 10 and self.x > shroom.x - 10 and self.row == shroom.row):
            shroom.loseHp()
            shroom.vel = -0.13
            shroom.aniMultiWalk = 40
            return True

    def draw(self, win):
        self.move()
        if self.animationCount + 1 >= 120:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        if self.vel != 0:
            win.blit(self.iceballAnimation[self.animationCount // 40], (self.x, self.y - 15)) #x
            self.animationCount = self.animationCount + 1
        else:
            win.blit(self.iceballAnimation[0], (self.x, self.y - 15))
        self.animationCount += 1

class Laser(Projectile):
    laserAnimation= [pygame.image.load('./images/dragon/laserStill.png')]    #need actual animation later
    def __init__(self, x, y, width, height, row, level):
        self.vel = 0
        self.startTime = time.time()
        self.lastAttackTime = 0
        self.level = level
        Projectile.__init__(self, x, y, width, height, row)

    def laserAttack(self, shroom):
        if shroom != None and shroom.hp > 0:
            if(int(((time.time() - self.startTime)) - self.lastAttackTime) * 10) > 5:
                for otherShroom in self.level.listShroom:
                    if otherShroom.x >= shroom.x and otherShroom.row == shroom.row:
                        otherShroom.loseHp()
                shroom.loseHp()
                self.lastAttackTime = int((time.time() - self.startTime))
    def draw(self, win):
        win.blit(self.laserAnimation[0], (self.x, self.y - 15))

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
    chilling = [pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs2.png'),pygame.image.load('./images/dragon/puffs3.png'),pygame.image.load('./images/dragon/puffs4.png'),pygame.image.load('./images/dragon/puffs4.png'),
    pygame.image.load('./images/dragon/puffs3.png'), pygame.image.load('./images/dragon/puffs2.png'),]
    #15frames
    def __init__(self, row, col, width, height, cost):
        self.hp = 10
        self.fireballs = []
        self.lastAttackTime = 0
        self.animationCount = 0
        self.fireballCd = 1
        Dragon.__init__(self, row, col, width, height, cost)
    
    def fireballSpawn(self, level):
        if (int((time.time() - level.startTime)) - self.lastAttackTime) > self.fireballCd and self.hp > 0:       #set time delay here, change the 1
            self.fireballs.append(Fireball(self.x + 85, self.y + 50, 25, 19, self.row))
            self.lastAttackTime = int((time.time() - level.startTime))
            return self.fireballs[0]

    def draw(self, win):
        if self.animationCount + 1 >= 450:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        win.blit(self.chilling[self.animationCount // 30], (self.x, self.y)) #x
        self.animationCount = self.animationCount + 1
        self.animationCount += 1
        for fireball in self.fireballs:
            fireball.draw(win)

    def attack(self, level, shroom):
        if self.attacking:
            self.fireballSpawn(level)
            for fireball in self.fireballs:
                if(shroom != None):
                    if(fireball.fireballAttack(shroom)):
                        self.fireballs.remove(fireball)

class Kaboomo(Dragon):    #suicide draggo
    flyAni = [pygame.image.load('./images/dragon/kaboomo1.png'), pygame.image.load('./images/dragon/kaboomo2.png'), pygame.image.load('./images/dragon/kaboomo3.png'), pygame.image.load('./images/dragon/kaboomo2.png'), pygame.image.load('./images/dragon/kaboomo5.png')]
    explodeAni = [pygame.image.load('./images/dragon/explode1.png'), pygame.image.load('./images/dragon/explode2.png'), pygame.image.load('./images/dragon/explode3.png'), pygame.image.load('./images/dragon/explode4.png'), pygame.image.load('./images/dragon/explode5.png'), pygame.image.load('./images/dragon/explode6.png'), pygame.image.load('./images/dragon/explode7.png'), ]
    #^7 frames
    def __init__(self, row, col, width, height, cost):
        self.hp = 1000
        self.animationCount = 0
        Dragon.__init__(self, row, col, width, height, cost)
        self.attacking = False

    def draw(self, win):
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
                    shroom.hp = 0
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
    
    #def skill(self): #increase radius of attack

class Snailey(Dragon):    #lazer go brrr
    s1 = pygame.image.load('./images/dragon/snailey1.png')
    s2 = pygame.image.load('./images/dragon/snailey2.png')
    s3 = pygame.image.load('./images/dragon/snailey3.png')
    s4 = pygame.image.load('./images/dragon/snailey4.png')
    chilling = [s1,s1,s1,s1,s1,s1,s2,s3,s4,s4,s4,s4,s4,s3,s2]
    #15 frames
    def __init__(self, row, col, width, height, cost):
        self.hp = 10
        self.animationCount = 0
        self.lazering = False
        self.laser = None
        self.laserStop = 0
        Dragon.__init__(self, row, col, width, height, cost)

    def draw(self, win):
        if self.animationCount + 1 >= 450:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        win.blit(self.chilling[self.animationCount // 30], (self.x, self.y + 5)) #x
        self.animationCount = self.animationCount + 1
        self.animationCount += 1
        if self.laser != None:
            self.laser.draw(win)

    def attack(self, level, firstShroom):          #i hate this method but its fine
        if self.attacking:
            if self.laser == None and int(time.time() - self.laserStop) > 3:    #change cd of laser
                self.laserStart = time.time()   #fix timer
                self.laser = self.laserSpawn(firstShroom.row, level)
                self.lazering = True
            if self.laser != None:
                if (int((time.time() - self.laser.startTime)) > 1 and self.hp > 0):   #laser lasts for 4 sec
                    self.lazering == False
                    self.laser = None
                    self.laserStop = time.time()     #time when the laser stops
            if self.laser != None:
                self.laser.laserAttack(firstShroom)
                if(firstShroom == None or firstShroom.hp == 0):
                    self.laser = None

    def laserSpawn(self, row, level):
        self.laser = Laser(self.x + 120, self.y + 30, 800 - self.x + 95, 50, row, level)
        return self.laser

    #def skill():    slow with longer laser duration

class Pebble(Dragon):     #tanky tank is tanky
    chill = pygame.image.load('./images/dragon/pebble.png')
    def __init__(self, row, col, width, height, cost):
        self.hp = 3
        Dragon.__init__(self, row, col, width, height, cost)
        self.attacking = False

    def draw(self, win):
        win.blit(self.chill, (self.x, self.y))

    #def skill(self.win):   no damage taken

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
        Dragon.__init__(self, row, col, width, height, cost)
    
    def iceballSpawn(self, level):
        if (int((time.time() - level.startTime)) - self.lastAttackTime) > 1 and self.hp > 0:       #set time delay here, change the 1
            self.iceballs.append(Iceball(self.x + 85, self.y + 50, 25, 19, self.row))
            self.lastAttackTime = int((time.time() - level.startTime))
            return self.iceballs[0]

    def draw(self, win):
        if self.animationCount + 1 >= 330:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        win.blit(self.chilling[self.animationCount // 30], (self.x, self.y)) #x
        self.animationCount = self.animationCount + 1
        self.animationCount += 1
        for iceball in self.iceballs:
            iceball.draw(win)

    def attack(self, level, shroom):
        if self.attacking:
            self.iceballSpawn(level)
            for iceball in self.iceballs:
                if(shroom != None):
                    if(iceball.iceballAttack(shroom)):
                        self.iceballs.remove(iceball)

    #def skill(self, level, shroom):   stop in place for 1s

