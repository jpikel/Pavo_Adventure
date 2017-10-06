"""
Filename - name_lists.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - 
"""

class room_info():
    room_titles = ["shore", "crash site", "game trail", "field", "dense brush", "camp", "woods",
        "cave", "mountain base", "fire tower", "river", "waterfall", "mountain ascent", 
        "mountain summit", "rapids", "ranger station"]
    room_connections = [1,3,2,2,2,3,3,2,2,1,3,1,2,2,2,1]
    room_dir = "../data/rooms/"
    feature_dir_dict = "../data/feature_dict"

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
    def get_dir_dict(self):
        return "../data/rooms_dict"
    def get_feature_dict_dir(self):
        return self.feature_dir_dict

class item_info():
    item_titles = ["lantern", "heavy winter parka", "dusty old map", "tattered notebook",
                "flare gun", "boat paddle", "rescue whistle", "frozen dead hare",
                "can of sweetened condensed milk", "can opener"]
    item_dir = "../data/items/"

    def get_titles(self):
        return self.item_titles
    def get_dir(self):
        return self.item_dir
    def get_dir_dict(self):
        return "../data/items_dict"

class save_info():
    temp_save_dir_rooms = "../data/temp_save_game/rooms/"
    temp_save_dir_items = "../data/temp_save_game/items/"
    save_dir = "../data/save_game/"

    def get_temp_save_dir_rooms(self):
        return self.temp_save_dir_rooms
    def get_temp_save_dir_items(self):
        return self.temp_save_dir_items
    def get_save_dir(self):
        return self.save_dir


class verb_info():
    verbs = ["look", "look at", "go", "take", "help", "inventory", 
            "use", "search", "pull", "eat", "read"]

    verb_definitions = { 
            "look": "Will repeat the long description of the room",
            "look at": "<feature or object> Allows you to look at something in the game",
            "go":"Move to another room",
            "take":"Pick up an item",
            "help":"Display this menu",
            "inventory":"Opens your character's inventory",
            "use":"Use an item in your inventory",
            "search":"search a feature to find items",
            "pull":"Pull on a feature in a room",
            "eat":"Your character attempts to eat an item",
            "read":"Your character attempts to read an item"
            }


    def get_verbs(self):
        return self.verbs
    def get_verb_definitions(self):
        return self.verb_definitions
    def get_dir_dict(self):
        return "../data/verbs_dict"
