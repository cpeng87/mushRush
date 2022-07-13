from pygame.sprite import Sprite
import pygame.freetype

class imageButton(object):
    def __init__(self, regPic, bigPic, x, y):
        self.mouse_over = False
        self.x = x
        self.y = y
        self.images = [regPic, bigPic]
        self.rects = [regPic.get_rect(center=(x,y)), bigPic.get_rect(center=(x,y)),]   #coordinates
        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]
    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class textButton(object):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, stateChange=None):      #like a constructor
        self.mouse_over = False

        default_image = create_surface_with_text(text = text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb)
        highlighted_image = create_surface_with_text(text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb)
        self.images = [default_image, highlighted_image]     #images saved in an list
        self.rects = [default_image.get_rect(center=center_position), highlighted_image.get_rect(center=center_position),]   #coordinates
        self.stateChange = stateChange
        super().__init__()    # calls the init method of the parent sprite class

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]
    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, click):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if click:
                return self.stateChange
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("showcardgothic", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()