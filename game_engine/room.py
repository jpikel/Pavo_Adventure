from item import Item
from player import Player

class Room(object):
    items = []
    hasItem = None

    def __init__(self, title, items, long_description, short_description, visited, connections):
        self.title = title
        self.coonections = connections
        self.items = items  #items found within room
        #self.feature1 = feature1
        #self.feature2 = feature2
        self.visited = visited
        self.long_description = long_description
        self.short_description = short_description

    def getName(self):
        return self.name

    def getConnections(self):
        return self.connections

    def getItems(self):
        for item in self.items:
            print(item.name)

    def getNumEvents(self):
        return self.events





class room_info():
    room_titles = ["shore", "crash site", "game trail", "field", "dense brush", "camp", "woods",
        "cave", "mountain base", "fire tower", "river", "waterfall", "mountain ascent",
        "mountain summit", "rapids", "ranger station"]
    room_connections = [1,3,2,2,2,3,3,2,2,1,3,1,2,2,2,1]
    room_dir = "../data/rooms/"

    #this list only used if we need to recreate empty rooms
    room_connection_list = {"shore":["crash site"],
            "crash site":["shore", "camp", "game trail"],
            "game trail":["crash site", "cave"],
            "field":["mountain base", "dense brush"],
            "dense brush":["field", "camp"],
            "camp":["dense brush", "woods", "crash site"],
            "woods":["camp", "river", "cave"],
            "cave":["woods", "game trail"],
            "mountain base":["mountain ascent", "field"],
            "fire tower":["mountain summit"],
            "river":["rapids", "waterfall", "woods"],
            "waterfall":["river"],
            "mountain ascent":["mountain summit", "mountain base"],
            "mountain summit":["mountain ascent", "fire tower"],
            "rapids":["ranger station", "river"],
            "ranger station":["rapids"]}


    def get_titles(self):
       return self.room_titles
    def get_connection_amount(self):
        return self.room_connections
    def get_dir(self):
        return self.room_dir
    def get_connection_list(self):
        return self.room_connection_list
    def get_aliases(self, title):
        try:
            return self.aliases[title]
        except Exception, e:
            return None


'''
room = Room("cave", 2, "gun", 2)
room1 = Room("gg", 2, "gun", 2)

room.setNorth
x =room1.getNorth

print x.getName
'''