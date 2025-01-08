import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        # Animation
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

    '''
    Dynamicly create a rect to not update it each time

    Returns: 
        A rect
    '''
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        # Handle x movement and collision
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        # Check to see if there are any rects in list
        for rect in tilemap.physics_rects_around(self.pos):
            # Check for collision
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: # collision e_rect moving right
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0: # collision e_rect moving left
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x # update players pos after collision

        # Handle y movement and collision
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        # Check to see if there are any rects in list
        for rect in tilemap.physics_rects_around(self.pos):
            # Check for collision
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0: # collision e_rect moving down
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0: # collision e_rect moving up
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y # update players pos after collision

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        # Gravity and thermal velocity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Stop player if rect collides with down or up direction
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')