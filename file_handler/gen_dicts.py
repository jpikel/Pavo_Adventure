"""
Filename - gen_dicts
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - Allows the adding of aliases and creating the dict files
of all aliases, for room/exits, verbs, and features
"""


import json
from collections import OrderedDict
from name_lists import room_info
from name_lists import item_info
from name_lists import verb_info
import os

ROOM_TITLES = room_info().get_titles()

class update():
    def gen_exit_dict(self):
        """
            generates the alias files for room names.  used in the 
            connected_room field of the room file in the possible exits
            and their aliases
            writes the dict to file in /data
        """
        room_dir = room_info().get_dir()
        room_titles = room_info().get_titles()

        exits = OrderedDict()
        try:
            with open(room_info().get_dir_dict(), 'r') as exit_file:
                exits = json.load(exit_file, object_pairs_hook=OrderedDict)
                exit_file.close()
        except Exception, e:
            pass

        room_file_exits = []

        #sync room files to rooms_dict
        for room in room_titles:
            new_dir = os.path.join(room_dir, room)
            with open(new_dir, 'r') as infile:
                room = json.load(infile, object_pairs_hook=OrderedDict)
                connected_rooms = room["connected_rooms"]
                for conn in connected_rooms:
                    connection = room['connected_rooms'][conn]
                    for alias in connection["aliases"]:
                        room_file_exits.append(alias)
                        if alias not in exits:
                            exits.update({alias:connection["title"]})
                infile.close()

        #sync the rooms_dict to all possible room aliases so we don't get out of sync
        for exit in exits:
            if exit not in room_file_exits:
                print(exit + " not found in list of room exits, removing.")
                del exits[exit]
                

        exits = OrderedDict(sorted(exits.items()))

        with open(room_info().get_dir_dict(), 'w') as outfile:
            json.dump(exits, outfile, indent = 1)
            outfile.close()
        print("Done making exits alias dictionary")

    def add_exit_alias(self, title, alias):
        """
            given a room title and alias
            adds the alias if it does not exist to all room files that hold
            the room passed in as a possible exit
            and generates the exit dict file upon exit

        """
        room_connections = room_info().get_connection_list()
        room_dir = room_info().get_dir()

        if title not in room_connections:
            print 'Invalid room name'
            return
        for key, value in room_connections.items():
            if title in value:
                #if the room has a connection to our desired room
                #open the room with the connection
                new_dir = os.path.join(room_dir, key)
                with open(new_dir, 'r') as room_file:
                    room_data = json.load(room_file, object_pairs_hook=OrderedDict)
                    room_file.close()
                #the title we passed in is the key of the dict in connected_rooms
                room = room_data['connected_rooms'][title]
                if alias not in room['aliases']:
                    room['aliases'].append(alias)
                    print("Added alias:"+alias+" to room:"+title+" in file:"+key)
                    #if we are adding data overwrite the previous room file
                    with open(new_dir, 'w') as room_file:
                        json.dump(room_data, room_file, indent=1)
                        room_file.close()
                else:
                    print 'Alias already exists'
        update().gen_exit_dict()

    def gen_item_dict(self):
        """
            iterates through all the item files, collects their aliases
            and puts them into a dict 
                {
                alias:title
                }
            writes that dict out to file in /data folder
        """
        item_dir = item_info().get_dir()
        item_titles = item_info().get_titles()
        items_dict = OrderedDict()
        for item_name in item_titles:
            new_dir = os.path.join(item_dir, item_name)
            with open(new_dir, 'r') as item_file:
                item = json.load(item_file, object_pairs_hook=OrderedDict)
                for alias in item['aliases']:
                    items_dict.update({alias:item_name})
                
        items_dict = OrderedDict(sorted(items_dict.items()))
        with open(item_info().get_dir_dict(), 'w') as outfile:
            json.dump(items_dict, outfile, indent=1)
        
        print ("Done making item dictionary")

    def add_item_alias(self, title, alias):
        """
            given an item's title and alias.  opens the item file to see if the
            alias already exists.  If not adds the alias and then
            regenerates the item's alias dict
        """
        item_titles = item_info().get_titles()
        item_dir = item_info().get_dir()

        if title in item_titles:
            new_dir = os.path.join(item_dir, title)
            with open(new_dir, 'r+') as item_file:
                item = json.load(item_file, object_pairs_hook=OrderedDict)
                if alias not in item['aliases']:
                    item['aliases'].append(alias)
                    item_file.seek(0)
                    json.dump(item, item_file, indent=1)
                    item_file.close()
                    print("Added alias:"+alias+" to item:"+title)
                else:
                    print("Alias already exists for item")
            self.gen_item_dict()
        else:
            print("Invalid item title")

    def gen_feature_dict(self):
        """
            iterates through all the room files.  Collects all the aliases
            for feature 1 and feature 2.  puts them into a dict 
            {
            alias: feature 1 official title
            alias: feature 2 official title
            }
            writes that out to the feature_dict file in /data
        """
        feature_dir = room_info().get_feature_dict_dir()
        room_dir = room_info().get_dir()
        rooms = room_info().get_titles()
        features_dict = OrderedDict()
        room = OrderedDict()

        #open all the room files and gather up each features aliases
        for title in rooms:
            new_dir = os.path.join(room_dir, title)
            with open(new_dir, 'r') as room_file:
                room = json.load(room_file, object_pairs_hook=OrderedDict)
                room_file.close()
            for feature in room['features']:
                feature_1 = room["features"][feature]['title']
                features_dict.update({feature_1:feature_1})
                aliases_1 = room["features"][feature]['aliases']

                for alias in aliases_1:
                    if alias not in features_dict:
                        features_dict.update({alias:feature_1})

        with open(feature_dir, 'w') as features_file:
            json.dump(features_dict, features_file, indent=1)
            features_file.close()
        print("Done making features alias dict")

    def add_feature_alias(self):
        """
            asks the user for the room and the feature, then the alias to add
            opens the room file, gets the appropriate feature. adds the alias to
            the feature if it does not exist
            closes the files
            DOES NOT regenerate the features_dict
        """
        room_title = raw_input("Enter offical room title where feature is located: ")
        feature_title = raw_input("Enter feature title: ")
        alias = self.get_alias()
        room_dir = room_info().get_dir()
        room_titles = room_info().get_titles()
        result = "Added " + alias + " to " + feature_title + " in room " + room_title

        if room_title in room_titles:
            new_dir = os.path.join(room_dir, room_title)
            with open(new_dir, 'r') as room_file:
                room = json.load(room_file, object_pairs_hook=OrderedDict)
                room_file.close()
                if feature_title in room['features']:
                    if alias not in room['features'][feature_title]['aliases']:
                        room['features'][feature_title]['aliases'].append(alias)
                        result = alias + " added to room " + room_title + "'s " + feature_title
                        with open(new_dir, 'w') as room_file:
                            json.dump(room, room_file, indent = 1)
                            room_file.close()

                    else:
                        result = alias + " already exists"
                else:
                    result = "Feature does not exist"
        else:
            result = "Room does not exist"

        print(result)

        

    def get_title(self):
        return raw_input("Enter the official title: ")

    def get_alias(self):
        return raw_input("Enter the desired alias: ")

    def get_vars(self):
        return self.get_title(), self.get_alias()

    def add_verb_alias(self):
        """
            asks the user to enter an official verb and alias
            if the alias does not exist in the dict adds it
            {
            alias:verb
            }
        """
        verbs = verb_info().get_verbs()
        verb = raw_input("Enter the official verb: ")
        alias = raw_input("Enter the alias: ")
        if verb in verbs:
            with open(verb_info().get_dir_dict(), 'r') as verb_file:
                verb_dict = json.load(verb_file, object_pairs_hook=OrderedDict)
                verb_file.close()
                if alias not in verb_dict:
                    verb_dict.update({alias:verb})
                    verb_dict = OrderedDict(sorted(verb_dict.items()))
                    with open(verb_info().get_dir_dict(), 'w') as verb_file:
                        json.dump(verb_dict, verb_file, indent=1)
                        verb_file.close()
                        print("verb dict updated")
                else:
                    print("Alias already stored")
        else:
            print("Not an official verb")


    def main(self):
        """
            prints a menu that the user can select from for the appropriate action
        """
        number = raw_input("\nWhat would you like to do?\n"
                "1. Add room alias\n"
                "2. Add item alias\n"
                "3. Generate item dictionary\n"
                "4. Generate room dictionary\n"
                "5. Add verb alias\n"
                "6. Add feature alias\n"
                "7. Generate feature dictionary\n"
                "q. Back\n"
                "\n:")

        if number == "1":
            title_alias = self.get_vars()
            self.add_exit_alias(title_alias[0], title_alias[1])
        elif number == "2":
            title_alias = self.get_vars()
            self.add_item_alias(title_alias[0], title_alias[1])
        elif number == "3":
            self.gen_item_dict()
        elif number == "4":
            self.gen_exit_dict()
        elif number == "5":
            self.add_verb_alias()
        elif number == "6":
            self.add_feature_alias()
        elif number == "7":
            self.gen_feature_dict()
        elif number == "q":
            return
        self.main()

def main():
    update().main()

if __name__ == "__main__":
    main()
