import pygame, sys
from spritesheet import Spritesheet

# Constants
TILE_SIZE: int = 16
WIDTH: int = TILE_SIZE * 35
HEIGHT: int = TILE_SIZE * 35
CAPTION: str = "Animation Test"
WHITE: tuple = (255, 255, 255)
BLACK: tuple = (0, 0, 0)
BG: tuple = (60, 60, 60)

class Player:
    def __init__(self):
        self.image = pygame.image.load("animation assets/proto.png").convert_alpha()
        self.sprite_sheet = Spritesheet(self.image)
        self.animation_list: list = []
        self.animation_frames: list = [2, 2, 2, 4, 4, 4]
        self.action: int = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown: int = 225
        self.frame: int = 0
        strip_counter: int = 0

        for animation in self.animation_frames:
            temp_list = []
            for x in range(animation):
                temp_list.append(self.sprite_sheet.get_image(x, 32, 32, strip_counter, BLACK))
            strip_counter += 1
            self.animation_list.append(temp_list)
            if strip_counter == 2:
                self.get_left_anims(strip_counter)
            elif strip_counter == 6:
                self.get_left_anims(strip_counter)

    def get_left_anims(self, index):
        flipped_list = []
        for anim in self.animation_list[index - 1]:
            flipped_frame = pygame.transform.flip(anim, True, False)
            flipped_frame.set_colorkey((0, 0, 0))
            flipped_list.append(flipped_frame)
        self.animation_list.insert(index, flipped_list)

    def render(self, screen):
        screen.blit(self.animation_list[self.action][self.frame], (0 ,0))

class Game:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.display = pygame.Surface((WIDTH // 2, HEIGHT // 2))

        self.player = Player()

    def state_checking(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN and self.player.action > 0:
                        self.player.action -= 1
                        self.player.frame = 0
                    if event.key == pygame.K_UP and self.player.action < len(self.player.animation_list) - 1:
                        self.player.action += 1
                        self.player.frame = 0

    def run(self):
        run = True
        while run:
            self.state_checking()

            current_time = pygame.time.get_ticks()
            if current_time - self.player.last_update >= self.player.animation_cooldown:
                self.player.frame += 1
                self.player.last_update = current_time
                if self.player.frame >= len(self.player.animation_list[self.player.action]):
                    self.player.frame = 0
            
            self.display.fill(BG)
            self.player.render(self.display)
            self.screen.blit(pygame.transform.scale(self.display, (WIDTH, HEIGHT)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

# Run the game
if __name__ == "__main__":
    Game().run()