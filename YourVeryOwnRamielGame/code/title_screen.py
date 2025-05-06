from scripts.state import State
from scripts.utils import draw_text
from game_world import GameInterface
import pygame

class Title(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.SysFont('mspgothic', 20)
        self.font_surf = self.title_font.render('Start', True, (0, 0, 0), (200, 200, 200))
        self.font_rect = self.font_surf.get_rect()
        print(self.font_rect)

    def update(self):
        mpos = pygame.mouse.get_pos()
        if self.game.menu_options['enter']:
            new_state = GameInterface(self.game)
            new_state.enter_state()
        if self.game.menu_options['left_click']:
            if self.font_rect.collidepoint(mpos):
                self.font_surf = self.title_font.render('Start', True, (0, 0, 0), (100, 100, 200))
        self.game.reset_keys()

        #print(mpos)
        

    def render(self, surf):
        surf.fill((100,200,45))
        draw_text(surf, self.game.font, 'title', (0,0,0), (50, 50))
        surf.blit(self.font_surf, (100, 100))
