import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSIC_TILES = {'brick', 'wall'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid = []

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'brick', 'pos': (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'wall', 'pos': (10, 5 + i)}

    def tiles_around(self, pos) -> list:
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rect_around(self, pos) -> list:
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSIC_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid:
            surf.blit(self.game.assets[tile['type']], (tile['pos'][0], tile['pos'][1]))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))