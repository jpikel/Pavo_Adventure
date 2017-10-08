from item import Item


class Room(object):
    items = []
    visited = False
    hasItem = None

    def __init__(self, title, connected_rooms, items, feature1, feature2, longDesc, shortDesc):
        self.title = title
        self.connected_rooms = connected_rooms
        self.items = items  #items found within room
        self.feature1 = feature1
        self.feature2 = feature2
        self.longDesc = longDesc
        self.shortDesc = shortDesc

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