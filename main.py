import pygame
import pygame.freetype
from pygame.locals import *
import player
import level
import Buttons
from enum import Enum

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    INSTRUCTION = 1
    LEVEL = 2
    PAUSE = 3
    GAME_OVER = 4

pygame.init()
white = (255, 255, 255)
icon = pygame.image.load("./images/shroomIcon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 600))  # pix size of screen length x height
pygame.display.set_caption("guns go pew pew")
gameState = GameState.TITLE
running = True

background_color = (215,224,209)      #change to title screen later
buttonColor = (117,153,138) #for level

titleBg = pygame.image.load('./images/bgs/bgPlaceholder.jpg')      #need replace!!!!!!!!!!!
instructionBg = pygame.image.load('./images/bgs/instructionScreen.png')
levelBg = pygame.image.load('./images/bgs/dragonfield.png')
gameOverBg = pygame.image.load('./images/bgs/gameOverPlaceholder.jpg')

grilledShroom = pygame.image.load('./images/shroom/shiitake.png')
grilledShroomBig = pygame.image.load('./images/shroom/shiitakeBig.png')

cursorImgs = [pygame.image.load('./images/dragon/puffs1.png'), pygame.image.load('./images/dragon/kaboomo1.png'), pygame.image.load('./images/dragon/snailey1.png')]
# main game logic loop
# takes care of the state machine in the game
# handles the transitions between states and calling the correct drawing method
while running:
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            click = True

    if gameState == GameState.TITLE:
        screen.blit(titleBg, (0, 0))
        level1 = level.Level(1, 20, 60)    #level, mush, time
        level2 = level.Level(1, 50, 90)    #level, mush, time
        level3 = level.Level(1, 70, 110)    #level, mush, time

        allLevels = [level1, level2, level3]
        levelIndex = 0
        quitButton = Buttons.textButton(       
            center_position=(650, 500),
            font_size=25,
            bg_rgb=background_color,
            text_rgb= white,
            text="Quit",
            stateChange = GameState.QUIT,
        )
        startButton = Buttons.textButton(
            center_position=(650, 450),
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

    if gameState == GameState.INSTRUCTION:
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
                gameState = nextState
        for button in instructionButtons:
            button.draw(screen)
    
    if gameState == GameState.LEVEL:
        if(player1.gameOverChecker()):
            gameState = GameState.GAME_OVER

        screen.blit(levelBg, (0, 0))

        #buttons and display
        menuButton = Buttons.textButton(                       #change to restart later
            center_position= (600, 45),
            font_size=30,
            bg_rgb=buttonColor,
            text_rgb=white,
            text="Menu",
            stateChange = GameState.TITLE
        )
        quitButton = Buttons.textButton(
            center_position= (715, 45),
            font_size=30,
            bg_rgb=buttonColor,
            text_rgb=white,
            text="Quit",
            stateChange = GameState.QUIT
        )
        lifeDisplay = Buttons.textButton(       
            center_position=(270, 45),
            font_size=30,
            bg_rgb=buttonColor,
            text_rgb= white,
            text=f"Lives: " + str(player1.lives),
            stateChange = None,
            )
        timeDisplay = Buttons.textButton(       
            center_position=(400, 45),
            font_size=30,
            bg_rgb=buttonColor,
            text_rgb= white,
            text=allLevels[levelIndex].timerMinSec(),         #replace with timer later
            stateChange=None,
            )
        grilledDisplay = Buttons.textButton(       
            center_position=(110, 45),
            font_size=30,
            bg_rgb=buttonColor,
            text_rgb= white,
            text= ": " + str(player1.grilled),       
            stateChange=None,
            )
        levelButtons = [menuButton, quitButton, lifeDisplay, timeDisplay, grilledDisplay]
        for button in levelButtons:
            nextState = button.update(pygame.mouse.get_pos(), click)
            if nextState is not None:
                gameState = nextState
        for button in levelButtons:
            button.draw(screen)
        screen.blit(grilledShroom, (55, 30))    #for counter display

        #cleaning dead things
        allLevels[levelIndex].removeShroom(player1)
        player1.removeDrag()

        #select dragon space
        if player1.selecting and click:
            x,y = pygame.mouse.get_pos()
            print(str(x) + ", " + str(y))
            if x > 179 and x < 780 and y > 79 and y < 580 and player1.shoppingNum != 0:
                player1.shop(x, y)
                player1.selecting = False
            else:
                player1.selecting = False

        #drops and shops buttons update
        for grilled in allLevels[levelIndex].shroomDrops:
            grilled.update(pygame.mouse.get_pos(), click, player1, allLevels[levelIndex])
            grilled.draw(screen)
        for button in player1.shopButtons:                     #wah si spaget code
            button.update(pygame.mouse.get_pos(), click, player1)     
            button.draw(screen)

        #action and draw
        for dragon in player1.mapDrags:
            shroomTarget = dragon.attackChecker(allLevels[levelIndex])
            dragon.attack(allLevels[levelIndex], shroomTarget)
            dragon.draw(screen)

        for shroom in allLevels[levelIndex].listShroom:
            dragonTarget = shroom.collisionWithDrag(player1)
            if shroom.attacking:
                shroom.attackDrag(dragonTarget, allLevels[levelIndex])
            shroom.draw(screen)
        
        if(allLevels[levelIndex].doneChecker()):
            nextLvButton = Buttons.textButton(
            center_position= (560, 550),
            font_size = 30,
            bg_rgb=buttonColor,
            text_rgb=white,
            text="Continue to next level",
            stateChange = GameState.LEVEL
            )
            nextLvButton.draw(screen)

            nextState = nextLvButton.update(pygame.mouse.get_pos(), click)
            if nextState is not None:     #reseting values for next level
                levelIndex = levelIndex + 1
                player1.mapDrags = []
                player1.grilled = 0
                player1.lives = 5
                player1.selecting = False
            nextLvButton.draw(screen)

    if gameState == GameState.GAME_OVER:
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

    if gameState == GameState.QUIT:
        pygame.quit()

    pygame.display.flip()
