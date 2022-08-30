import pygame
import pygame.freetype
from pygame.locals import *
import player
import level
import Buttons
from enum import Enum
import time

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    INSTRUCTION = 1
    LEVEL = 2
    PAUSE = 3
    GAME_OVER = 4
    WIN = 5

pygame.init()
white = (255,255,255)
icon = pygame.image.load("./images/shroomIcon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 600))  # pix size of screen length x height
pygame.display.set_caption("guns go pew pew")
gameState = GameState.TITLE
running = True

background_color = (192,134,105)      #change to title screen later
buttonColor = (117,153,138) #for level

titleBg = pygame.image.load('./images/bgs/titledragmush.png')      #need replace!!!!!!!!!!!
instructionBg = pygame.image.load('./images/bgs/instructionScreen.png')
levelBg = pygame.image.load('./images/bgs/dragonfield.png')
gameOverBg = pygame.image.load('./images/bgs/gameOverPlaceholder.jpg')

grilledShroom = pygame.image.load('./images/shroom/shiitake.png')
grilledShroomBig = pygame.image.load('./images/shroom/shiitakeBig.png')

cursorImgs = [pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/kaboomo1.png'), pygame.image.load('./images/dragon/snailey1.png'), pygame.image.load('./images/dragon/pebble.png'), pygame.image.load('./images/dragon/lani1.png'), pygame.image.load('./images/dragon/removeButton.png'),]
# main game logic loop
# takes care of the state machine in the game
# handles the transitions between states and calling the correct drawing method
clock = pygame.time.Clock()
while running:
    clock.tick(90)
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            click = True

    if gameState == GameState.TITLE:
        screen.blit(titleBg, (0, 0))
        level1 = level.Level(1, 10, 60)    #level, mush, time
        level2 = level.Level(1, 50, 90)    #level, mush, time
        level3 = level.Level(1, 70, 110)    #level, mush, time

        allLv = [level1, level2, level3]
        lvIndex = 0
        quitButton = Buttons.textButton(       
            center_position=(650, 550),
            font_size=25,
            bg_rgb=background_color,
            text_rgb= white,
            text="Quit",
            stateChange = GameState.QUIT,
        )
        startButton = Buttons.textButton(
            center_position=(650, 500),
            font_size=30,
            bg_rgb=background_color,
            text_rgb= white,
            text="Start",
            stateChange = GameState.INSTRUCTION,
        )
        titleButtons = [quitButton, startButton]
        for button in titleButtons:
            nextState = button.update(pygame.mouse.get_pos(), click)
            if nextState is not None:
                gameState = nextState
        for button in titleButtons:
            button.draw(screen)

    elif gameState == GameState.INSTRUCTION:
        player1 = player.Player()
        screen.blit(instructionBg, (0, 0))
        returnButton = Buttons.textButton(
            center_position=(150, 540),
            font_size=20,
            bg_rgb=background_color,
            text_rgb=white,
            text="Return to menu",
            stateChange = GameState.TITLE,
        )
        continueButton = Buttons.textButton(
            center_position=(650, 535),
            font_size=30,
            bg_rgb=background_color,
            text_rgb=white,
            text="Continue",
            stateChange = GameState.LEVEL,
        )
        instructionButtons = [returnButton, continueButton]
        for button in instructionButtons:
            nextState = button.update(pygame.mouse.get_pos(), click)
            if nextState is not None:
                if nextState == GameState.LEVEL:
                    allLv[lvIndex].startTime = time.time()
                gameState = nextState
        for button in instructionButtons:
            button.draw(screen)
    
    elif gameState == GameState.LEVEL:
        if(player1.gameOverChecker()):
            gameState = GameState.GAME_OVER

        elif(allLv[lvIndex].paused):
            screen.fill(background_color)
            pausedText = Buttons.displayText(       
                center_position=(400, 320),
                font_size=60,
                bg_rgb=background_color,
                text_rgb= white,
                text=f"Paused",
            )
            continueButton = Buttons.textButton(
                center_position= (400, 500),
                font_size=30,
                bg_rgb=background_color,
                text_rgb=white,
                text="Continue",
                stateChange = GameState.LEVEL
            )
            quitButton = Buttons.textButton(
                center_position= (400, 550),
                font_size=30,
                bg_rgb=background_color,
                text_rgb=white,
                text="Quit",
                stateChange = GameState.QUIT
            )
            pausedText.draw(screen)
            pauseButtons = [continueButton, quitButton]
            for button in pauseButtons:
                nextState = button.update(pygame.mouse.get_pos(), click)
                if nextState is not None:
                    gameState = nextState
                    if nextState == GameState.LEVEL:
                        allLv[lvIndex].unpause()
                        allLv[lvIndex].paused = False
            for button in pauseButtons:
                button.draw(screen)

        else:
            screen.blit(levelBg, (0, 0))
            #buttons and display
            pauseButton = Buttons.textButton(                       #change to restart later
                center_position= (600, 45),
                font_size=30,
                bg_rgb=buttonColor,
                text_rgb=white,
                text="Pause",
                stateChange = GameState.LEVEL
            )
            quitButton = Buttons.textButton(
                center_position= (715, 45),
                font_size=30,
                bg_rgb=buttonColor,
                text_rgb=white,
                text="Quit",
                stateChange = GameState.QUIT
            )

            lifeDisplay = Buttons.displayText(       
                center_position=(270, 45),
                font_size=30,
                bg_rgb=buttonColor,
                text_rgb= white,
                text=f"Lives: " + str(player1.lives),
                )
            timeDisplay = Buttons.displayText(       
                center_position=(400, 45),
                font_size=30,
                bg_rgb=buttonColor,
                text_rgb= white,
                text=allLv[lvIndex].timerMinSec(),         #replace with timer later
                )
            grilledDisplay = Buttons.displayText(       
                center_position=(110, 45),
                font_size=30,
                bg_rgb=buttonColor,
                text_rgb= white,
                text= ": " + str(player1.grilled),
                )
            levelDisplay = [lifeDisplay, timeDisplay, grilledDisplay]
            levelButtons = [pauseButton, quitButton,]
            for button in levelButtons:
                nextState = button.update(pygame.mouse.get_pos(), click)
                if nextState is not None:
                    gameState = nextState
                    if nextState == GameState.LEVEL:
                        allLv[lvIndex].paused = True
                        allLv[lvIndex].pauseStart = time.time()

            #spawn shroom
            allLv[lvIndex].mushSpawn()

            #cleaning dead things
            allLv[lvIndex].removeShroom(player1)
            player1.removeDrag()

            #select dragon space when shopping
            if player1.selecting and player1.grilled >= player1.costs[player1.shoppingNum - 1] and len(player1.mapDrags) < 25:
                pygame.mouse.set_visible(False)
                if click:
                    x,y = pygame.mouse.get_pos()
                    if x > 179 and x < 780 and y > 79 and y < 580 and player1.shoppingNum != 0:
                        player1.shop(x, y, player1.costs[player1.shoppingNum - 1])
                        pygame.mouse.set_visible(True)
                    else:
                        player1.selecting = False
                        pygame.mouse.set_visible(True)
            else:
                player1.selecting = False

            #drops and shops buttons update
            for grilled in allLv[lvIndex].shroomDrops:
                grilled.update(pygame.mouse.get_pos(), click, player1, allLv[lvIndex])
            for button in player1.shopButtons:                     #wah si spaget code
                button.update(pygame.mouse.get_pos(), click, player1)     
                button.draw(screen)

            #action and draw
            for text in levelDisplay:
                text.draw(screen)
            screen.blit(grilledShroom, (55, 30))    #for counter display

            for dragon in player1.mapDrags:
                shroomTarget = dragon.attackChecker(allLv[lvIndex])
                dragon.attack(allLv[lvIndex], shroomTarget)
                dragon.draw(screen)

            for button in levelButtons:
                button.draw(screen)

            for shroom in allLv[lvIndex].listShroom:
                dragonTarget = shroom.collisionWithDrag(player1)
                if shroom.attacking:
                    shroom.attackDrag(dragonTarget, allLv[lvIndex])
                shroom.draw(screen)

            for grilled in allLv[lvIndex].shroomDrops:
                grilled.draw(screen)

            if player1.selecting and player1.grilled >= player1.costs[player1.shoppingNum - 1] and len(player1.mapDrags) < 25:
                cursorRect = cursorImgs[player1.shoppingNum - 1].get_rect()
                cursorRect.center = pygame.mouse.get_pos()  # update position 
                screen.blit(cursorImgs[player1.shoppingNum - 1], cursorRect) #draw the cursor
            
            if(allLv[lvIndex].doneChecker()):
                nextLvButton = Buttons.textButton(
                center_position= (560, 550),
                font_size = 30,
                bg_rgb=buttonColor,
                text_rgb=white,
                text="Continue to next level",
                stateChange = GameState.LEVEL
                )
                nextState = nextLvButton.update(pygame.mouse.get_pos(), click)
                if lvIndex > len(allLv) - 2:
                    gameState = GameState.WIN

                nextLvButton.draw(screen)               #something weird, button still being drawn
                if nextState is not None:     #reseting values for next level
                    lvIndex = lvIndex + 1
                    allLv[lvIndex].startTime = time.time()
                    player1.mapDrags = []
                    player1.grilled = 20
                    player1.lives = 5
                    player1.selecting = False
                    player1.grid = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]

    elif gameState == GameState.GAME_OVER:
        screen.blit(gameOverBg, (0, 0))
        titleButton = Buttons.textButton(                 #change to restart later
            center_position= (400, 400),
            font_size=30,
            bg_rgb=buttonColor,
            text_rgb=white,
            text="Title",
            stateChange = GameState.TITLE
        )
        quitButton = Buttons.textButton(
            center_position= (400, 450),
            font_size=30,
            bg_rgb=buttonColor,
            text_rgb=white,
            text="Quit",
            stateChange = GameState.QUIT
        )
        gameOverButtons = [titleButton, quitButton]
        for button in gameOverButtons:
            nextState = button.update(pygame.mouse.get_pos(), click)
            if nextState is not None:
                gameState = nextState
        for button in gameOverButtons:
            button.draw(screen)

    elif gameState == GameState.WIN:
        screen.blit(titleBg, (0,0))
        winText = Buttons.displayText(       
            center_position=(400, 320),
            font_size=60,
            bg_rgb=background_color,
            text_rgb= white,
            text=f"You Win!",
        )
        titleButton = Buttons.textButton(
            center_position= (400, 500),
            font_size=30,
            bg_rgb=background_color,
            text_rgb=white,
            text="Title",
            stateChange = GameState.TITLE
        )
        quitButton = Buttons.textButton(
            center_position= (400, 550),
            font_size=30,
            bg_rgb=background_color,
            text_rgb=white,
            text="Quit",
            stateChange = GameState.QUIT
        )
        winText.draw(screen)
        winButtons = [titleButton, quitButton]
        for button in winButtons:
            nextState = button.update(pygame.mouse.get_pos(), click)
            if nextState is not None:
                gameState = nextState
        for button in winButtons:
            button.draw(screen)

    else:
        pygame.quit()

    pygame.display.flip()