import pygame, sys, spritesheet

# Constants
TILE_SIZE: int = 16
WIDTH = TILE_SIZE * 35
HEIGHT = TILE_SIZE * 35
CAPTION = "Don't Give Up :D"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
VELOCITY = 1

# Represents a key object that can be picked up by the player
class Key:
    def __init__(self, image_path, pos):
        """
        Initialize a Key object.

        Args:
        - image_path (str): Path to the image file for the key.
        - pos (tuple): Initial position of the key (x, y).
        """
        self.type = "key"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.active = True  # Whether the key is active (visible and interactable)
        self.picked_up = False  # Whether the key has been picked up by the player

    def interact(self):
        """ 
        Perform interaction with the key (e.g., when the player picks it up).
        """
        self.active = False
        self.rect.topleft = (-100, -100)  # Move the key off-screen
        self.picked_up = True

    def render(self, display):
        """
        Render the key on the display.

        Args:
        - display (pygame.Surface): The surface onto which the key should be rendered.
        """
        if self.active:
            display.blit(self.image, self.rect.topleft)

# Represents a door object that can transition to another room
class Door:
    def __init__(self, image_path, pos, next_room):
        """
        Initialize a Door object.

        Args:
        - image_path (str): Path to the image file for the door.
        - pos (tuple): Initial position of the door (x, y).
        - next_room (str): Identifier for the next room to transition to.
        """
        self.type = "door"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.next_room = next_room  # Identifier of the next room to transition to

    def interact(self, game_state_manager):
        """
        Perform interaction with the door (e.g., transition to the next room).

        Args:
        - game_state_manager (GameStateManager): The game state manager object.
        """
        game_state_manager.set_state(self.next_room)

    def render(self, display):
        """
        Render the door on the display.

        Args:
        - display (pygame.Surface): The surface onto which the door should be rendered.
        """
        display.blit(self.image, self.rect.topleft)

# Represents the player character
class Player:
    def __init__(self, image_path, pos):
        """
        Initialize the Player object.

        Args:
        - image_path (str): Path to the image file for the player character.
        - pos (tuple): Initial position of the player (x, y).
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.sprite_sheet = spritesheet.Spritesheet(self.image)
        self.animation_list: list = []
        self.animation_frames: list = [2, 2, 2, 4, 4, 4] #down idle, right idle, up idle, down walk, right walk, up walk
        self.action: int = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown: int = 225
        self.frame: int = 0
        strip_counter: int = 0

        # Adding all animation in spritesheet to the main animation list
        for animation in self.animation_frames:
            temp_list = []
            for x in range(animation):
                temp_list.append(self.sprite_sheet.get_image(x, 32, 32, strip_counter, BLACK))
            strip_counter += 1
            self.animation_list.append(temp_list)
            if strip_counter == 2:
                self.get_left_facing_anims(strip_counter)
            elif strip_counter == 6:
                self.get_left_facing_anims(strip_counter)

        self.rect = self.animation_list[self.action][self.frame].get_rect(topleft = pos)

    def get_left_facing_anims(self, index):
        flipped_list = []
        for anim in self.animation_list[index - 1]:
            flipped_frame = pygame.transform.flip(anim, True, False)
            flipped_frame.set_colorkey((0, 0, 0))
            flipped_list.append(flipped_frame)
        self.animation_list.insert(index, flipped_list)

    def move(self, direction, display_rect):
        """
        Move the player character based on the specified direction.

        Args:
        - direction (str): Direction of movement ("up", "down", "left", "right").
        - display_rect (pygame.Rect): The rectangular area representing the display bounds.
        """
        # Walking animations
        
        if direction == "up":
            self.rect.y -= VELOCITY
            self.action = 7
        elif direction == "down":
            self.rect.y += VELOCITY
            self.action = 4
        elif direction == "left":
            self.rect.x -= VELOCITY
            self.action = 6
        elif direction == "right":
            self.rect.x += VELOCITY
            self.action = 5

        # Boundary checking to ensure the player stays within the display bounds
        if self.rect.top < display_rect.top:
            self.rect.top = display_rect.top
        if self.rect.bottom > display_rect.bottom:
            self.rect.bottom = display_rect.bottom
        if self.rect.left < display_rect.left:
            self.rect.left = display_rect.left
        if self.rect.right > display_rect.right:
            self.rect.right = display_rect.right

    def render(self, display):
        """
        Render the player character on the display.

        Args:
        - display (pygame.Surface): The surface onto which the player should be rendered.
        """
        display.blit(self.animation_list[self.action][self.frame], self.rect.topleft)

# Represents the living room area in the game
class LivingRoom:
    def __init__(self, display, gameStateManager, player):
        """
        Initialize the LivingRoom object.

        Args:
        - display (pygame.Surface): The surface representing the living room display.
        - gameStateManager (GameStateManager): The game state manager object.
        - player (Player): The player object.
        """
        self.display = display
        self.rect = display.get_rect()
        self.scale = (TILE_SIZE * 26, TILE_SIZE * 26)  # Scale of the living room area
        self.gameStateManager = gameStateManager
        self.player = player
        self.interactables = [
            Door("assets/door.png", (TILE_SIZE / 2, (self.display.get_height() - TILE_SIZE) / 2), 'bathroom')
        ]

    def check_collisions(self):
        """
        Check for collisions between the player and interactable objects.

        Returns:
        - Interactable object (Door or None): The interactable object collided with by the player,
          or None if no collision.
        """
        for obj in self.interactables:
            if self.player.rect.colliderect(obj.rect):
                return obj
        return None
    
    def check_interactions(self):
        """
        Check for interactions between the player and interactable objects.

        Returns:
        - Interactable object (Door or None): The interactable object interacted with by the player,
          or None if no interaction.
        """
        for obj in self.interactables:
            if self.player.rect.colliderect(obj.rect):
                if obj.type == "door":
                    return obj
        return None
    
    def update_player_position(self):
        """
        Update the player's position after interacting with the bathroom door.
        """
        self.player.rect.topleft = (TILE_SIZE, (self.display.get_height() - TILE_SIZE) / 2)
    
    def run(self):
        """
        Run the living room scene, rendering all components.
        """
        self.display.fill(RED)
        for obj in self.interactables:
            obj.render(self.display)
        self.player.render(self.display)

# Represents the bathroom area in the game
class Bathroom:
    def __init__(self, display, gameStateManager, player):
        """
        Initialize the Bathroom object.

        Args:
        - display (pygame.Surface): The surface representing the bathroom display.
        - gameStateManager (GameStateManager): The game state manager object.
        - player (Player): The player object.
        """
        self.display = display
        self.rect = display.get_rect()
        self.scale = (TILE_SIZE * 26, TILE_SIZE * 26)  # Scale of the bathroom area
        self.gameStateManager = gameStateManager
        self.player = player
        self.key = Key("assets/key.png", (0,0))
        self.interactables = [
            Door("assets/door.png", ((self.display.get_width() - TILE_SIZE * 1.5), (self.display.get_height() - TILE_SIZE) / 2), 'living room'),
            self.key
        ]

    def check_collisions(self):
        """
        Check for collisions between the player and interactable objects.

        Returns:
        - Interactable object (Door, Key, or None): The interactable object collided with by the player,
          or None if no collision.
        """
        for obj in self.interactables:
            if self.player.rect.colliderect(obj.rect):
                return obj
        return None
    
    def check_interactions(self):
        """
        Check for interactions between the player and interactable objects.

        Returns:
        - Interactable object (Door, Key, or None): The interactable object interacted with by the player,
          or None if no interaction.
        """
        for obj in self.interactables:
            if self.player.rect.colliderect(obj.rect):
                if obj.type == "door":
                    return obj
                elif obj.type == "key":
                    return obj
        return None
    
    def update_player_position(self):
        """
        Update the player's position after interacting with the living room door.
        """
        self.player.rect.topleft = (self.display.get_width() - TILE_SIZE * 2 , (self.display.get_height() - TILE_SIZE) / 2)

    def run(self):
        """
        Run the bathroom scene, rendering all components.
        """
        self.display.fill(BLUE)
        for obj in self.interactables:
            obj.render(self.display)
        self.player.render(self.display)
        
# Manages the current game state
class GameStateManager:
    def __init__(self, current_State):
        """
        Initialize the GameStateManager.

        Args:
        - current_State (str): Identifier of the initial game state.
        """
        self.current_state = current_State

    def get_state(self):
        """
        Get the current game state.

        Returns:
        - str: Identifier of the current game state.
        """
        return self.current_state
    
    def set_state(self, state):
        """
        Set the current game state.

        Args:
        - state (str): Identifier of the new game state.
        """
        self.current_state = state

# Main game class that manages initialization, input handling, and game loop
class Game:
    def __init__(self):
        """
        Initialize the Game object.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)

        # Set up game rooms and initial configurations
        self.setup_rooms()
        self.directions = []

        # Initialize the player character
        self.player = Player("animation assets/proto.png", ((self.living_room_display.get_width() - TILE_SIZE) / 2, (self.living_room_display.get_height() - TILE_SIZE) / 2))

        # Set up game state manager and initial game state
        self.setup_gameStateManager()

    def setup_rooms(self):
        """
        Set up game room displays.
        """
        self.living_room_display = pygame.Surface((WIDTH / 3, HEIGHT / 3))
        print(self.living_room_display)
        self.bathroom_display = pygame.Surface((WIDTH / 4, HEIGHT / 4))
        print(self.bathroom_display)

    
    def setup_font(self, text):
        """
        Set up font for in-game text rendering.
        """
        self.text_surface = self.font.render(text, False, 'Purple')
        self.text_rect = self.text_surface.get_rect()

    def setup_gameStateManager(self):
        """
        Set up game state manager and initial game states.
        """
        self.game_state_manager = GameStateManager('living room')
        self.living_room = LivingRoom(self.living_room_display, self.game_state_manager, self.player)
        self.bathroom = Bathroom(self.bathroom_display, self.game_state_manager, self.player)

        self.states = {'living room': self.living_room, 
                       'bathroom': self.bathroom}
        self.current_state = self.states[self.game_state_manager.get_state()]

    def handle_input(self):
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
                elif event.key == pygame.K_e and self.current_state.check_collisions():
                    interaction_obj = self.current_state.check_interactions()
                    if interaction_obj:
                        if interaction_obj.type == "door":
                            interaction_obj.interact(self.game_state_manager)
                            self.current_state = self.states[self.game_state_manager.get_state()]
                            self.current_state.update_player_position()
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

    def run(self):
        """
        Run the game loop.
        """
        run = True
        while run:
            # Update the main game screen
            self.screen.fill(BLACK)

            # Run the current state (living room or bathroom)
            self.current_state.run()

            # Handle user input events
            self.handle_input()
            # Move the player based on input directions
            if self.directions:
                self.player.move(self.directions[0], self.current_state.rect)

            # Display interaction text when colliding with an object
            colliding = self.current_state.check_collisions()
            if colliding:
                self.setup_font('E')
                self.text_rect.centerx = self.player.rect.centerx
                self.text_rect.top = self.player.rect.bottom
                self.current_state.display.blit(self.text_surface, self.text_rect)

            current_time = pygame.time.get_ticks()
            if current_time - self.player.last_update >= self.player.animation_cooldown:
                self.player.frame += 1
                self.player.last_update = current_time
                if self.player.frame >= len(self.player.animation_list[self.player.action]):
                    self.player.frame = 0

            self.display_centerloc = ((WIDTH - self.current_state.scale[0]) / 2, (HEIGHT - self.current_state.scale[1]) / 2)
            #self.screen.blit(pygame.transform.scale(self.current_state.display, self.current_state.scale), self.display_centerloc)
            if self.bathroom.key.picked_up == True:
                self.setup_font("You Win!!!")
                self.screen.blit(self.text_surface, self.text_rect)
            else:
                self.screen.blit(pygame.transform.scale(self.current_state.display, (TILE_SIZE * 26, TILE_SIZE * 26)), self.display_centerloc)
            pygame.display.update()
            self.clock.tick(60)

# Run the game
if __name__ == "__main__":
    Game().run()
