'''
After figuring out the whole doors situation, next thing to figure out would be 
the illusion of different sized rooms. I will have to play around with the scales. 
Maybe get started with making background art
'''
import pygame, sys
from os.path import join
from oldplayer import Player
from GameStateManager import GameStateManager
from RoomsClass import LivingRoom, Bathroom, Bedroom

TILE_SIZE = 16
WINDOW_WIDTH = TILE_SIZE * 32
WINDOW_HEIGHT = TILE_SIZE * 32

class Game():
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.screen.fill('white')
        self.clock = pygame.time.Clock()

        # Create player and directions list
        self.player = Player(join('animation assets', 'proto.png'), (50, 50))
        self.directions = []

        # Create displays for the rooms
        self.setup_room_displays()

        # Create state manager and initialize room objects
        self.setup_state_manager()

    def setup_room_displays(self):
        self.living_room_display = pygame.Surface((TILE_SIZE * 15, TILE_SIZE * 15))
        self.bathroom_display = pygame.Surface((TILE_SIZE * 15,TILE_SIZE * 15))
        self.bedroom_display = pygame.Surface((TILE_SIZE * 15, TILE_SIZE * 15))
        

    def setup_state_manager(self):
        self.state_manager = GameStateManager('living room')
        self.living_room = LivingRoom(self.living_room_display, self.state_manager, self.player, 'living room', 'red')
        self.bathroom = Bathroom(self.bathroom_display, self.state_manager, self.player, 'bathroom', 'blue')
        self.bedroom = Bedroom(self.bedroom_display, self.state_manager, self.player, 'bedroom', 'green')

        self.states = {
            'living room': self.living_room,
            'bathroom': self.bathroom,
            'bedroom': self.bedroom
        }

        self.current_state = self.states[self.state_manager.get_current_state()]

    def handle_events(self):
        """
        Handle user input events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.directions.append("up")
                elif event.key == pygame.K_DOWN:
                    self.directions.append("down")
                elif event.key == pygame.K_LEFT:
                    self.directions.append("left")
                elif event.key == pygame.K_RIGHT:
                    self.directions.append("right")
                elif event.key == pygame.K_e:
                    interaction_obj = self.current_state.check_collision()
                    if interaction_obj:
                        if interaction_obj.type == "door":
                            interaction_obj.interact(self.state_manager)
                            self.current_state = self.states[self.state_manager.get_current_state()]
                            self.last_state = self.states[self.state_manager.get_last_state()]
                            self.current_state.update_player_pos(self.current_state, self.last_state)
                        elif interaction_obj.type == "key":
                            interaction_obj.interact()
            elif event.type == pygame.KEYUP:
                self.player.frame = 0
                if event.key == pygame.K_UP:
                    self.directions.remove("up")
                    self.player.action = 3
                elif event.key == pygame.K_DOWN:
                    self.directions.remove("down")
                    self.player.action = 0
                elif event.key == pygame.K_LEFT:
                    self.directions.remove("left")
                    self.player.action = 2
                elif event.key == pygame.K_RIGHT:
                    self.directions.remove("right")
                    self.player.action = 1

    def run(self) -> None:

        # run the event handler
        run = True
        while run:

            self.current_state.run()

            self.handle_events()
            if self.directions:
                self.player.move(self.directions[0], self.current_state.rect)

            self.screen.fill('black')

            # render player
            self.player.render(self.current_state.display)
            self.scaled_display = pygame.transform.scale(self.current_state.display, (WINDOW_WIDTH - (TILE_SIZE * 2), WINDOW_HEIGHT - (TILE_SIZE * 2)))
            self.screen.blit(self.scaled_display, (0, 0))
            
            # blit surfaces onto screen
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    Game().run()