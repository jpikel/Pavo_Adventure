"""
Filename - name_lists.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - 
"""

class room_info():
    room_titles = ["Shore", "Crash Site", "Game Trail", "Field", "Dense Brush", "Camp", "Woods",
        "Cave", "Mountain Base", "Fire Tower", "River", "Waterfall", "Mountain Ascent", 
        "Mountain Summit", "Rapids", "Ranger Station"]
    room_connections = [1,3,2,2,2,3,3,2,2,1,3,1,2,2,2,1]
    room_dir = "../data/rooms/"

    #This list only used if we need to recreate empty rooms
    room_connection_list = {"Shore":["Crash Site"],
            "Crash Site":["Shore", "Camp", "Game Trail"],
            "Game Trail":["Crash Site", "Cave"],
            "Field":["Mountain Base", "Dense Brush"],
            "Dense Brush":["Field", "Camp"],
            "Camp":["Dense Brush", "Woods", "Crash Site"],
            "Woods":["Camp", "River", "Cave"],
            "Cave":["Woods", "Game Trail"],
            "Mountain Base":["Mountain Ascent", "Field"],
            "Fire Tower":["Mountain Summit"],
            "River":["Rapids", "Waterfall", "Woods"],
            "Waterfall":["River"],
            "Mountain Ascent":["Mountain Summit", "Mountain Base"],
            "Mountain Summit":["Mountain Ascent", "Fire Tower"],
            "Rapids":["Ranger Station", "River"],
            "Ranger Station":["Rapids"]}

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

class item_info():
    item_titles = ["Lantern", "Heavy Winter Parka", "Dusty Old Map", "Tattered Notebook",
                "Flare Gun", "Boat Paddle", "Rescue Whistle", "Frozen Dead Hare",
                "Can of Sweetened Condensed Milk", "Can Opener"]
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
