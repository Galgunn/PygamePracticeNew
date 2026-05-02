import pygame, os
pygame.init()

# Declaring variables
DISPLAY_WIDTH: int
DISPLAY_LENGTH: int
BASE_IMG_PATH: str
FONT: pygame.Font

# Initializing variables
DISPLAY_WIDTH = 500
DISPLAY_LENGTH = 500
BASE_IMG_PATH = 'talktome/assets/images/'
FONT = pygame.font.SysFont('consolas', 20)

def load_image(path, colorkey=(1, 1, 1)):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey(colorkey)
    return img

def load_images(path, colorkey=(0, 0, 0)):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, colorkey))
    return images