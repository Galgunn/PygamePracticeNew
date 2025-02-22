class Spawner:
    def __init__(self, doorway_to, rect):
        self.doorway_to = doorway_to
        self.rect = rect
        self.left_spawnpoint = [self.rect.midleft[0] - 10, self.rect.midleft[1] - 2.5]
        self.right_spawnpoint = [self.rect.midright[0] + 5, self.rect.midright[1] - 2.5]

    def get_room_name(self):
        return self.doorway_to
