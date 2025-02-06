import pygame, math

class Entity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.collisions = {'left': False, 'right': False, 'up': False, 'down': False}

        #Animation
        self.action = ''
        self.anim_offset = (-2, -10)
        self.flip = False
        self.set_action('idle/right')

    def rect(self):
        return pygame.FRect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def spawn_rects(self, tilemap):
        return tilemap.utilities_rect_around(self.pos)
    
    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def move_next_room(self, map_name, tilemap, dir):
        self.game.load_level(map_name)
        for spawner in tilemap.extract([('utility', 0)], keep=True):
            spawner_rect = pygame.FRect(spawner['pos'][0], spawner['pos'][1], 16, 16)
            if dir == 'left':
                self.pos[0] = spawner_rect.midleft[0] - 10
                self.pos[1] = spawner_rect.midleft[1] - 2.5
            if dir == 'right':
                self.pos[0] = spawner_rect.midright[0] + 5
                self.pos[1] = spawner_rect.midright[1] - 2.5

    def normalize(self, movement):
        magnitude = math.sqrt(pow(movement[0], 2) + pow(movement[1], 2))
        if magnitude != 0:
            vector_normalized = (movement[0] / magnitude, movement[1] / magnitude)
            return vector_normalized
        else:
            return movement

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'left': False, 'right': False, 'up': False, 'down': False}
        frame_movement = pygame.math.Vector2(movement)
        if frame_movement.magnitude() != 0:
            frame_movement = frame_movement.normalize()

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x
        for rect in tilemap.utilities_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] < 0: # Moving left
                    self.collisions['left'] = True
                if frame_movement[0] > 0: # Moving right
                    self.collisions['right'] = True
                    
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if self.collisions['left'] == True:
            self.move_next_room('kitchen', tilemap, 'left')
        if self.collisions['right'] == True:
            self.move_next_room('living_room', tilemap, 'right')
            
        if frame_movement[0] > 0:
            self.flip = False
        if frame_movement[0] < 0:
            self.flip = True
        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        #pygame.draw.rect(surf, 'green', pygame.FRect(self.pos[0] - offset[0], self.pos[1] - offset[1], self.size[0], self.size[1]))
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.idle_dir = 'idle/right'

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action('walk/right')
            self.idle_dir = 'idle/right'
        elif movement[1] < 0:
            self.set_action('walk/up')
            self.idle_dir = 'idle/up'
        elif movement[1] > 0:
            self.set_action('walk/down')
            self.idle_dir = 'idle/down'
        else:
            self.set_action(self.idle_dir)