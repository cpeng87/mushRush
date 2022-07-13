import dragon
import pygame
from Buttons import imageButton

puffsButton = pygame.image.load('./images/dragon/puffs1.png')
puffsButtonBig = pygame.image.load('./images/dragon/anyaBig.png')
cursorImgs = [pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/kaboomo1.png'), pygame.image.load('./images/dragon/snailey1.png')]

class Player:
    def __init__(self, grilled=5, lives=5, current_level=1, drags=0):
        self.grilled = grilled
        self.lives = lives
        self.current_level = current_level
        self.drags = drags
        self.mapDrags = []
        self.shopButtons = [shopButton(puffsButton, puffsButtonBig, 92, 120, 1), shopButton(puffsButton, puffsButtonBig, 92, 220, 2)]
        self.selecting = False
        self.shoppingNum = 0

        self.mapDrags = [dragon.Puffs(1, 1, 120, 72), dragon.Puffs(2, 1, 120, 72), dragon.Puffs(3, 1, 120, 72), dragon.Puffs(4, 1, 120, 72), dragon.Kaboomo(2, 4, 76, 72), dragon.Snailey(5, 1, 120, 72), dragon.Pebble(3, 2, 110, 72)]    #need change width and height

    def buy(self, shroomCost):
        if self.drags >= 25:
            print("too many dragons on the field. they like their personal space")
        else:
            self.grilled = self.grilled - shroomCost

    def sell(self, dragCost):
        self.grilled = self.grilled + (dragCost / 2)

    def loseLife(self):
        self.lives = self.lives - 1

    def collectShroom(self):
        self.grilled = self.grilled + 1

    def removeDrag(self): 
        for dragons in self.mapDrags:
            if(dragons.defeatedCheck()):
                self.mapDrags.remove(dragons)

    def gameOverChecker(self):
        if self.lives <= 0:
            return True
        return False
    
    def shop(self, x, y):
        if(x >= 180 and x <= 299):
            col = 1
        elif(x >= 300 and x <= 419):
            col = 2        
        elif(x >= 420 and x <= 539):
            col = 3 
        elif(x >= 540 and x <= 659):
            col = 4
        else:
            col = 5

        if(y >= 80 and y <= 179):
            row = 1
        elif(y >= 180 and y <= 279):
            row = 2
        elif(y >= 280 and y <= 379):
            row = 3
        elif(y >= 380 and y <= 479):
            row = 4
        else:
            row = 5

        print(str(row) + ", " + str(col))

        if self.selecting:
            if self.shoppingNum == 1:
                if(self.grilled >= 4):    #change costs later
                    self.buy(4)
                    self.mapDrags.append(dragon.Puffs(row, col, 120, 72))
                else:
                    self.selecting = False
            elif self.shoppingNum == 2:
                if(self.grilled >= 2):
                    self.buy(2)
                    self.mapDrags.append(dragon.Kaboomo(row, col, 76, 72))
                else:
                    self.selecting = False

class shopButton(imageButton):
    def __init__(self, regPic, bigPic, x, y, dragNum):
        self.dragNum = dragNum
        imageButton.__init__(self, regPic, bigPic, x, y)

    def update(self, mouse_pos, mouse_up, player1):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                    player1.selecting = True
                    player1.shoppingNum = self.dragNum
        else:
            self.mouse_over = False


