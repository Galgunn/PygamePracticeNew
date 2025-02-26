import pygame, os

BASE_MAP_PATH = 'PadlockGamePractice/assets/maps'
BASE_IMG_PATH = 'PadlockGamePractice/assets/images/'

def load_image(path, colorkey=(0, 0, 0)):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey(colorkey)
    return img

def load_images(path, colorkey=(0, 0, 0)):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, colorkey))
    return images

def load_maps():
    maps = []
    for map_name in os.listdir(BASE_MAP_PATH):
        maps.append(map_name.split('.')[0])
    return maps

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class Spritesheet():
    def __init__(self, img, size):
        self.sheet = img
        self.size = size
        
    def get_image(self, column, row, color=(0, 0, 0)):
        surf = pygame.Surface(self.size)
        surf.blit(self.sheet, (0, 0), ((column * self.size[0]), (row * self.size[1]), self.size[0], self.size[1]))
        surf.set_colorkey(color)
        return surf
    
    def get_frames(self, row, frames):
        animation_frames = []
        for x in range(frames):
            animation_frames.append(self.get_image(x, row, (0, 0, 0)))
        return animation_frames
    
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

    def img(self):
        return self.images[int(self.frame / self.frame_dur)]