
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


class item_info():
    item_titles = ["Lantern", "Heavy Winter Parka", "Dusty Old Map", "Tattered Notebook",
                "Flare Gun", "Boat Paddle", "Rescue Whistle", "Frozen Dead Hare",
                "Can of Sweetened Condensed Milk", "Can Opener"]
    item_dir = "../data/items/"

    def get_titles(self):
        return self.item_titles
    def get_dir(self):
        return self.item_dir
