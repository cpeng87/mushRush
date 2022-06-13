import pygame
import pygame.freetype
from pygame.locals import *
import player
import menu
import level
import shroom

pygame.init()

background_color = (215,224,209)     #change to title screen later
white = (255, 255, 255)
icon = pygame.image.load('shroom.png')
titleBg = pygame.image.load('bgPlaceholder.jpg')     #need replace 700 x 450
pygame.display.set_icon(icon)
    
screen = pygame.display.set_mode((800, 600))    #pix size of screen length x height
pygame.display.set_caption('guns go pew pew')
game_state = menu.GameState.TITLE
running = True

levelNum = 1
time = 60
mushNum = 20

def redrawGameWindow():     #need import screen or say where it from
    global walkCount

    screen.blit(bg, (0,0))
    if walkCount + 1 >= 12:
        walkCount = 0
    if(shroom.vel != 0):
        screen.blit(shroom.walkRight[walkCount//3], (shroom.x, shroom.y))
        walkCount = walkCount + 1
    else:
        screen.blit(shroom.walkRight[0], shroom.x, shroom.y)

    pygame.display.update()

while running:
    screen.blit(titleBg, (0,0))
    if game_state == menu.GameState.TITLE:
        game_state = menu.title_screen(screen)
        
    if game_state == menu.GameState.NEWGAME:
        player1 = player.Player()
        game_state = menu.instruction(screen,player1)

    if game_state == menu.GameState.INSTRUCTION:
        game_state = menu.instruction(screen, player1)

    if game_state == menu.GameState.LEVEL:
        start_ticks = pygame.time.get_ticks()
        level1 = level.Level(levelNum, mushNum, time, start_ticks)
        game_state = menu.levelTime(screen, player1)
        redrawGameWindow()

    if game_state == menu.GameState.NEXT_LEVEL:
        levelNum += 1
        mushNum += 20
        time += 30
        start_ticks = pygame.time.get_ticks()
        nextLevel = level.Level(levelNum, mushNum, time, start_ticks)
        game_state = menu.levelTime(screen, player1)

    if game_state == menu.GameState.GAME_OVER:
        game_state = menu.gameOver(screen, player1)

    if game_state == menu.GameState.QUIT:
        pygame.quit()


