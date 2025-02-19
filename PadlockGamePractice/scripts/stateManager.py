class StateManager:
    def __init__(self, current_state, tilemap) -> None:
        self.current_state = current_state
        self.last_state = current_state
        self.tilemap = tilemap

    def load_map(self, map_name):
        self.tilemap.load('PadlockGamePractice/assets/maps/' + str(map_name) + '.json')

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