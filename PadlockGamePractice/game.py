import pygame, sys

from scripts.utils import load_image, load_images, Animation
from scripts.entities import Entity, Player
from scripts.tilemap import Tilemap

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Practicing')
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.assets = {
            'player': load_image('player/idle/right/00.png'),
            'wall': load_images('tiles/wall'),
            'floor': load_images('tiles/floor'),
            'utility': load_images('tiles/utility'),
            'player/idle/down': Animation(load_images('player/idle/down'), frame_dur=12),
            'player/idle/right': Animation(load_images('player/idle/right'), frame_dur=12),
            'player/idle/up': Animation(load_images('player/idle/up'), frame_dur=12),
            'player/walk/down': Animation(load_images('player/walk/down'), frame_dur=10),
            'player/walk/right': Animation(load_images('player/walk/right'), frame_dur=10),
            'player/walk/up': Animation(load_images('player/walk/up'), frame_dur=10),
        }
            
        self.player = Player(self, (0, 0), (5, 5))
        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self, 16)
        self.load_level('living_room')

        spawn_points = []
        for spawn_point in self.tilemap.extract([('utility', 0)], keep=False):
            spawn_points.append(pygame.FRect(spawn_point['pos'][0], spawn_point['pos'][1], 16, 16))
        
        self.player.pos[0] = (spawn_points[0].centerx - 2.5)
        self.player.pos[1] = (spawn_points[0].centery -2.5)

        self.scroll = [0, 0]

    def load_level(self, map_name):
        self.tilemap.load('PadlockGamePractice/assets/maps/' + str(map_name) + '.json')

    def run(self):
        self.run = True
        while self.run:
            self.display.fill((100, 200, 100))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]))
            self.player.render(self.display, offset=render_scroll)

            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    # if event.key == pygame.K_1:
                    #     self.level = 1
                    #     self.load_level(self.level)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

            # Game rendering
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    Game().run()
            