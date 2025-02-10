import pygame
pygame.init()

from spritesheet import Spritesheet

# Constant
VELOCITY: int = 1
BLACK: tuple = (0, 0, 0)

class Player:
    def __init__(self, image_path: str, pos: tuple):
        """
        Initialize the Player object.

        Args:
        - image_path (str): Path to the spritesheet file for the player character.
        - pos (tuple): Initial position of the player (x, y).
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.sprite_sheet = Spritesheet(self.image)

        self.setup_animations()

        self.rect = self.animation_list[self.action][self.frame].get_rect(topleft = pos)

    def setup_animations(self) -> None:
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
                self.get_left_facing_frames(strip_counter)
            elif strip_counter == 6:
                self.get_left_facing_frames(strip_counter)

    # Get left facing frames
    def get_left_facing_frames(self, index):
        flipped_list = []
        for anim in self.animation_list[index - 1]:
            flipped_frame = pygame.transform.flip(anim, True, False)
            flipped_frame.set_colorkey((0, 0, 0))
            flipped_list.append(flipped_frame)
        self.animation_list.insert(index, flipped_list)

    def animation_counter(self) -> None:
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = self.current_time
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0

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
        self.animation_counter()
        display.blit(self.animation_list[self.action][self.frame], self.rect.topleft)

