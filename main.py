import pygame
import pygame.freetype
from pygame.locals import *

import player
from level import Level
import drawer
import gameState as gs

#variables
levelNum = 1
timer = 20        #level time limit in seconds
mushNum = 20

levels = [Level(levelNum, mushNum, timer), Level(levelNum, mushNum, timer)]
currentLevel = levels[0]

pygame.init()

background_color = (215, 224, 209)  # change to title screen later
white = (255, 255, 255)
icon = pygame.image.load("./images/shroomIcon.png")
titleBg = pygame.image.load("./images/bgs/bgPlaceholder.jpg")  # need replace 700 x 450
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((800, 600))  # pix size of screen length x height
pygame.display.set_caption("guns go pew pew")
game_state = gs.GameState.TITLE
running = True

# main game logic loop
# takes care of the state machine in the game
# handles the transitions between states and calling the correct drawing method
while running:
    screen.blit(titleBg, (0, 0))
    if game_state == gs.GameState.TITLE:
        game_state = drawer.title_screen(screen)

    if game_state == gs.GameState.NEWGAME:
        player1 = player.Player()
        game_state = drawer.instruction(screen, player1)

    if game_state == gs.GameState.INSTRUCTION:
        game_state = drawer.instruction(screen, player1)

    if game_state == gs.GameState.LEVEL:
        game_state = drawer.level(screen, player1, currentLevel)

    if game_state == gs.GameState.NEXT_LEVEL:
        levelNum += 1
        mushNum += 20
        timer += 30
        currentLevel = levels[levelNum - 1]
        game_state = gs.GameState.LEVEL

    if game_state == gs.GameState.GAME_OVER:
        game_state = drawer.gameOver(screen, player1)

    if game_state == gs.GameState.QUIT:
        pygame.quit()
