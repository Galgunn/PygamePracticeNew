import pygame
from scripts.state import State
from scripts.game_states.world_state import GameWorld

class Menu(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        if self.game.state_interaction['left_click']['just_pressed']:
            game_world = GameWorld(self.game)
            game_world.enter_state()

    def render(self, surf):
        surf.fill('green')
