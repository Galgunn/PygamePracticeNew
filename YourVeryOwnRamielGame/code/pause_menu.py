from scripts.utils import draw_text
from scripts.state import State

class PauseMenu(State):
    
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        if self.game.menu_options['escape']:
            self.exit_state()
        self.game.reset_keys()

    def render(self, surf):
        self.prev_state.render(surf)
        draw_text(surf, self.game.font, 'le pause', (0,0,0), (50, 50))