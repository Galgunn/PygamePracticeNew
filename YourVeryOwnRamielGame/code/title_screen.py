from scripts.state import State
from scripts.utils import draw_text, Animation, load_images
from game import Game
import pygame

class Title(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.SysFont('mspgothic', 20)
        self.font_surf = self.title_font.render('Start', True, (0, 0, 0), (200, 200, 200))
        self.font_rect = self.font_surf.get_rect(topleft=(100, 100))

        self.rect= pygame.Rect(100, 100, 33, 14)

    def update(self):
        mpos = pygame.mouse.get_pos()
        mpos = (mpos[0] / 2, mpos[1] / 2)
        if self.game.menu_options['enter']:
            new_state = Game(self.game)
            new_state.enter_state()
        if self.rect.collidepoint(mpos):
            self.game.assets['start_button'].update()
            if self.game.menu_options['left_click']:
                new_state = Game(self.game)
                new_state.enter_state()
        else:
            self.game.assets['start_button'].reset()
        self.game.reset_keys()


        #print(mpos)
        

    def render(self, surf):
        surf.fill((100,200,45))
        # pygame.draw.rect(surf, (45, 45, 45), self.rect, 1)
        surf.blit(self.game.assets['start_button'].img(), self.rect)
