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