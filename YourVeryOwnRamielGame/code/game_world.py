from scripts.state import State
from pause_menu import PauseMenu
from scripts.utils import draw_text

class GameInterface(State):

    def __init__(self, game):
        super().__init__(game)

    def update(self):
        if self.game.menu_options['escape']:
            self.exit_state()
        if self.game.menu_options['enter']:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.game.reset_keys()
            

    def render(self, surf):
        surf.fill((45,30,56))
        draw_text(surf, self.game.font, 'Gaming!!!', (0,0,0), (0,40))