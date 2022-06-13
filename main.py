import pygame
import pygame.freetype
from pygame.locals import *
from enum import Enum

import player
from level import Level
import shroom
import drawer
import gameState as gs

#variables
levelNum = 1
time = 60
mushNum = 20

levels = [Level(levelNum, mushNum, time, 0), Level(levelNum, mushNum, time, 0)]
currentLevel = levels[0]

pygame.init()

background_color = (215, 224, 209)  # change to title screen later
white = (255, 255, 255)
icon = pygame.image.load("shroom.png")
titleBg = pygame.image.load("bgPlaceholder.jpg")  # need replace 700 x 450
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
        start_ticks = pygame.time.get_ticks()
        currentLevel.startTime = start_ticks
        game_state = drawer.level(screen, player1, currentLevel)

    if game_state == gs.GameState.NEXT_LEVEL:
        levelNum += 1
        mushNum += 20
        time += 30
        start_ticks = pygame.time.get_ticks()
        currentLevel = levels[levelNum - 1]
        game_state = gs.GameState.LEVEL

    if game_state == gs.GameState.GAME_OVER:
        game_state = drawer.gameOver(screen, player1)

    if game_state == gs.GameState.QUIT:
        pygame.quit()
