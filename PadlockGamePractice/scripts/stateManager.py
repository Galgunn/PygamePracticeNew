class StateManager:
    def __init__(self, current_state, game) -> None:
        self.current_state = current_state
        self.last_state = current_state
        self.game = game
        self.player = self.game.player

    def get_current_state(self):
        return self.current_state
    
    def get_last_state(self):
        return self.last_state
    
    def set_state(self, state):
        self.last_state = self.current_state
        self.current_state = state

    def print_all(self):
        print(self.current_state)
        print(self.last_state)
        print(self.player)