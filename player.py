
import dragon
import pygame
from Buttons import imageButton

puffsButton = pygame.image.load('./images/dragon/dragonPlaceholder.png')     #button images
puffsButtonBig = pygame.image.load('./images/dragon/anyaBig.png')
removeReg = pygame.image.load('./images/dragon/removeButton.png')
removeBig = pygame.image.load('./images/dragon/removeButtonBig.png')

class Player:
    def __init__(self, grilled=20, lives=5, current_level=1, drags=0):
        self.grilled = grilled
        self.lives = lives
        self.current_level = current_level
        self.drags = drags
        self.mapDrags = []
        self.grid = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]
        self.shopButtons = [shopButton(puffsButton, puffsButtonBig, 92, 120, 1), shopButton(puffsButton, puffsButtonBig, 92, 220, 2), shopButton(puffsButton, puffsButtonBig, 92, 320, 3), shopButton(puffsButton, puffsButtonBig, 92, 420, 4), shopButton(puffsButton, puffsButtonBig, 92, 520, 5), shopButton(removeReg, removeBig, 500, 45, 6)]  #change the remove one
        self.selecting = False
        self.shoppingNum = 0
        self.buffing = False
        self.costs = [4, 2, 10, 8, 8, -1]  #puffs, kaboomo, snailey, pebble, lani


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
                self.grid[dragons.row][dragons.col] = 0
                self.mapDrags.remove(dragons)

    def gameOverChecker(self):
        if self.lives <= 0:
            return True
        return False

    def contains(self, row, col):
        for drag in self.mapDrags:
            if(drag.row == row and drag.col == col):
                return drag
        return None

    def rowCol(self, x, y):
        if(x >= 180 and x <= 299):
            col = 0
        elif(x <= 419):
            col = 1
        elif(x <= 539):
            col = 2 
        elif(x <= 659):
            col = 3
        else:
            col = 4

        if(y >= 80 and y <= 179):
            row = 0
        elif(y <= 279):
            row = 1
        elif(y <= 379):
            row = 2
        elif(y <= 479):
            row = 3
        else:
            row = 4
        return row,col

    def shop(self, x, y, cost):
        row, col = self.rowCol(x,y)
        if cost == -1:
            for drago in self.mapDrags:
                if drago.row == row and drago.col == col:
                    self.selecting = False
                    self.mapDrags.remove(drago)
                    self.grid[row][col] = 0
                    self.grilled += int(drago.cost/2)
                    return

        elif self.selecting and self.grid[row][col] == 0:
            self.buy(cost)
            if self.shoppingNum == 1:
                self.mapDrags.append(dragon.Puffs(row, col, 120, 72, cost))
            elif self.shoppingNum == 2:
                self.mapDrags.append(dragon.Kaboomo(row, col, 76, 72, cost))
            elif self.shoppingNum == 3:
                self.mapDrags.append(dragon.Snailey(row, col, 120, 72, cost))
            elif self.shoppingNum == 4:
                self.mapDrags.append(dragon.Pebble(row, col, 120, 72, cost))
            elif self.shoppingNum == 5:
                self.mapDrags.append(dragon.Lani(row, col, 120, 60, cost))
            self.selecting = False
            self.grid[row][col] = 1

        self.selecting = False

    def buff(self, x, y):
        row, col = self.rowCol(x,y)
        buffDrag = self.contains(row, col)
        if(buffDrag != 0):
            buffDrag.skill()
            self.buffing = False
            return True
        self.buffing = False
        return False

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

