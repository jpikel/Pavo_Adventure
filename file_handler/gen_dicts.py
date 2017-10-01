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

class update():
    def gen_exit_dict(self):
        room_dir = room_info().get_dir()
        room_titles = room_info().get_titles()

        with open('../data/exits_dict', 'r') as exit_file:
            exits = json.load(exit_file, object_pairs_hook=OrderedDict)
            for room in room_titles:
                with open(room_dir + room, 'r') as infile:
                    room = json.load(infile, object_pairs_hook=OrderedDict)
                    connected_rooms = room["connected_rooms"]
                    for connection in connected_rooms:
                        for alias in connection["aliases"]:
                            if alias not in exits:
                                exits.update({str(alias):str(connection["title"])})
                    infile.close()

            exit_file.close()

        exits = OrderedDict(sorted(exits.items()))

        with open("../data/exits_dict", 'w') as outfile:
            json.dump(exits, outfile, indent = 4)
            outfile.close()

        print("Done making exits alias dictionary")

    def add_exit_alias(self, title, alias):
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
                                        print("alias:"+alias+" to room:"+title+" in file:"+key)
                            room_file.seek(0)
                            json.dump(room_data, room_file, indent=4)
                            room_file.close()
            update().gen_exit_dict()
        else:
            print("Invalid room title")

    def gen_item_dict(self):
        item_dir = item_info().get_dir()
        item_titles = item_info().get_titles()

        items_dict = OrderedDict()

        for item in item_titles:
            items_dict.update({item:item})

        with open("../data/items_dict", 'w') as outfile:
            json.dump(items_dict, outfile, indent=4)

    def add_item_alias(self, title, alias):
        item_titles = item_info().get_titles()

        with open("../data/items_dict", 'r+') as outfile:
            items_dict = json.load(outfile, object_pairs_hook=OrderedDict)
            if title in item_titles:
                if alias not in items_dict:
                    print("adding alias: "+alias+ " with title: "+title)
                    items_dict.update({alias:title})
                    items_dict = OrderedDict(sorted(items_dict.items()))
                    outfile.seek(0)
                    json.dump(items_dict, outfile, indent=4)
                else:
                    print("alias already exists in dict")
            else:
                print("invalid title, item does not exist")

            outfile.close()

update().add_exit_alias("Camp", "campsite")
#update().gen_exit_dict()
