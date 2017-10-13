from item import Item

class Player(object):
    inventory = []
    hasAilment = 0
    isSated = 1
    isRescued = False
    lastSated = 0 #date time
    roomsVisited = 0 #keeps track of how many rooms visited
    isDead = False

    def __init__(self, name, location, inventory, condition, sated):
        self.name = name
        self.location = location
        self.inventory = inventory #list of items player is holding
        self.condition = condition#HP make it an integer!
        self.sated = sated  # hunger/thirst

    def getName(self):
        return self.name

    def getInventory(self):
        for items in self.inventory:
            print(items.title)

    def getLocation(self):
        return self.location.title

    def checkCondition(self):
        if self.roomsVisited % 3 == 0:
            self.condition +=1
        if self.condition > 50:
            self.isDead = True

    def getCondition(self):
        if self.condition <= 10:
            print "You feel well"
        elif self.condition > 10 and self.condition <=20:
            print "You are a little worn down"
        elif self.condition > 20 and self.condiion <=30:
            print "Things are looking bad"
        elif self.condition > 30 and self.condiion <=40:
            print "Things are looking bad"
        elif self.condition > 40:
            print "You are on death's door"

    def getSated(self):
        if self.sated != "hungry" and self.sated != "thirsty":
            self.isSated = 1
            return 0
        if self.sated == "hungry":
            self.isSated = 0
            return 1
        if self.sated == "thirsty":
            self.isSated = 0
            return 2

    #add item to player inventory
    def addToInventory(self, i=Item):
        if len(self.inventory) < 10: #arbitrary number for limiting inventory size
            self.inventory.append(i)
        else:
            print "You cannot carry anymore"

    def removeFromInventory(self, i=Item):
        #str(item)
        if i in self.inventory:
            self.inventory.remove(i)
        else:
            print "Cannot find item"

    def addRoomsVisited(self):
        self.roomsVisited += 1

    def getLastSated(self):
        self.lastSated = self.roomsVisited * 4
        print "You ate %d hours ago", (self.lastSated)
        return self.lastSated


