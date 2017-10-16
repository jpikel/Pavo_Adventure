"""
Filename - data_entry.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description -
"""

from file_handler.name_lists import room_info
from file_handler.name_lists import item_info
from collections import OrderedDict
import os
import json
import types
import io 
import re
import sys

NOT_ALLOWED = ["title", "id"]
ROOM_TOP_LEVEL = ["long_description", "short_description", "items_in_room"]
ITEM_TOP_LEVEL = []
FILES_TO_IGNORE = ["Rooms.md", "Items.md"]
ROOM_SRC_DIR = room_info().get_dir()
ROOM_TITLES = room_info().get_titles()
ITEM_SRC_DIR = item_info().get_dir()
ITEM_TITLES = item_info().get_titles()

def mod_rooms():
    """
    will iterate through the entire json of a room
    allowing the user to add to the fields of all the key words
    that are considered editable
    the source dir is /data/rooms/
    """
    while True:
        filename = raw_input("Enter template room or item to edit, q to quit: ")
        filename = str(filename)
        if filename in ROOM_TITLES:
            src_dir = ROOM_SRC_DIR
        elif filename in ITEM_TITLES:
            src_dir = ITEM_SRC_DIR
        if filename == "q":
            break
        if (filename not in FILES_TO_IGNORE and 
                filename in ROOM_TITLES or filename in ITEM_TITLES):
            new_dir = os.path.join(src_dir, filename)
            print new_dir
            with open(new_dir, 'r') as open_file:
                try:
                    str_ = open_file.read()
                    #deal with nasty nasty single quotes!
                    #see additional note in function below store_room
                    #str_ = str_.replace("\u2019", "'")
                    json_obj = json.loads(str_, object_pairs_hook=OrderedDict)
                    #room = json.load(open_file, object_pairs_hook=OrderedDict)
                    open_file.close()
                    if filename in ROOM_TITLES:
                        json_obj = edit_room(json_obj)
                    else:
                        json_obj = edit_item(json_obj)
                    store_obj(json_obj, src_dir)
                except Exception, e:
                    print e

def edit_room(room):
    """
    This is the function where the user may edit the room
    Expects a json of a room object
    """

    #top level first
    for key in room:
        if key is not NOT_ALLOWED and key in ROOM_TOP_LEVEL:
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
    #edit the features title and the verbs descriptions
    for feature in room['features']:
        verbs = room['features'][feature]['verbs']
        print "\n Now editing feature " + feature
        text = edit_loop('title', room['features'][feature])
        if text == 'q':
            return room
        elif text != 'n':
            room['features'][feature]['title'] = text
        #edit that features verbs description fields
        for verb in verbs:
            print "\n Now editing " + verb + " in feature " + feature
            verbs = edit_verb(verbs, verb)

    return room

def edit_item(item):
    """
    This function is where the user may edit a few of the fields in the 
    item and the verbs contained in that item
    """
    #an item does not have any editable top level fields at the moment
    #at least not ones we want to edit it here
    #for key in item:
     #   if key is not NOT_ALLOWED and key in ITEM_TOP_LEVEL:

    verbs = item['verbs']
    for verb in verbs:
        print "\nNow editing " + verb + " in " + item['title']
        verbs = edit_verb(verbs, verb)
    return item

def edit_verb(verbs, verb):
    """
    edit the description of each verb in the json obj
    """
    text = edit_loop('description', verbs[verb])
    if text == 'q':
        return verbs 
    elif text != 'n':
        verbs[verb]['description'] = text
    return verbs


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


def store_obj(obj_json, src_dir):
    """
    store the json into the src_dir
    """
    new_dir = os.path.join(src_dir, obj_json['title'])
    with open(new_dir, "w") as open_file:
        str_ = json.dumps(obj_json, indent=4)
        str_ = the_replacer(str_)
        open_file.write(str_)
        open_file.close()
    return

def the_replacer(str_):
    """
    searchs through the string and replaces certain unicode strings
    """
    #single quotes in an inputted string were being converted to a 
    #unicode sequence that the terminal could not understand
    #so forcefully change them into a single quote here and
    #then write the json out to file
    #after this happens subsequent load and dump should be ok
    #2019 is right single quote
    #2018 is left single quote
    #201c is left double quote
    #201d is right double quote
    str_ = str_.replace("\u2019", "'")
    str_ = str_.replace("\u2018", "'")
    str_ = str_.replace("\u201c", r"\"")
    str_ = str_.replace("\u201d", r"\"")
    return str_



#references:
#https://stackoverflow.com/questions/25231989/how-to-check-if-a-variable-is-a-dictionary-in-python

#https://stackoverflow.com/questions/19591458/python-reading-from-a-file-and-saving-to-utf-8

#https://stackoverflow.com/questions/1254454/fastest-way-to-convert-a-dicts-keys-values-from-unicode-to-str
