import pygame, os

BASE_IMG_PATH = 'YourVeryOwnRamielGame/assets/images/'

def draw_text(surf, font, text, color, pos):
    text_surf = font.render(text, True, color)
    #text_surf.set_colorkey((0, 0, 0))
    text_rect = text_surf.get_rect()
    text_rect.topleft = pos
    surf.blit(text_surf, text_rect)

def load_image(path, colorkey=(0, 0, 0)):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey(colorkey)
    return img

def load_images(path, colorkey=(0, 0, 0)):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, colorkey))
    return images

class Animation():
    def __init__(self, images, frame_dur, loop=True):
        self.images = images
        self.frame_dur = frame_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.frame_dur, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.frame_dur * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.frame_dur * len(self.images) - 1)
            if self.frame >= self.frame_dur * len(self.images) - 1:
                self.done = True

    def reset(self):
        self.frame = 0

    def img(self):
        return self.images[int(self.frame / self.frame_dur)]