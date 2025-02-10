
import pygame

class Spritesheet:

    def __init__(self, image) -> None:
        self.sheet = image

    def get_image(self, frame, width, height, strip, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), (strip * height), width, height))
        image.set_colorkey(color)

        return image