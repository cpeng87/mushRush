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

class Laser(Projectile):
    laserAnimation= [pygame.image.load('./images/dragon/laserStill.png')]    #need actual animation later
    def __init__(self, x, y, width, height, row):
        self.vel = 0
        self.startTime = time.time()
        self.lastAttackTime = 0
        Projectile.__init__(self, x, y, width, height, row)

    def laserAttack(self, shroom):
        if shroom != None and shroom.hp > 0:
            if(int(((time.time() - self.startTime)) - self.lastAttackTime) * 10) > 5:
                shroom.loseHp()
                self.lastAttackTime = int((time.time() - self.startTime))
    def draw(self, win):
        win.blit(self.laserAnimation[0], (self.x, self.y))

class Dragon(object):
    def __init__(self, row, col, width, height):
        self.x = colPix[col - 1]     
        self.y = rowPix[row - 1] 
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

    def attack(self, level, shroom):
        return

class Puffs(Dragon):    #fireball drag
    chilling = [pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/puffs2.png'),pygame.image.load('./images/dragon/puffs3.png'),pygame.image.load('./images/dragon/puffs4.png'),pygame.image.load('./images/dragon/puffs4.png'),
    pygame.image.load('./images/dragon/puffs3.png'), pygame.image.load('./images/dragon/puffs2.png'),]
    #15frames
    def __init__(self, row, col, width, height):
        self.hp = 10
        self.fireballs = []
        self.lastAttackTime = 0
        self.animationCount = 0
        Dragon.__init__(self, row, col, width, height)
    
    def fireballSpawn(self, level):
        if (int((time.time() - level.startTime)) - self.lastAttackTime) > 1 and self.hp > 0:       #set time delay here, change the 1
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

class Snailey(Dragon):    #lazer go brrr
    chilling = [pygame.image.load('./images/dragon/snailey1.png'), pygame.image.load('./images/dragon/snailey1.png'), pygame.image.load('./images/dragon/snailey2.png'), pygame.image.load('./images/dragon/snailey1.png'), pygame.image.load('./images/dragon/snailey2.png'), pygame.image.load('./images/dragon/snailey1.png'), pygame.image.load('./images/dragon/snailey3.png'), 
    pygame.image.load('./images/dragon/snailey4.png'), pygame.image.load('./images/dragon/snailey5.png'), pygame.image.load('./images/dragon/snailey5.png'), pygame.image.load('./images/dragon/snailey5.png'), pygame.image.load('./images/dragon/snailey5.png'), pygame.image.load('./images/dragon/snailey5.png'), pygame.image.load('./images/dragon/snailey4.png'), pygame.image.load('./images/dragon/snailey3.png')]
    #15 frames
    def __init__(self, row, col, width, height):
        self.hp = 10
        self.animationCount = 0
        self.lazering = False
        self.laser = None
        self.laserStop = 0
        Dragon.__init__(self, row, col, width, height)

    def draw(self, win):
        if self.animationCount + 1 >= 450:    #x*numSprites, x is how many times a frame is played
            self.animationCount = 0
        win.blit(self.chilling[self.animationCount // 30], (self.x, self.y)) #x
        self.animationCount = self.animationCount + 1
        self.animationCount += 1
        if self.laser != None:
            self.laser.draw(win)

    def attack(self, level, firstShroom):          #i hate this method but its fine
        if self.attacking:
            if self.laser == None and int(time.time() - self.laserStop) > 1:
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
        self.laser = Laser(self.x + 120, self.y + 30, 800 - self.x + 95, 50, row)
        return self.laser


class Kaboomo(Dragon):    #suicide draggo
    flyAnimation = [pygame.image.load('./images/dragon/kaboomo1.png'), pygame.image.load('./images/dragon/kaboomo2.png'), pygame.image.load('./images/dragon/kaboomo3.png'), pygame.image.load('./images/dragon/kaboomo2.png'), pygame.image.load('./images/dragon/kaboomo5.png')]
    def __init__(self, row, col, width, height):
        self.hp = 3
        self.animationCount = 0
        Dragon.__init__(self, row, col, width, height)
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

class Pebble(Dragon):     #tanky tank is tanky
    chill = pygame.image.load('./images/dragon/pebble.png')
    def __init__(self, row, col, width, height):
        self.hp = 15
        Dragon.__init__(self, row, col, width, height)
        self.attacking = False

    def draw(self, win):
        win.blit(self.chill, (self.x, self.y))


