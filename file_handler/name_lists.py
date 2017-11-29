"""
Filename - name_lists.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - Official lists of of official names for rooms, items, keys in the dicts
"""

import os
from collections import OrderedDict
data_dir = os.path.abspath('data')

class room_info():
    """
        this class contains official titles and connections about rooms
        also contains the room directories.
        only has getters for the different static variables
    """
    room_titles = ["shore", "crash site", "game trail", "field", "dense brush", "camp", "woods",
        "cave", "mountain base", "fire tower", "river", "waterfall", "mountain path",
        "mountain summit", "rapids", "ranger station"]
    room_singles = ['shore', 'crash', 'site', 'game', 'trail', 'field', 'dense', 'brush',
            'camp', 'mountain', 'summit', 'rapids', 'ranger', 'station', 'river',
            'waterfall', 'cave', 'fire', 'tower', 'path', 'base']
    room_connections = [1,3,2,2,2,3,3,2,2,1,3,1,2,2,2,1]
    room_dir = os.path.join(data_dir, "rooms")
    room_dir_dict = os.path.join(data_dir, "rooms_dict")
    feature_dir_dict = os.path.join(data_dir, "feature_dict")

    #this list only used if we need to recreate empty rooms
    room_connection_list = {"shore":["crash site"],
            "crash site":["shore", "camp", "game trail"],
            "game trail":["crash site", "cave"],
            "field":["mountain base", "dense brush"],
            "dense brush":["field", "camp"],
            "camp":["dense brush", "woods", "crash site"],
            "woods":["camp", "river", "cave"],
            "cave":["woods", "game trail"],
            "mountain base":["mountain path", "field"],
            "fire tower":["mountain summit"],
            "river":["rapids", "waterfall", "woods"],
            "waterfall":["river"],
            "mountain path":["mountain summit", "mountain base"],
            "mountain summit":["mountain path", "fire tower"],
            "rapids":["ranger station", "river"],
            "ranger station":["rapids"]}

    def get_titles(self):
       return self.room_titles
    def get_singles(self):
       return self.room_singles
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
    def get_dir_dict(self):
        return self.room_dir_dict
    def get_feature_dict_dir(self):
        return self.feature_dir_dict

class item_info():
    """
        this class contains the official information about items, their titles,
        and the directory for the templates
        only has getters for these features
    """
    item_titles = ["lantern", "heavy winter parka", "old map", "spiral bound notepad",
                "flare gun", "boat paddle", "rescue whistle",
                "can of sweetened condensed milk", "candy bar", "medical kit"]
    item_dir = os.path.join(data_dir, "items")

    item_singles = ['lantern', 'heavy', 'winter', 'parka', 'map', 'spiral', 'bound',
            'notepad', 'flare', 'gun', 'boat', 'paddle', 'rescue', 'whistle',
            'can','of',
            'sweetened', 'condensed', 'milk', 'candy', 'bar', 'medical', 'kit']

    def get_titles(self):
        return self.item_titles
    def get_singles(self):
        return self.item_singles
    def get_dir(self):
        return self.item_dir
    def get_dir_dict(self):
        return os.path.join(data_dir, "items_dict")

class save_info():
    """
        official save info and getters to access the save information
        primarily save directories
    """
    temp_save_dir_rooms = os.path.join(data_dir, "temp_save_game/rooms")
    temp_save_dir_items = os.path.join(data_dir, "temp_save_game/items")
    save_dir = os.path.join(data_dir, "save_game")
    save_dir_rooms = os.path.join(data_dir, "save_game/rooms")
    save_dir_items = os.path.join(data_dir, "save_game/items")


    def get_temp_save_dir_rooms(self):
        return self.temp_save_dir_rooms
    def get_temp_save_dir_items(self):
        return self.temp_save_dir_items
    def get_save_dir(self):
        return self.save_dir
    def get_save_dir_rooms(self):
        return self.save_dir_rooms
    def get_save_dir_items(self):
        return self.save_dir_items


class verb_info():
    """
        official verb info and getters to access the verb features
    """
    verbs = ["look", "look at", "go", "take", "help", "inventory",
            "use", "search", "pull", "eat", "read", "drop"]

    verb_definitions = OrderedDict({
            "look": "Will repeat the long description of the room",
            "look at": "<feature or object> Allows you to look at something in the game",
            "go":"Move to another room",
            "take":"Pick up an item",
            "drop":"Drop an item",
            "help":"Display this menu",
            "inventory":"Opens your character's inventory",
            "use":"Use an item in your inventory",
            "search":"search a feature to find items",
            "pull":"Pull on a feature in a room",
            "eat":"Your character attempts to eat an item",
            "read":"Your character attempts to read an item"
            })


    def get_verbs(self):
        return self.verbs
    def get_verb_definitions(self):
        return self.verb_definitions
    def get_dir_dict(self):
        return os.path.join(data_dir, "verbs_dict")

class dict_keys():
    """
    official dict keys are stored here as lists with getters
    """
    room_keys = ["id", "title", "visited", "long_description", "short_description",
            "features", "connected_rooms", "items_in_room", "feature_searched",
            "room_temp", "room_artifact"]
         #   "room_hazards", "room_hazard_description", "room_hazard_item",
          #  "room_hazard_occurs_description", "room_hazard_attributes_affected",
          #  "room_hazard_safe_description"]
    feature_keys = ["aliases","verbs","title"]
    verbs = ["look at", "take",
            "use", "search", "pull", "eat", "read", "drop"]
    verb_keys = ["description", "modifiers"]
    use_additional_keys = ["deactivate_description"]
    connected_room_keys = ["accessible", "distance_from_room", "title",
            "pre_item_description", "item_required_title", "compass_direction",
            "id", "item_required", "aliases"]
    item_keys = ["id", "title", "aliases", "verbs", "active", "activatable"]
#            "attributes_affected_requirement_met",
#            "attributes_affected_requirement_not_met",
#            "requirement_met", "requirement_met_description",
#            "requirement_not_met_description",
#            "item_combination", "room_combination",
#            "feature_combination"]
    optional_keys = ["artifact", "modifiers", "act_mods", "de_mods", "own_updates"]


    def get_room_keys(self):
        return self.room_keys
    def get_feature_keys(self):
        return self.feature_keys
    def get_verbs(self):
        return self.verbs
    def get_verb_keys(self):
        return self.verb_keys
    def get_opt_keys(self):
        return self.optional_keys
    def get_additional_use_keys(self):
        return self.use_additional_keys
    def get_connected_room_keys(self):
        return self.connected_room_keys
    def get_item_keys(self):
        return self.item_keys
