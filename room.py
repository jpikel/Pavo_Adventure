from item import Item


class Room(object):
    items = []

    def __init__(self, name, connections, items, events):
        self.name = name
        self.connections = connections #pathways to other rooms
        self.items = items  #items found within room
        self.events = events #events that can tigger in a room

    def getName(self):
        return self.name

    def getConnections(self):
        return self.connections

    def getItems(self):
        for item in self.items:
            print(item.name)

    def getNumEvents(self):
        return self.events



room = Room("cave", 2, "gun", 2)
room1 = Room("gg", 2, "gun", 2)

room.setNorth
x =room1.getNorth

print x.getName