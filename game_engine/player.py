from item import Item


class Player(object):
    inventory = []
    hasAilment = 0
    isSated = 1
    isRescued = 0
    lastSated = 0 #date time
    roomsVisited = 0 #keeps track of how many rooms visited

    def __init__(self, name, inventory, condition, sated):
        self.name = name
        self.inventory = inventory #list of items player is holding
        self.condition = condition#HP make it an integer!
        self.sated = sated  # hunger/thirst

    def getName(self):
        return self.name

    def getInventory(self):
        for items in self.inventory:
            print(items.name)

    def getCondition(self):
            if self.condition == "well":
                self.hasAilment = 0
                return 0
            if self.condition == "sick":
                self.hasAilment = 1
                return 1
            if self.condition == "injured":
                self.hasAilment = 1
                return 2
            if self.condtion == "dead":
                self.hasAilment = 1
                return 3

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


# manual testing of player
item1 = Item("sleeping bag", "Alex")
item2 = Item("knife", "Alex")
item1.getName
inv = [item1, item2];
person = Player("alex", inv, "well", "thirsty")
x = (person.getCondition())
print x
person.getInventory()
y =person.getName()
print y
z = person.getSated()
print z

item3 = Item("gun", "alex")
person.addToInventory(item3)
person.getInventory()
person.removeFromInventory(item3)
person.getInventory()

item4 = Item("pillow", "alex")
person.removeFromInventory(item4)
person.getInventory()



