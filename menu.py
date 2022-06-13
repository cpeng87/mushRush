import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates
import level
import shroom

background_color = (215,224,209)      #change to title screen later
white = (255, 255, 255)
titleBg = pygame.image.load('bgPlaceholder.jpg')      #need replace!!!!!!!!!!!
instructions = pygame.image.load('instructionScreen.png')
levelField = pygame.image.load('dragonfield.png')
gameOverScreen = pygame.image.load('gameOverPlaceholder.jpg')

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2
    PAUSE = 3
    INSTRUCTION = 4
    LEVEL = 5
    GAME_OVER = 6

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("showcardgothic", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):      #like a constructor
        self.mouse_over = False

        default_image = create_surface_with_text(text = text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb)
        highlighted_image = create_surface_with_text(text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb)
        self.images = [default_image, highlighted_image]     #images saved in an list
        self.rects = [default_image.get_rect(center=center_position), highlighted_image.get_rect(center=center_position),]   #coordinates
        self.action = action
        super().__init__()    # calls the init method of the parent sprite class

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]
    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def title_screen(screen):
    quit_btn = UIElement(       
        center_position=(650, 500),
        font_size=25,
        bg_rgb=background_color,
        text_rgb= white,
        text="Quit",
        action=GameState.QUIT,
    )
    start_btn = UIElement(
        center_position=(650, 450),
        font_size=30,
        bg_rgb=background_color,
        text_rgb= white,
        text="Start",
        action=GameState.NEWGAME,
    )
    buttons = RenderUpdates(start_btn, quit_btn)
    return game_loop(screen, buttons, titleBg)
    
#need change to actual level
def instruction(screen, player1):
    return_btn = UIElement(
        center_position=(150, 540),
        font_size=20,
        bg_rgb=background_color,
        text_rgb=white,
        text="Return to menu",
        action=GameState.TITLE,
    )

    continue_btn = UIElement(
        center_position=(650, 535),
        font_size=30,
        bg_rgb=background_color,
        text_rgb=white,
        text="Continue",
        action=GameState.LEVEL
    )
    
    buttons = RenderUpdates(return_btn, continue_btn)
    return game_loop(screen, buttons, instructions)

buttonColor = (200,100,100)

def levelTime(screen, player1):
    menu_btn = UIElement(
        center_position= (550, 50),
        font_size=30,
        bg_rgb=buttonColor,
        text_rgb=white,
        text="Menu",
        action=GameState.TITLE
    )

    quit_btn = UIElement(
        center_position= (700, 50),
        font_size=30,
        bg_rgb=buttonColor,
        text_rgb=white,
        text="Quit",
        action=GameState.QUIT
    )

    nextlevel_btn = UIElement(
        center_position= (560, 550),
        font_size = 30,
        bg_rgb=background_color,
        text_rgb=white,
        text="Continue to next level",
        action=GameState.NEXT_LEVEL
    )
    buttons = RenderUpdates(menu_btn, nextlevel_btn, quit_btn)
    return game_loop(screen, buttons, levelField)

def gameOver(screen, player1):
    menu_btn = UIElement(
        center_position= (550, 50),
        font_size=30,
        bg_rgb=buttonColor,
        text_rgb=white,
        text="Menu",
        action=GameState.TITLE
    )

    quit_btn = UIElement(
        center_position= (700, 50),
        font_size=30,
        bg_rgb=buttonColor,
        text_rgb=white,
        text="Quit",
        action=GameState.QUIT
    )
    buttons = RenderUpdates(menu_btn, quit_btn)
    return game_loop(screen, buttons, gameOverScreen)

def game_loop(screen, buttons, bg):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(bg, (0,0))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        if(GameState.LEVEL):
            level.listShrooms.draw(screen)
        pygame.display.flip()

        

