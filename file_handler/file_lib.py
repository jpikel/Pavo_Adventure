"""
Filename - file_lib.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - This file handles a lot of reads and writes out to file.  Also handles
the save game and load game when it comes to moving the files into their appropriate
locations for use by the game engine.
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
ROOM_TITLES = room_info().get_titles()
ITEM_TITLES = item_info().get_titles()
ROOM_DIR = room_info().get_dir()
TEMP_ROOM_DIR = save_info().get_temp_save_dir_rooms()
ITEM_DIR = item_info().get_dir()
TEMP_ITEM_DIR = save_info().get_temp_save_dir_items()
SAVE_DIR = save_info().get_save_dir()
SAVE_ROOM_DIR = save_info().get_save_dir_rooms()
SAVE_ITEM_DIR = save_info().get_save_dir_items()
DEBUG_SAVE_LOAD = 0

def new_game():
    """
    First cleans both the rooms and items folders in the temporary save
    directory.  Then copies the original template files from
    the data folder to the temp save folder for rooms and items
    """
    #comment out when in production
    if DEBUG_SAVE_LOAD: print("Preparing to make new game")
    #make the temp rooms files if it does not exist then clean it
    src_dir = ROOM_DIR
    dst_dir = TEMP_ROOM_DIR
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    #comment out in production
    if DEBUG_SAVE_LOAD: print("Cleaning" + dst_dir)
    clean_dir(dst_dir)
    #copy the official rooms to the temp save
    copy_files(src_dir, dst_dir)

    #if the items dir does not exist make it, then clean it and copy the items
    src_dir = ITEM_DIR
    dst_dir = TEMP_ITEM_DIR
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    #comment out in production
    if DEBUG_SAVE_LOAD: print("Cleaning" + dst_dir)
    clean_dir(dst_dir)
    copy_files(src_dir, dst_dir)

    #confirm all the files go copied to the temp dirs for rooms and items
    if val_room_files_in_temp() and val_item_files_in_temp():
        return True
    return False


def copy_files(src_dir, dst_dir):
    """
    attemps to copy all the files from the source to the destination
    except those in the IGNORE list
    """
    try:
        #comment out in production
        if DEBUG_SAVE_LOAD: print("Copying from " +src_dir+ "\nto " + dst_dir)
        for item in os.listdir(src_dir):
            if item not in IGNORE:
                src = os.path.join(src_dir, item)
                if os.path.isfile(src):
                    dst = os.path.join(dst_dir, item)
                    shutil.copy2(src,dst)
    except Exception, e:
        print("Something went horribly wrong creating the temp save file")
        print(e)

def save_game(player, current_room, turns):
    """
    saves the game to the Save Game dir
    expects to receive the player class object and the current room object
    when called, returns True on success
    """
    #convert the player class object to a dict for easy handling
    try:
        player_dict = player.__dict__
        player_dict['current_room'] = current_room['title']
        player_dict['turns'] =  turns
        #store the current room out to the temp save dir so we can copy it all 
        #at once
        store_room(current_room)
        #remove the save game dirs
        #clean up the room dir if it exists otherwisre make it
        if os.path.isdir(SAVE_ROOM_DIR):
            clean_dir(SAVE_ROOM_DIR)
        else:
            os.makedirs(SAVE_ROOM_DIR)
        #clean up the items dir if it exists otherwise make it
        if os.path.isdir(SAVE_ITEM_DIR):
            clean_dir(SAVE_ITEM_DIR)
        else:
            os.makedirs(SAVE_ITEM_DIR)
        #if the 'player' file exists in save_game delete it!

        player_file = os.path.join(SAVE_DIR, 'player')
        if os.path.exists(player_file):
            os.remove(player_file)
        #copy all the files from the temp dir to the save game dirs
        copy_files(TEMP_ROOM_DIR, SAVE_ROOM_DIR)
        copy_files(TEMP_ITEM_DIR, SAVE_ITEM_DIR)
        #write out the player
        with open(player_file, 'w') as open_file:
            json.dump(player_dict, open_file, indent=1)
            open_file.close()
        return True, True
    except Exception, e:
        return False, e

def load_game():
    """
    moves the files in the Save game dir to the temp save dir
    only if the save game dir exists
    returns the player as a dict and the current room as a dict
    """
    success = True
    msg = []
    #check if /data/save_game exits
    #otherwise run a new game and return the shore, but no player
    if not os.path.isdir(SAVE_DIR):
        new_game()
        return None, load_room('shore'), False, 'No save game found starting new game'
    #if the temp room dir does not exist make it
    if not os.path.isdir(TEMP_ROOM_DIR):
        os.makedirs(TEMP_ROOM_DIR)
    else:
        clean_dir(TEMP_ROOM_DIR)
    #if the temp item dir does not exist make it
    if not os.path.isdir(TEMP_ITEM_DIR):
        os.makedirs(TEMP_ITEM_DIR)
    else:
        clean_dir(TEMP_ITEM_DIR)
    #if the room dir in save game does not exist 
    #copy the templates instead
    if not os.path.isdir(SAVE_ROOM_DIR):
        copy_files(ROOM_DIR, TEMP_ROOM_DIR)
        success = False
        msg.append('Rooms not found using new rooms.')
    else:
        copy_files(SAVE_ROOM_DIR, TEMP_ROOM_DIR)
    #if the item dir in save game does not exist copy the templates instead
    if not os.path.isdir(SAVE_ITEM_DIR):
        copy_files(ITEM_DIR, TEMP_ITEM_DIR)
        success = False
        msg.append('Items not found using new items.')
    else:
        copy_files(SAVE_ITEM_DIR, TEMP_ITEM_DIR)

    #after copying the files make sure all the room files are in the temp dir
    #as expected
    #if either of these fails for any reason they will return False
    if not val_room_files_in_temp() or not val_item_files_in_temp():
        msg.append('Warning not all files copied.')
        success = False

    player_file = os.path.join(SAVE_DIR, 'player')
    player = None
    if os.path.exists(player_file):
        with open(player_file, 'r') as open_file:
            player = json.load(open_file)
            open_file.close()

    if player:
        current_room = load_room(player['current_room'])
        del player['current_room']
    else:
        success = False
        msg.append('Player file not found start new player.')
        current_room = load_room('shore')

    return player, current_room, success, msg


def val_room_files_in_temp():
    """
    confirms that all the room files exist in the temp dir
    if the room does not exist copies it from the template dir
    """
    try:
        list_of_things = []
        for thing in os.listdir(TEMP_ROOM_DIR):
            if thing not in IGNORE:
                list_of_things.append(thing)

        for element in ROOM_TITLES:
            if element not in list_of_things:
                src_dir = os.path.join(ROOM_DIR, element)
                shutil.copy2(src_dir, TEMP_ROOM_DIR)
        return True
    except Exception, e:
        return False

def val_item_files_in_temp():
    """
    confirms that all the item files exist in the temp dir
    if the item does not exist copies it from the template dir
    """
    try:
        list_of_things = []
        for thing in os.listdir(TEMP_ITEM_DIR):
            if thing not in IGNORE:
                list_of_things.append(thing)
        for element in ITEM_TITLES:
            if element not in list_of_things:
                src_dir = os.path.join(ITEM_DIR, element)
                shutil.copy2(src_dir, TEMP_ITEM_DIR)
        return True
    except Exception, e:
        return False


def clean_dir(dst_dir):
    """
    removes all the files in the directory passed in except those in the
    IGNORE list
    """
    if os.path.isdir(dst_dir):
        try:
            for item in os.listdir(dst_dir):
                if item not in IGNORE:
                    to_del = os.path.join(dst_dir, item)
                    os.remove(to_del)
            return True
        except Exception, e:
            print("Something went wrong cleaning the directory")
            print(e)
            return False
    else:
        return False

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
        #cannot set room to visited here. because this function is called
        #by other functions when editing a room
        #current_room['visited'] = True
        room_path = combine_temp_room_path(room_title)
        with open(room_path, 'w') as room_file:
            room_file.seek(0)
            json.dump(current_room, room_file, indent=1)
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
        item_path = combine_temp_item_path(item_title)
        with open(item_path, 'w') as item_file:
            item_file.seek(0)
            json.dump(current_item, item_file, indent=1)
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

def merge(updates, original):
    """
        takes the updates and puts them into the original dict
        be very careful using this can quickly overwrite an entire 
        structure. Has no safe guards at the moment.
    """
    for key, value in updates.items():
        #if the value of the key is a dict and
        #if the dict beyond is empty and it is in the destination
        #delete the key in the destination
        if isinstance(value, dict) and not bool(updates[key]) and key in original:
            original.pop(key, None)
        #if it a dict with stuff in it then enter the dict and recurse
        elif isinstance(value, dict):
            node = original.setdefault(key,  {})
            merge(value, node)
        #otherwise assign the dict    
        else:
            original[key] = value
    return original

def get_order(source):
    """
        given a dict returns a list of the keys in the top level of the
        dict
    """
    order = source.items()
    order_list = []
    for key in order:
        order_list.append(key[0])
    return order_list


def update(updates, original):
    """
    driver function gets the top level sorted order of an OrderedDict
    Then merges the updates into the original dict
    then re-sorts the new dict by the keys from the original order
    then returns the newly merged and sorted dict
    """
    source_order = get_order(original)
    merged = merge(updates, original)
    sorted_d = OrderedDict(sorted(merged.items(), key=lambda i:source_order.index(i[0])))
    return sorted_d

def gather_dicts(source, key):
    """
    for the key passed in if the value is a dict returns that dict or list of dicts
    """
    if key in source and isinstance(source[key], list) or isinstance(source[key], dict):
        return source[key]
    else:
        return None

def add_key_before_dicts(source, key, top_key):
    """
    when passed in a source dict structure, the key is the new key of the dict
    top_key is the existing key in the file
    creates a new structured dict that is returned
    top_key: { key[value]: obj }
    """
    new_dict = OrderedDict()
    for obj in source:
        new_dict.update({obj[key]:obj})

    updated_dict = OrderedDict()
    updated_dict.update({top_key:new_dict})
    return updated_dict



#reference https://stackoverflow.com/questions/20656135/python-deep-merge-dictionary-data
#Reference - https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
