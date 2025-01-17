import sys
import pygame
from scripts.utils import load_images, load_maps
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0
BASE_MAP_PATH = 'PadlockGamePractice/assets/rooms/'

class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Editor')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.assets = {
            'floor': load_images('tiles/floor'),
            'wall': load_images('tiles/wall'),
        }
        self.rooms = {}
        
        maps = load_maps()
        level = 0
        for room in maps:
            self.rooms[room] = level
            level += 1

        # Camera movement
        self.movement = [False, False, False, False]
        
        self.tilemap = Tilemap(self, tile_size=16)

        # Loading of tilemap
        self.level = 0
        try:
            self.load_level(self.level)
        except FileNotFoundError:
            pass

        # Camera offset
        self.scroll = [0, 0]

        # Get tile
        self.tile_list = list(self.assets) # Returns assets keys
        self.tile_group = 0
        self.tile_variant = 0

        # Tile selection
        self.left_click = False
        self.right_click = False
        self.shift = False
        # Grid placement toggle
        self.ongrid = True

    def load_level(self, map_id):
        self.tilemap.load('PadlockGamePractice/assets/rooms/' + str(map_id) + '.json')
        
    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            # Camera movement
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            # Scale down due to scaling in our blitting
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            # Calculate grid pos
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            ''' 
            Displays where your current tile will be placed
            '''
            if self.ongrid:
                # Scale into pixel grid pos, and snap onto grid
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            # Add tile to tilemap
            if self.left_click and self.ongrid:
                # Add dict of tile to tilemap variable in Tilemap
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}

            # Remove tiles pixel grid tiles
            if self.right_click:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                # Remove offgrid tiles
                for tile in self.tilemap.offgrid.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_rect = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_rect.collidepoint(mpos):
                        self.tilemap.offgrid.remove(tile)

            # Display the current tile your selecting
            self.display.blit(current_tile_img, (5, 5))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.left_click = True
                        # Allowing off grid tile placement
                        if not self.ongrid:
                            # Add dict of tile to offgrid tiles variable in Tilemap
                            self.tilemap.offgrid.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_click = True
                    if self.shift:
                        if event.button == 4:
                            # Modulus loop trick
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            # Modulus loop trick
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            # Modulus loop trick
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            # To avoid out of index error
                            self.tile_variant = 0
                        if event.button == 5:
                            # Modulus loop trick
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            # To avoid out of index error
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.left_click = False
                    if event.button == 3:
                        self.right_click = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    # if event.key == pygame.K_t:
                    #     self.tilemap.autotile()
                    if event.key == pygame.K_e:
                        map_name = str(input('Save map name: '))
                        if not self.rooms:
                            self.rooms[map_name] = 0
                        if map_name not in self.rooms:
                            levels = list(self.rooms.values())
                            self.rooms[map_name] = levels[-1] + 1
                        self.tilemap.save(BASE_MAP_PATH + map_name + '.json')
                    if event.key == pygame.K_o:
                        map_name = str(input('load map name: '))
                        if map_name in self.rooms:
                            self.load_level(map_name)
                    if event.key == pygame.K_i:
                        print(self.rooms)
                                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()