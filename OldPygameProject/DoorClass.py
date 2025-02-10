import pygame
pygame.init()

class Door:
    def __init__(self, image_path: str, pos: tuple, next_room: str) -> None:
        self.type = 'door'
        self.image = pygame.image.load(image_path)
        self.pos = pos
        self.rect = self.image.get_rect(topleft= pos)
        self.next_room = next_room
    
    def interact(self, state_manager):
        state_manager.set_state(self.next_room)

    def render(self, display):
        display.blit(self.image, self.rect)

class Peekhole(Door):
    def __init__(self, image_path: str, pos: tuple, next_room: str) -> None:
        super().__init__(image_path, pos, next_room)
        