"""
Filename - data_entry.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description -
"""

from file_handler.name_lists import room_info
from collections import OrderedDict
import os
import json

NOT_ALLOWED = ["title", "id"]
FILES_TO_IGNORE = ["Rooms.md", "Items.md"]
SRC_DIR = room_info().get_dir()

def mod_rooms():
    """
    will iterate through the entire json of a room
    allowing the user to add to the fields of all the key words
    that are considered editable
    the source dir is /data/rooms/
    """
    for filename in os.listdir(SRC_DIR):
        if filename not in FILES_TO_IGNORE and not filename.endswith("swp"):
            new_dir = os.path.join(SRC_DIR, filename)
            print new_dir
            with open(new_dir, 'r') as open_file:
                try:
                    room = json.load(open_file, object_pairs_hook=OrderedDict)
                    open_file.close()
                    room = edit_room(room)
                    store_room(room)
                except Exception, e:
                    print e

def edit_room(room):
    """
    This is the function where the user may edit the room
    Expects a json of a room object
    """

    #top level first
    for key in room:
        room[key] = edit_loop(key, room)
        print "key:value now"
        print key + " : " + room[key]

    return room


def edit_loop(key, room):
    """
    this loop will ask the user to allow edits
    """
    while True:
        print key + ": " + room[key]
        ch = raw_input("Edit y/n? ")
        ch = ch.lower()
        if ch == "y":
            while True:
                text = raw_input("Enter new value: ")
                print "You entered: " + text
                ch = raw_input("Accept y/n? ")
                if ch == "y":
                    return text
        elif ch == "n":
            return room[key]
def store_room(room):
    """
    store the json into the room template folders /data/rooms/
    """
    new_dir = os.path.join(SRC_DIR, room['title'])
    with open(new_dir, "w") as open_file:
        json.dump(room, open_file, indent=4)
        open_file.close()
    return
