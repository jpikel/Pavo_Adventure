"""
Filename - 
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - 
"""

from collections import OrderedDict
import json
from name_lists import room_info

def update_aliases():

    room_conn_list = room_info().get_connection_list()
    room_titles = room_info().get_titles()

    for title in room_titles:
        with open(room_info().get_dir()+title, 'r+') as outfile:
            room = json.load(outfile, object_pairs_hook=OrderedDict)
            connected_rooms = room['connected_rooms']
            for other_room in connected_rooms:
                aliases = room_info().get_aliases(other_room['title'])
                if aliases is not None:
                    for alias in aliases:
                        if alias not in other_room['aliases']:
                            other_room['aliases'].append(alias)
            outfile.seek(0)
            json.dump(room, outfile, indent=4)

    print("Done updating room aliases")

#update_aliases()
