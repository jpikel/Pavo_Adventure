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
import types
import io 
import re
import sys

NOT_ALLOWED = ["title", "id"]
TOP_LEVEL = ["long_description", "short_description", "items_in_room"]
FILES_TO_IGNORE = ["Rooms.md", "Items.md"]
SRC_DIR = room_info().get_dir()
ROOM_TITLES = room_info().get_titles()

def mod_rooms():
    """
    will iterate through the entire json of a room
    allowing the user to add to the fields of all the key words
    that are considered editable
    the source dir is /data/rooms/
    """
    while True:
        filename = raw_input("Enter template room to edit, q to quit: ")
        filename = str(filename)
        if filename == "q":
            break
        if filename not in FILES_TO_IGNORE and filename in ROOM_TITLES:
            new_dir = os.path.join(SRC_DIR, filename)
            print new_dir
            with open(new_dir, 'r') as open_file:
                try:
                    str_ = open_file.read()
                    #deal with nasty nasty single quotes!
                    str_ = str_.replace("\u2019", "'")
                    room = json.loads(str_, object_pairs_hook=OrderedDict)
                    #room = json.load(open_file, object_pairs_hook=OrderedDict)
                    open_file.close()
                    room = edit_room(room)
                    #print(room)
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
        if key is not NOT_ALLOWED and key in TOP_LEVEL:
            text = edit_loop(key, room)
            if text == 'q':
                return room
            elif text != 'n':
                if isinstance(room[key], basestring):
                    room[key] = text
                elif isinstance(room[key], list) and text not in room[key]:
                    #do not allow duplicates
                    room[key].append(text)
                elif isinstance(room[key], dict):
                    print "ERROR! I can't handle dicts yet"


    for feature in room['features']:
        verbs = room['features'][feature]['verbs']
        for verb in verbs:
            print "\n Now editing " + verb + " in feature " + feature
            text = edit_loop('description', verbs[verb])
            if text == 'q':
                return room
            elif text != 'n':
                verbs[verb]['description'] = text

    return room


def edit_loop(key, this_pair):
    """
    this loop will ask the user to allow edits
    """
    while True:
        print "\n" + str(key) + ": " + str(this_pair[key])
        ch = raw_input("\nEdit y/n/q? ")
        ch = ch.lower()
        if ch == "y":
            while True:
                try:
                    text = raw_input("\nEnter new value: ")
                except Exception, e:
                    print e
                print "\nYou entered: " + text
                ch = raw_input("\n\nAccept y/n? ")
                if ch == "y":
                    return text
        elif ch == "n":
            return ch
        elif ch == 'q':
            return 'q'


def store_room(room):
    """
    store the json into the room template folders /data/rooms/
    """
    new_dir = os.path.join(SRC_DIR, room['title'])
    with open(new_dir, "w") as open_file:
        str_ = json.dumps(room, indent=4)
        str_ = str_.replace("\u2019", "'")
        open_file.write(str_)
        open_file.close()
    return

    


#references:
#https://stackoverflow.com/questions/25231989/how-to-check-if-a-variable-is-a-dictionary-in-python

#https://stackoverflow.com/questions/19591458/python-reading-from-a-file-and-saving-to-utf-8

#https://stackoverflow.com/questions/1254454/fastest-way-to-convert-a-dicts-keys-values-from-unicode-to-str
