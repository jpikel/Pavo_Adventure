"""
Filename - player.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - this file contains the class that is the player.
the player has a name, his health is illness, hunger, cold, whether
the player is dead or rescued, and the player has an inventory
"""
#ref:https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search

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
        """
        returns the player's name
        """
        return self.name

    def set_player_stats(self, player_dict):
        """
        used when a game is loaded to set all the variables of player a player
        then returns the player
        """
        self.cold = player_dict["cold"]
        self.hunger = player_dict["hunger"]
        self.illness = player_dict["illness"]
        self.name = player_dict["name"]
        self.rescued = player_dict["rescued"]
        self.dead = player_dict["dead"]
        self.inventory= player_dict["inventory"]
        return self

    def getCondition(self):
        """
        returns a string that relates the players current illness
        """
        text = ""
        if self.illness <= 10:
            text =  "You feel well, "
        elif self.illness > 10 and self.illness <=20:
            text =  "You are a little worn down, "
        elif self.illness > 20 and self.illness<=30:
            text =  "Things are looking bad, "
        elif self.illness > 30 and self.illness <=40:
            text =  "Things are looking bad, "
        elif self.illness > 40:
            text =  "You are on death's door,"
        if self.hunger <= 10:
            text += "well fed, "
        elif self.hunger > 10 and self.hunger <= 20:
            text += "mildly peckish, "
        elif self.hunger > 20 and self.hunger <= 30:
            text += "very hungry, "
        elif self.hunger > 30 and self.hunger <= 40:
            text += "ravenous, "
        elif self.hunger > 40:
            text += "dying of hunger, "
        if self.cold <= 10:
            text += "and not cold."
        elif self.cold > 10 and self.cold <= 20:
            text += "and chilly."
        elif self.cold > 20 and self.cold <= 30:
            text += "and very cold."
        elif self.cold > 30 and self.cold <= 40:
            text += "and frigid."
        elif self.cold > 40:
            text += "and dying of cold."
        return text

    def updatePlayerCondition(self, turns):
        """
        This works now as intended
        degrades the player's illness and hunger for every 2 moves
        """
        #Degrade the player's condition every three moves.
        #seems to be evaluating wrong atm
        if turns % 2 == 0:
            self.illness += 1
            self.hunger += 2
        if (self.illness > 50 or
            self.hunger > 50 or
            self.cold > 50):
            self.dead = True
        
    def set_illness(self, illness):
        """
        add whatever value is passed in to update the player's illness
        """
        self.illness += illness

    def set_hunger(self, hunger):
        """
        add the value passed in to the hunger attribute of the player
        """
        self.hunger += hunger
    def set_cold(self, cold):
        """
        add the value passed in to the cold attribute of the player
        """
        self.cold += cold
    def set_rescue(self, rescue):
        """
        set the rescued attribute of the player
        """
        self.rescued = rescue

    def get_death_status(self):
        return self.dead

    def get_rescue_status(self):
        return self.rescued

    def get_reason_for_death(self):
        """
        returns a string as to why the player died and from what
        """
        text = 'Sadly, ' + self.getName() + ' died as a result of extreme '
        if self.illness > 50 and self.hunger > 50 and self.cold > 50:
            return text + 'illness, hunger and cold.'
        elif self.illness > 50 and self.hunger > 50:
            return text + 'illness and hunger.'
        elif self.illness > 50 and self.cold > 50:
            return text + 'illness and cold.'
        elif self.hunger > 50 and self.cold > 50:
            return text + 'hunger and cold.'
        elif self.illness > 50:
            return text + 'illness.'
        elif self.hunger > 50:
            return text + 'hunger.'
        elif self.cold > 50:
            return text + 'cold.'
        return ""
    #------------------------------------------------------------------------
    # This section relates to items, and inventory
    #------------------------------------------------------------------------
    def print_inventory(self):
        """
         the player's current inventory
        """
        if  len(self.inventory) == 0:
            text = "You don't have anything in your inventory"
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

    def search_inventory_excluding(self, title):
        return [item for item in self.inventory if item['title'] != title]

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

#    def addRoomsVisited(self):
#        self.roomsVisited += 1
#
#    def getLastSated(self):
#        self.lastSated = self.roomsVisited * 4
#         #"You ate %d hours ago", (self.lastSated)
#        return self.lastSated
#
#
