class Spawner:
    def __init__(self, room, next_room):
        self.room = room
        self.next_room = next_room

    def print_rooms(self):
        print(self.room)
        print(self.next_room)