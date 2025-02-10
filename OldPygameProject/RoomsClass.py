import pygame
from KeyClass import Key
from DoorClass import Door
pygame.init()

class Room:
    def __init__(self, display, state_manager, player, type, color) -> None:
        self.display = display
        self.rect = display.get_rect()
        self.state_manager = state_manager
        self.player = player
        self.room_type = type
        self.color = color

    def check_collision(self) -> object:
        for obj in self.interactables:
            if self.player.rect.colliderect(obj.rect):
                return obj
        return None

    def update_player_pos(self, current_room, last_room) -> None:
        self.current_room = current_room.room_type
        self.last_room = last_room.room_type
        if self.current_room == 'living room':
            if self.last_room == 'bathroom':
                self.player.rect.center = current_room.bathroom_door_spawn
            if self.last_room == 'bedroom':
                self.player.rect.center = current_room.bedroom_door_spawn
        else:
            self.player.rect.center = current_room.door_spawn
    
    def run(self) -> None:
        self.display.fill(self.color)
        for obj in self.interactables:
            obj.render(self.display)
        self.player.render(self.display)

class LivingRoom(Room):
    def __init__(self, display, state_manager, player, type, color) -> None:
        super().__init__(display, state_manager, player, type, color)
        self.bathroom_door = Door('assets/door.png', (50, 50), 'bathroom')
        self.bathroom_door_spawn = self.bathroom_door.rect.center
        self.bedroom_door = Door('assets/door.png', (100, 150), 'bedroom')
        self.bedroom_door_spawn = self.bedroom_door.rect.center
        
        self.interactables = [
            self.bathroom_door,
            self.bedroom_door
        ]
        
class Bathroom(Room):
    def __init__(self, display, state_manager, player, type, color) -> None:
        super().__init__(display, state_manager, player, type, color)
        self.livingroom_door = Door('assets/door.png', (150, 50), 'living room')
        self.door_spawn = self.livingroom_door.rect.center
        self.bathroom_key = Key('assets/key.png',  (50, 100))

        self.interactables = [
            self.livingroom_door,
            self.bathroom_key
        ]

class Bedroom(Room):
    def __init__(self, display, state_manager, player, type, color) -> None:
        super().__init__(display, state_manager, player, type, color)
        self.livingroom_door = Door('assets/door.png', (100, 150), 'living room')
        self.door_spawn = self.livingroom_door.rect.center
        
        self.interactables = [
            self.livingroom_door 
        ]