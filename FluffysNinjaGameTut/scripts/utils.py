import os
import pygame

BASE_IMG_PATH = 'FluffysNinjaGameTut/data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_duration = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        # If it has a loop
        if self.loop:
            # Force the animation to loop around with modulus
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        # No loop
        else:
            # min finds the last frame in the animation, off by one error so thats why theres -1
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    ''' 
    Get current img of the animation
    
    Returns:
        The current frame in the animation by dividing the total frames from 
        the update method elapsed by the duration
    '''
    def img(self):
        return self.images[int(self.frame / self.img_duration)]