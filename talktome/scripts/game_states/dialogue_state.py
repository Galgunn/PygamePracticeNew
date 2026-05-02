import pygame
from scripts.state import State

SCALE: int = 3

class Dialogue(State):
    def __init__(self, game, character=pygame.Surface):
        super().__init__(game)
        self.char_surf: pygame.Surface
        self.char_rect: pygame.FRect
        self.char_pos: tuple

        self.char_surf = pygame.transform.scale_by(character, SCALE)
        self.char_rect = self.char_surf.get_frect()

    def update(self):
        pass

    def render(self, surf):
        surf.fill('blue')
        surf_rect = surf.get_frect()
        self.char_rect.bottom = surf_rect.bottom
        surf.blit(self.char_surf, (self.char_rect))
        