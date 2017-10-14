"""
Filename - file_lib.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description -
"""
#from __future__ import print_function
import shutil #for file handling
import json
import os
import logging
import sys
from collections import OrderedDict
from name_lists import save_info
from name_lists import room_info
from name_lists import item_info

IGNORE = ["TempSaveGame.md", "Rooms.md", "Items.md"]

def new_game():
    """
    First cleans both the rooms and items folders in the temporary save
    directory.  Then copies the original template files from
    the data folder to the temp save folder for rooms and items
    """
    print("Preparing to make new game")
    src_dir = room_info().get_dir()
    dst_dir = save_info().get_temp_save_dir_rooms()
    copy_files(src_dir, dst_dir)
    src_dir = item_info().get_dir()
    dst_dir = save_info().get_temp_save_dir_items()
    copy_files(src_dir, dst_dir)


def copy_files(src_dir, dst_dir):
    """
    attemps to copy all the files from the source to the destination
    except those in the IGNORE list
    """
    try:
        print("Cleaning" + dst_dir)
        clean_dir(dst_dir)
        print("Copying from " +src_dir+ "\nto temp " + dst_dir)
        for item in os.listdir(src_dir):
            if item not in IGNORE:
                src = os.path.join(src_dir, item)
                dst = os.path.join(dst_dir, item)
                shutil.copy2(src,dst)
    except Exception, e:
        print("Something went horribly wrong creating the temp save file")
        print(e)

def clean_dir(dst_dir):
    """
    removes all the files in the directory passed in except those in the
    IGNORE list
    """
    try:
        for item in os.listdir(dst_dir):
            if item not in IGNORE:
                to_del = os.path.join(dst_dir, item)
                os.remove(to_del)
    except Exception, e:
        print("Something went wrong cleaning the directory")
        print(e)

def load_room(room_title):
    """
    opens the room passed in from the temporary save folder.
    reads in the contents and returns the dict
    """
    try:
        room_path = combine_temp_room_path(room_title)
        with open(room_path, 'r') as room_file:
            room = json.load(room_file, object_pairs_hook=OrderedDict)
            room_file.close()
        return room
    except Exception, e:
        return e

def store_room(current_room):
    """
    writes out the current room to its file as a string in the form as json
    to the appropriate room file in the temp save folder
    overwrites the file

    """
    try:
        room_title = current_room['title']
        current_room['visited'] = True
        room_path = combine_temp_room_path(room_title)
        with open(room_path, 'w') as room_file:
            room_file.seek(0)
            json.dump(current_room, room_file, indent=4)
            room_file.close()
    except Exception, e:
        raise e

def combine_temp_room_path(room_title):
    """
    returns a path to the temp room dir and the room title
    """
    room_path = save_info().get_temp_save_dir_rooms()
    room_path = os.path.join(room_path, room_title)
    return room_path

def load_item(title):
    """
    returns a complete item structure
    """
    try:
        item_path = combine_temp_item_path(title)
        with open(item_path, 'r') as item_file:
            item = json.load(item_file, object_pairs_hook=OrderedDict)
            item_file.close()
        return item
    except Exception, e:
        return e

def store_item(current_item):
    """
    write an item out to the temp save dir
    """
    try:
        item_title = current_item['title']
        current_item['visited'] = True
        item_path = combine_temp_item_path(item_title)
        with open(item_path, 'w') as item_file:
            item_file.seek(0)
            json.dump(current_item, item_file, indent=4)
            item_file.close()
    except Exception, e:
        raise e

def combine_temp_item_path(title):
    """
    returns path to the temp item dir and the item's title
    """
    item_path = save_info().get_temp_save_dir_items()
    item_path = os.path.join(item_path,title)
    return item_path




#Reference - https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
