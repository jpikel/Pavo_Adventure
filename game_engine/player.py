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
import engine_helpers as helpers

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

    @property
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
            text =  "You feel well "
        elif self.illness > 10 and self.illness <=20:
            text =  "You are a little worn down, and you are "
        elif self.illness > 20 and self.illness<=30:
            text =  "Things are looking bad, and you are "
        elif self.illness > 30 and self.illness <=40:
            text =  "Things are looking bad, and you are "
        elif self.illness > 40:
            text =  "You are on death's door, and you are"
        if self.hunger <= 10:
            text += "well fed "
        elif self.hunger > 10 and self.hunger <= 20:
            text += "mildly peckish "
        elif self.hunger > 20 and self.hunger <= 30:
            text += "very hungry "
        elif self.hunger > 30 and self.hunger <= 40:
            text += "ravenous "
        elif self.hunger > 40:
            text += "dying of hunger "
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

    def updatePlayerCondition(self, turns, room_temp):
        """
        This works now as intended
        degrades the player's illness and hunger for every 2 moves
        if the player has the parka and is wearing it then we give the player
        a reduction in his cold attribute
        """
        #Degrade the player's condition every two moves.
        #seems to be evaluating wrong atm

        #here's the parka boost to the player!
        parka = self.search_inventory('heavy winter parka')
        if parka is not None and parka['active'] == True:
            self.cold -= 2
        self.cold += room_temp
        if turns % 2 == 0:
            self.illness += 1
            self.hunger += 2
        if (self.illness > 50 or
            self.hunger > 50 or
            self.cold > 50):
            self.dead = True
        
    def add_to_illness(self, illness):
        """
        add whatever value is passed in to update the player's illness
        """
        self.illness += illness

    def add_to_hunger(self, hunger):
        """
        add the value passed in to the hunger attribute of the player
        """
        self.hunger += hunger
    def add_to_cold(self, cold):
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
        text = 'Sadly, ' + self.name + ' died as a result of extreme '
        if self.illness > 50 and self.hunger > 50 and self.cold > 50:
            text += 'wounds, hunger and cold.'
        elif self.illness > 50 and self.hunger > 50:
            text += 'wounds and hunger.'
        elif self.illness > 50 and self.cold > 50:
            text += 'wounds and cold.'
        elif self.hunger > 50 and self.cold > 50:
            text += 'hunger and cold.'
        elif self.illness > 50:
            text += 'wounds.'
        elif self.hunger > 50:
            text += 'hunger.'
        elif self.cold > 50:
            text += 'cold.'
        text += ' As hard as you tried you did not manage to brave the elements.'
        text += (' Next time perhaps take better care of yourself.  Cold, hunger,'
             ' and illness can all come quickly in the Desolate Journey.'
             ' The challenges are tough but they can be overcome and you will'
             ' one day find your way to rescue.  But, not on this day.')
        if self.dead:
            return text
        return ""
    #------------------------------------------------------------------------
    # This section relates to items, and inventory
    #------------------------------------------------------------------------
    @property
    def get_inventory(self):
        return self.inventory

    def print_inventory(self):
        """
         the player's current inventory
        """
        if  len(self.inventory) == 0:
            text = "You don't have anything in your inventory"
        else:
            item_list = self.inventory
            text = "Rummaging through your belongings you find "
            for item in item_list:
                #if we have more than 1 item in our list
                #and this item is the last item
                #use and item
                if (item_list.index(item) > 0 and 
                        item_list.index(item) == len(item_list)-1):
                    text += 'and a ' + item['title'] + '.'
                else:
                    text += 'a ' + item['title'] + ', '
            if text[-2] == ',':
                text = text[:-2] + '.'

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
    #------------------------------------------------------------------------
    # This section relates to item actions
    #------------------------------------------------------------------------
    def item_action_inventory(self, item_title, action, room_searched):
        """
        called by the verb handler.  Looks up the item file and opens it
        returns the description listed for the particular verb at this moment.
        and modifiers if any
        """
        res = helpers.response_struct()
        try:
            item = self.search_inventory(item_title)
            if item and action == 'take':
                res.description = 'You are already holding the ' + item_title + '.'
                return res
            res.title = item_title
            res.description = item['verbs'][action]['description']
            res.modifiers = item['verbs'][action]['modifiers']
            #res["success"] = True
            if 'artifact' in item['verbs'][action]:
                res.artifact = item['verbs'][action]['artifact']
            if action == "use" and item['activatable'] == True:
                if item['active'] == True:
                    item['active'] = False
                    if 'de_mods' in item['verbs']['use']:
                        res.modifiers = item['verbs']['use']['de_mods']
                    res.description = item['verbs']['use']['deactivate_description']
                else:
                    item['active'] = True
                    if 'act_mods' in item['verbs']['use']:
                        res.modifiers = item['verbs']['use']['act_mods']
            elif action == "drop" and room_searched == False:
                res.description = "There is no where secure to drop the item."
                res.modifiers = {}
        except KeyError:
            res.description = 'You are not able to ' + action + ' ' + item_title+'.'
        return res
