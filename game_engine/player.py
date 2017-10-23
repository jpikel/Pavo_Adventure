from item import Item

class Player(object):
    def __init__(self, name=None):
        self.name = name
        self.illness = 10
        self.hunger = 10
        self.cold = 10
        self.rescued = False
        self.dead = False
        #the player should hold the inventory
        self.inventory = []

    def getName(self):
        return self.name

    def set_player_stats(self, player_dict):
        self.cold = player_dict["cold"]
        self.hunger = player_dict["hunger"]
        self.illness = player_dict["illness"]
        self.name = player_dict["name"]
        self.rescued = player_dict["rescued"]
        self.dead = player_dict["dead"]
        self.inventory= player_dict["inventory"]
        return self

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
        #seems to be evaluating wrong atm
        if turns % 3 == 0:
            self.illness += 1
        if (self.illness > 50 or
            self.hunger > 50 or
            self.cold > 50):
            self.dead = True
        
    def set_illness(self, illness):
        """
        add whatever value is passed in to update the player's illness
        """
        self.illness += illness

    def get_death_status(self):
        return self.dead
    def get_rescue_status(self):
        return self.rescued

    #------------------------------------------------------------------------
    # This section relates to items, and inventory
    #------------------------------------------------------------------------
    def print_inventory(self):
        """
        print the player's current inventory
        """
        if  len(self.inventory) == 0:
            print "You don't have anything in your inventory"
        else:
            text = "Rummaging through your belongings you find "
            for item in self.inventory:
                text += "a " + item['title'] + ", "
            text = text[:-2]
            return text

    def get_items_inventory_titles(self):
        item_list = []
        for item in self.inventory:
            item_list.append(item['title'])
        return item_list

    def search_inventory(self, title):
        items = [item for item in self.inventory if item['title'] == title]
        if items:
            return items[0]
        return None

#ref:https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
    def search_inventory_excluding(self, title):
        return [item for item in self.inventory if item['title'] != title]
#MARKED FOR DELETION
#    def get_item_from_inventory(self, title):
#        for item in self.inventory:
#            if item['title'] == title:
#                return item
#        return None

    def add_item_to_inventory(self, item_to_add):
        """
        adds an item to inventory, does not allow duplicates
        """
        if not self.search_inventory(item_to_add['title']):
            self.inventory.append(item_to_add)

    def remove_item_from_inventory(self, title):
        """
        iterates through inventory to remove the item title passed in
        """
        self.inventory = self.search_inventory_excluding(title)

    def addRoomsVisited(self):
        self.roomsVisited += 1

    def getLastSated(self):
        self.lastSated = self.roomsVisited * 4
        print "You ate %d hours ago", (self.lastSated)
        return self.lastSated


