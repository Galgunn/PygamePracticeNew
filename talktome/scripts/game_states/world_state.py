import pygame
from scripts.state import State

class GameWorld(State):
    def __init__(self, game):
        super().__init__(game)
        self.red_surf: pygame.Surface
        self.red_rect: pygame.FRect
        self.blue_surf: pygame.Surface
        self.blue_rect: pygame.FRect

        self.red_surf = self.game.assets['red']
        self.red_rect = self.red_surf.get_frect(topleft=(350, 0))
        self.blue_surf = self.game.assets['blue']
        self.blue_rect = self.blue_surf.get_frect(topleft=(50, 0))

    def update(self):
        mpos: tuple

        mpos = pygame.mouse.get_pos()
        if self.red_rect.collidepoint(mpos):
            print('Whole lotta red')

        if self.blue_rect.collidepoint(mpos):
            print('I am iceman')

    def render(self, surf):
        surf_rect = surf.get_frect()
        self.red_rect.bottom = surf_rect.bottom
        self.blue_rect.bottom = surf_rect.bottom
        surf.fill('white')
        surf.blit(self.red_surf, self.red_rect)
        surf.blit(self.blue_surf, self.blue_rect)