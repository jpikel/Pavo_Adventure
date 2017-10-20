from item import Item

class Player(object):
    def __init__(self, name):
        self.name = name
        self.illness = 10
        self.hunger = 10
        self.cold = 10
        self.rescued = False
        self.dead = False

    def getName(self):
        return self.name

    def getCondition(self):
        text = ""
        if self.illness <= 10:
            text =  "You feel well."
        elif self.illness > 10 and self.illness <=20:
            text =  "You are a little worn down."
        elif self.illness > 20 and self.illness<=30:
            text =  "Things are looking bad."
        elif self.illness > 30 and self.illness <=40:
            text =  "Things are looking bad."
        elif self.illness > 40:
            text =  "You are on death's door."
        return text

    def updatePlayerCondition(self, turns):
        #Degrade the player's condition every three moves.
        if turns % 3 == 0:
            self.illness += 1
        if (self.illness > 50 or
            self.hunger > 50 or
            self.cold > 50):
            self.dead = True


    # def getSated(self):
    #     if self.sated != "hungry" and self.sated != "thirsty":
    #         self.isSated = 1
    #         return 0
    #     if self.sated == "hungry":
    #         self.isSated = 0
    #         return 1
    #     if self.sated == "thirsty":
    #         self.isSated = 0
    #         return 2

    #add item to player inventory
    # def addToInventory(self, i=Item):
    #     if len(self.inventory) < 10: #arbitrary number for limiting inventory size
    #         self.inventory.append(i)
    #     else:
    #         print "You cannot carry anymore"

    # def removeFromInventory(self, i=Item):
    #     #str(item)
    #     if i in self.inventory:
    #         self.inventory.remove(i)
    #     else:
    #         print "Cannot find item"

    def addRoomsVisited(self):
        self.roomsVisited += 1

    def getLastSated(self):
        self.lastSated = self.roomsVisited * 4
        print "You ate %d hours ago", (self.lastSated)
        return self.lastSated


