from player import Player
from room import Room


class Game:
    map [16]

    def __init__(self, player, map, tod):
        self.player = player
        self.map = map  #list of connecting rooms
        self.tod = tod  #time of day




