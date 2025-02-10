import pygame
pygame.init()

class Key:
    def __init__(self, image_path: str, pos: tuple) -> None:
        self.type = 'key'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft= pos)
        self.active = True
        self.picked_up = False

    def interact(self) -> None:
        self.active = False
        self.rect.topleft = (-100, -100)
        self.picked_up = True

    def render(self, display) -> None:
        if self.active:
            display.blit(self.image, self.rect)
