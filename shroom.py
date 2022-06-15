import pygame
import time

class Shrooms(object):
    walkLeft = [pygame.image.load("./images/shroom/mushroom1.png"), pygame.image.load("./images/shroom/mushroom2.png"), pygame.image.load("./images/shroom/mushroom1.png"), pygame.image.load("./images/shroom/mushroom4.png")]
    mushAttack = [pygame.image.load("./images/shroom/mushAttack1.png"),pygame.image.load("./images/shroom/mushAttack1.png"),pygame.image.load("./images/shroom/mushAttack1.png"),pygame.image.load("./images/shroom/mushAttack1.png"), pygame.image.load("./images/shroom/mushAttack1.png"), pygame.image.load("./images/shroom/mushAttack1.png"), pygame.image.load("./images/shroom/mushAttack1.png"), pygame.image.load("./images/shroom/mushAttack1.png"), pygame.image.load("./images/shroom/mushAttack2.png"), pygame.image.load("./images/shroom/mushAttack3.png"),
    pygame.image.load("./images/shroom/mushAttack3.png"), pygame.image.load("./images/shroom/mushAttack4.png"), pygame.image.load("./images/shroom/mushAttack5.png"), pygame.image.load("./images/shroom/mushAttack6.png"), pygame.image.load("./images/shroom/mushAttack4.png"), pygame.image.load("./images/shroom/mushAttack3.png"),
    pygame.image.load("./images/shroom/mushAttack3.png"), pygame.image.load("./images/shroom/mushAttack2.png"),]
    #^18sprites 

    #to make a shroom = Shrooms(5, 100, 410, 64, 64, 450)
    def __init__(self, hp, x, y, width, height, end, row):
        self.hp = hp
        self.x = x     #xy coordinates of shroom
        self.y = y    
        self.width = width        #of shroom 77x54
        self.height = height
        self.end = end
        self.path = [x, end]
        self.vel = -0.25      #moving left 0.25
        self.walkCount = 0    #for animation
        self.row = row
        self.attacking = False
        self.lastAttackTime = 0     #at what second did the last attack occur
        self.attackCount = 0

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 160:    #x*numSprites, x is how many times a frame is played
            self.walkCount = 0
        if self.attackCount + 1 >= 234:
            self.attackCount = 0
        if self.vel != 0:
            win.blit(self.walkLeft[self.walkCount // 40], (self.x, self.y)) #x
            self.walkCount = self.walkCount + 1
        elif self.attacking:
            win.blit(self.mushAttack[self.attackCount // 13], (self.x - 12, self.y -35))
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
        if dragon != None:
            if (int((time.time() - level.startTime)) - self.lastAttackTime) > 1 and dragon.hp > 0:       #set time delay here, change the 1
                dragon.loseLife()
                self.lastAttackTime = int((time.time() - level.startTime))
        else:
            self.vel = -0.25
            self.attacking = False

    def collisionWithDrag(self, player1):
        for dragon in player1.mapDrags:
            if((dragon.x + dragon.width - 5) == self.x and dragon.row == self.row):
                self.vel = 0
                self.attacking = True
                return dragon

class droppedShroom(object):
    def __init__(self, x, y):
        grilledShroom = pygame.image.load('./images/shroom/shiitake.png')
        grilledShroomBig = pygame.image.load('./images/shroom/shiitakeBig.png')
        self.mouse_over = False
        self.x = x
        self.y = y
        self.images = [grilledShroom, grilledShroomBig]
        self.rects = [grilledShroom.get_rect(center=(x,y)), grilledShroomBig.get_rect(center=(x,y)),]   #coordinates
        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]
    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up, player1, level):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                player1.collectShroom()
                level.removeShroomDrop(self)
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

