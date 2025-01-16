'''
There is 2 types of positions
- grid pos:String = 3;10
- pixel pos:tuple = (50, 50)

to get grid pos you must divide and turn into an int
    (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

to get pixel pos you must multiply
    (gridpos[0] * TILE_SIZE, gridpos[1] * TILE_SIZE)
'''
import json

import pygame

# Autotiling
AUTOTILE_TYPES = {'grass', 'stone'}
AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8
}
# tiles around the player or entity
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
# a set of tiles that have physics 
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches [-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

    '''
    Finds tiles around pos 

    Returns:
        List of dicts corresponding to a tile that are near a pos
    '''
    def tiles_around(self, pos) -> list:
        tiles = [] # list of tiles dict that are around the players pos
        # Turn the player pixel pos into a tuple thats easy to work with a grid pos
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS: # Get the tuple in NEIGHBOR_OFFSETS
            # Adds tuples tile_loc and offset and turns it to a str to get grid pos
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            # Check to see if check_loc(grid pos) is equal to a key in self.tilemap (grid pos)
            if check_loc in self.tilemap:
                # Adds the value (tile dict) corresponding to the key (grid pos), to tiles list
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    '''
    Get rects near a pos

    Returns:
        A list of rects
    '''
    def physics_rects_around(self, pos) -> list:
        rects = [] # Rects that with collision
        # Check to see if theres a tile dict in the list
        for tile in self.tiles_around(pos):
            # Check to see if the tile is a part of the PHYSICS_TILE set
            if tile['type'] in PHYSICS_TILES:
                # Create and add a rect object of the tile to rects
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                # Check for tiles around current tile
                if check_loc in self.tilemap:
                    # Check if both tiles are the same type
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # First look for tiles in the x axis
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            # Then look for tiles in the y axis
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                # Check if a location is in the tile map dict
                if loc in self.tilemap:
                    # Get the tile
                    tile = self.tilemap[loc]
                    # Blit to the surf provided
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

        '''    
        # loc is the key or grid pos in tilemap dict: {'3;10': {'type': 'grass', 'variant': 1, 'pos': (3, 10)}
        for loc in self.tilemap:
            # Get the value and return a dict of a tile: {'type': 'grass', 'variant': 1, 'pos': (3, 10)}
            tile = self.tilemap[loc]
            # We can use those keys and values in tile to find the specific asset we want to use and where to place it
            # For example: surf.blit(self.game.assets[tile['grass']][tile[1]], (tile['pos'][0]=3 * self.tile_size, tile['pos'][1]=10 * self.tile_size))
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
        '''