"""
Filename - 
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - 
"""


import json
from collections import OrderedDict
from name_lists import room_info
from name_lists import item_info
from name_lists import verb_info

class update():
    def gen_exit_dict(self):
        """
        Function - 
        Parameters - 
        Preconditions - 
        Postconditions - 
        Description - 
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

        for room in room_titles:
            with open(room_dir + room, 'r') as infile:
                room = json.load(infile, object_pairs_hook=OrderedDict)
                connected_rooms = room["connected_rooms"]
                for connection in connected_rooms:
                    for alias in connection["aliases"]:
                        if alias not in exits:
                            exits.update({str(alias):str(connection["title"])})
                infile.close()

        exits = OrderedDict(sorted(exits.items()))

        with open(room_info().get_dir_dict(), 'w') as outfile:
            json.dump(exits, outfile, indent = 4)
            outfile.close()
        print("Done making exits alias dictionary")

    def add_exit_alias(self, title, alias):
        """
        Function - 
        Parameters - 
        Preconditions - 
        Postconditions - 
        Description - 
        """
        room_connections = room_info().get_connection_list()
        room_dir = room_info().get_dir()

        if title in room_connections:
            for key, value in room_connections.items():
                for room in value:
                    if room == title:
                        with open(room_dir+key, 'r+') as room_file:
                            room_data = json.load(room_file, object_pairs_hook=OrderedDict)
                            room_data_conn = room_data['connected_rooms']
                            for room in room_data_conn:
                                if title == room['title']:
                                    if alias not in room['aliases']:
                                        room['aliases'].append(alias)
                                        print("Added alias:"+alias+" to room:"+title+" in file:"+key)
                            room_file.seek(0)
                            json.dump(room_data, room_file, indent=4)
                            room_file.close()
            update().gen_exit_dict()
        else:
            print("Invalid room title")

    def gen_item_dict(self):
        """
        Function - 
        Parameters - 
        Preconditions - 
        Postconditions - 
        Description - 
        """
        item_dir = item_info().get_dir()
        item_titles = item_info().get_titles()

        items_dict = OrderedDict()

        for item_name in item_titles:
            with open(item_dir+item_name, 'r') as item_file:
                item = json.load(item_file, object_pairs_hook=OrderedDict)
                for alias in item['aliases']:
                    items_dict.update({alias:item_name})
                
        items_dict = OrderedDict(sorted(items_dict.items()))
        with open(item_info().get_dir_dict(), 'w') as outfile:
            json.dump(items_dict, outfile, indent=4)
        
        print ("Done making item dictionary")

    def add_item_alias(self, title, alias):
        """
        Function - 
        Parameters - 
        Preconditions - 
        Postconditions - 
        Description - 
        """
        item_titles = item_info().get_titles()
        item_dir = item_info().get_dir()

        if title in item_titles:
            with open(item_dir + title, 'r+') as item_file:
                item = json.load(item_file, object_pairs_hook=OrderedDict)
                if alias not in item['aliases']:
                    item['aliases'].append(alias)
                    item_file.seek(0)
                    json.dump(item, item_file, indent=4)
                    item_file.close()
                    print("Added alias:"+alias+" to item:"+title)
                else:
                    print("Alias already exists for item")
            self.gen_item_dict()
        else:
            print("Invalid item title")

    def gen_feature_dict(self):
        """
        Function - 
        Parameters - 
        Preconditions - 
        Postconditions - 
        Description - 
        """
        feature_dir = room_info().get_feature_dict_dir()
        room_dir = room_info().get_dir()
        rooms = room_info().get_titles()
        features_dict = OrderedDict()
        room = OrderedDict()

        for title in rooms:
            with open(room_dir + title, 'r') as room_file:
                room = json.load(room_file, object_pairs_hook=OrderedDict)
                room_file.close()
            feature_1 = room['feature_1_title']
            feature_2 = room['feature_2_title']
            features_dict.update({feature_1:feature_1})
            features_dict.update({feature_2:feature_2})
            aliases_1 = room['feature_1_aliases']
            aliases_2 = room['feature_2_aliases']

            for alias in aliases_1:
                if alias not in features_dict:
                    features_dict.update({alias:feature_1})
            for alias in aliases_2:
                if alias not in features_dict:
                    features_dict.update({alias:feature_2})

        with open(feature_dir, 'w') as features_file:
            json.dump(features_dict, features_file, indent=4)
            features_file.close()
        print("Done making features alias dict")

    def add_feature_alias(self):
        """
        Function - 
        Parameters - 
        Preconditions - 
        Postconditions - 
        Description - 
        """
        room_title = raw_input("Enter offical room title: ")
        feature_title = raw_input("Enter feature title: ")
        alias = self.get_alias()
        room_dir = room_info().get_dir()
        room_titles = room_info().get_titles()
        result = "Added " + alias + " to " + feature_title + " in room " + room_title

        if room_title in room_titles:
            with open(room_dir + room_title, 'r') as room_file:
                room = json.load(room_file, object_pairs_hook=OrderedDict)
                if feature_title == room['feature_1_title']:
                    if alias not in room['feature_1_aliases']:
                        room['feature_1_aliases'].append(alias)
                        result = alias + " added to room " + room_title + "'s " + feature_title
                    else:
                        result = alias + " already exists"
                elif feature_title == room['feature_2_title']:
                    if alias not in room['feature_2_aliases']:
                        room['feature_2_aliases'].append(alias)
                        result = alias + " added to room " + room_title + "'s " + feature_title
                    else:
                        result = alias + " already exists"
                else:
                    result = "Feature does not exist"
                room_file.close()
                with open(room_dir + room_title, 'w') as room_file:
                    json.dump(room, room_file, indent = 4)
                    room_file.close()
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
        verbs = verb_info().get_verbs()
        verb = raw_input("Enter the official verb: ")
        alias = raw_input("Enter the alias: ")
        if verb in verbs:
            with open(verb_info().get_dir_dict(), 'r+') as verb_file:
                verb_dict = json.load(verb_file, object_pairs_hook=OrderedDict)
                if alias not in verb_dict:
                    verb_dict.update({alias:verb})
                    verb_dict = OrderedDict(sorted(verb_dict.items()))
                    verb_file.seek(0)
                    json.dump(verb_dict, verb_file, indent=4)
                    print("verb dict updated")
                else:
                    print("Alias already stored")
                verb_file.close()
        else:
            print("Not an official verb")


    def main(self):
        """
        Function - 
        Parameters - 
        Preconditions - 
        Postconditions - 
        Description - 
        """
        number = raw_input("\nWhat would you like to do?\n"
                "1. Add room alias\n"
                "2. Add item alias\n"
                "3. Generate item dictionary\n"
                "4. Generate room dictionary\n"
                "5. Add verb alias\n"
                "6. Add feature alias\n"
                "7. Generate feature dictionary\n"
                "9. Quit\n")

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
        elif number == "9":
            exit()
        self.main()
            
update().main()
