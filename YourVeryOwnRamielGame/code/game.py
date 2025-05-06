import pygame, sys
from scripts.utils import draw_text
from title_screen import Title

pygame.init()

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Ram')
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.menu_options = {'escape': False, 'enter': False, 'left_click': False}
        self.running = True
        self.state_stack = []
        self.font = pygame.font.SysFont('mspgothic', 25)
        self.load_states()

    def run(self):
        while self.running:
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu_options['escape'] = True
                if event.key == pygame.K_RETURN:
                    self.menu_options['enter'] = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.menu_options['left_click'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.menu_options['escape'] = False
                if event.key == pygame.K_RETURN:
                    self.menu_options['enter'] = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.menu_options['left_click'] = False

    def update(self):
        self.state_stack[-1].update()

    def render(self):
        self.state_stack[-1].render(self.display)
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.flip()
        self.clock.tick(60)

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def reset_keys(self):
        for option in self.menu_options:
            self.menu_options[option] = False

if __name__ == '__main__':
    Game().run()