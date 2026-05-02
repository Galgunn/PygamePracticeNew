import pygame, sys
from scripts.utils import DISPLAY_WIDTH, DISPLAY_LENGTH, load_image, load_images
from scripts.game_states.menu_state import Menu

pygame.init()

class Game():
    def __init__(self):
        # Declare variables
        self.screen: pygame.Surface
        self.display: pygame.Surface
        self.clock: pygame.Clock
        self.running: bool
        self.state_stack: list
        self.state_interaction: dict
        self.assets: dict

        # Initialize variables
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_LENGTH)) 
        self.display = pygame.Surface(self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.running = True
        self.state_stack = []

        self.state_interaction = {
            'left_click': {'just_pressed': False},
            'escape_key': {'just_pressed': False}
        }

        self.assets = {
            'red': load_image('characters/red/red.png'),
            'blue': load_image('characters/blue/blue.png'),
            'delighted': load_image('fxs/delighted.png'),
            'suprised': load_image('fxs/suprised.png'),
            'confused': load_image('fxs/confused.png')
        }

        self.load_state()

    def run(self):
        while self.running:

            for option in self.state_interaction:
                self.state_interaction[option]['just_pressed'] = False

            # Event handler            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.state_interaction['left_click']['just_pressed'] = True

            # Update
            self.state_stack[-1].update()

            # Render
            self.state_stack[-1].render(self.display)
            self.screen.blit(self.display, (0, 0))
            
            pygame.display.flip()
            self.clock.tick(60)

    def load_state(self):
        main_menu = Menu(self)
        main_menu.enter_state()
        

if __name__ == '__main__':
    Game().run()