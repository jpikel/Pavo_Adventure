"""
Filename - file_lib.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - 
"""
from __future__ import print_function
import shutil #for file handling
import json
import os
import logging
import sys
from collections import OrderedDict
from name_lists import save_info
from name_lists import room_info
from name_lists import item_info

ignore = ["TempSaveGame.md", "Rooms.md", "Items.md"]

class response_struct():
    def __init__(self):
        self.response = {
                    "title":None,
                    "description":None,
                    "move":False,
                    "distance_from_room":0
                }

class file_ops():
    def new_game(self):
        #Reference - https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
        src_dir = room_info().get_dir()
        dst_dir = save_info().get_temp_save_dir_rooms()
        self.copy_files(src_dir, dst_dir)
        src_dir = item_info().get_dir()
        dst_dir = save_info().get_temp_save_dir_items()
        self.copy_files(src_dir, dst_dir)


    def copy_files(self, src_dir, dst_dir):
        try:
            self.clean_dir(dst_dir)
            for item in os.listdir(src_dir):
                if item not in ignore:
                    src = os.path.join(src_dir, item)
                    dst = os.path.join(dst_dir, item)
                    shutil.copy2(src,dst)
        except Exception, e:
            print("Something went horribly wrong creating the temp save file")

    def clean_dir(self, dst_dir):
        try:
            for item in os.listdir(dst_dir):
                if item not in ignore:
                    to_del = os.path.join(dst_dir, item)
                    os.remove(to_del)
        except Exception, e:
            print("Something went wrong cleaning the directory")


class room_ops():
    def __init__(self):
        self.current_room = OrderedDict()
        self.temp_dir = save_info().get_temp_save_dir_rooms()
        self.item_not_found = "The cold must be making you delirious, you can't seem to find a " 

    def get_room_title(self):
        return str(self.current_room['title'])

    def get_room_long_desc(self):
        return str(self.current_room['long_description'])

    def get_room_short_desc(self):
        return str(self.current_room['short_description'])

    def get_visited(self):
        return self.current_room['visited']

    def check_connections(self, title_or_direction, items):
        response = response_struct()
        for room in self.current_room['connected_rooms']:
            if title_or_direction == room['title'] or title_or_direction == room['compass_direction']:
                if room['item_required'] == True:
                    if room['item_required_title'] in items:
                        item_dir = save_info().get_temp_save_dir_items() + room['item_required_title']
                        with open(item_dir, 'r') as item_file:
                            item = json.load(item_file, object_pairs_hook=OrderedDict)
                            item_file.close()
                            if item['active'] == True:
                                response['move'] = True
                                response['distance_from_room'] = room['distance_from_room']
                                response['title'] = str(room['title'])
                                return response
                            else:
                                self.response['description'] = str(room['pre_item_description'])
                                return response
                    else:
                        response.response['description'] = str(room['pre_item_description'])
                        return response
                else:
                    response['move'] = True
                    response['distance_from_room'] = room['distance_from_room']
                    response['title'] = str(room['title'])
                    return response

        return response

    def store_room(self):
        try:
            room_title = self.current_room['title']
            self.current_room['visited'] = True
            with open(self.temp_dir+room_title, 'w') as room_file:
                room_file.seek(0)
                json.dump(self.current_room, room_file, indent=4)
                room_file.close()
        except Exception, e:
            raise e

    def load_room(self, room_title):
        try:
            with open(self.temp_dir+room_title, 'r') as room_file:
                self.current_room = json.load(room_file, object_pairs_hook=OrderedDict)
                return True
        except Exception, e:
            return False

    def get_items(self):
        text = {"description":"Looking around you see "}
        if self.current_room['feature_searched'] == True:
            items = self.current_room['items_in_room']
            for item in items:
                text["description"] += "a " + item + ", "
            text["description"] = str(text["description"][:-2])
        else:
            text["description"] = "You don't notice anything you could pick up"
        return text

    def lookat(self, title):
        response = {
                    "description":None
                }
        if title in self.current_room['items_in_room']:
            if self.current_room['feature_searched'] == True:
                return str( item_ops().lookat(title))
        elif title in self.current_room['feature_1_aliases']:
            response["description"] = str( self.current_room['feature_1_description'])
        elif title in self.current_room['feature_2_aliases']:
            response["description"] = str( self.current_room['feature_2_description'])
        else:
            response["description"] = str( self.item_not_found + title)
        return response

    def use(self, title, action):
        response = {
                    "description" : None
                }
        if title in self.current_room['feature_1_aliases']:
            if action in self.current_room['feature_1_verbs']:
                response["description"] = str( self.current_room['feature_1_action_description'])
        elif title in self.current_room['feature_2_aliases']:
            if action in self.current_room['feature_2_verbs']:
                response["description"] = str( self.current_room['feature_2_action_description'])
        else:
            response["description"] = str( self.item_not_found + title)
        return response

class item_ops():
    def __init__(self):
        self.temp_dir = save_info().get_temp_save_dir_items()
        self.items = item_info().get_titles()
        self.item_not_found = "The cold must be making you delirious, you can't seem to find a " 

    def use(self, item_title, action):
        response = {
                    "description":None
                }
        if item_title in self.items:
            with open(self.temp_dir+item_title, 'r+') as item_file:
                item = json.load(item_file, object_pairs_hook=OrderedDict)
                if action in item['action_verbs']:
                    if item['activatable'] == True:
                        if item['active'] == True:
                            item['active'] = False
                            response["description"] = str( item['deactivate_description'])
                        else:
                            item['active'] = True
                            response["description"] = str( item['activate_description'])
                        item_file.close()
                        with open(self.temp_dir + item_title, 'w') as item_file:
                            json.dump(item, item_file, indent=4)
                    else:
                        response["description"] = str( item['activate_description'])
        else:
            response["description"] = str( self.item_not_found + item_title)
        return response

    def lookat(self, item_title):
        response = {
                    "description": None
                }
        if item_title in self.items:
            with open(self.temp_dir+item_title, 'r') as item_file:
                item = json.load(item_file, object_pairs_hook=OrderedDict)
                item_file.close()
                response["description"] = str( item['description'])
        else:
            response["description"] = str( self.item_not_found + item_title)
        return response

    def is_an_item(self, item_title):
        if item_title in self.items:
            return True
        else:
            return False

class game_ops():
    def __init__(self):
        self.room = room_ops()
        self.items = item_ops()

    def new_game(self):
        try:
            file_ops().new_game()
            self.room.load_room("Shore")
            return True
        except Exception, e:
            return False

    def load_game(self):
        try:
            return self.room.load_room("Game Trail")
        except Exception, e:
            return False

    def get_room_title(self):
        return self.room.get_room_title()

    def get_room_desc(self):
        if self.room.get_visited() == False:
            return self.room.get_room_long_desc()
        else:
            return self.room.get_room_short_desc()

    def look(self):
        return {"description":self.room.get_room_long_desc()}

    def check_move(self, title_or_compass, items_inventory):
        result = self.room.check_connections(title_or_compass, items_inventory)
        if result["move"] == True:
            self.room.store_room()
            self.room.load_room(result['title'])
        if result['description'] is None:
            result['description'] = str(self.get_room_desc())
        return result

    def get_room_items(self):
        return self.room.get_items()

    def use(self, title, action, in_inventory):
        if self.items.is_an_item(title) and in_inventory == True:
            return self.items.use(title, action)
        else:
            return self.room.use(title, action)

    def lookat(self, title, in_inventory):
        if self.items.is_an_item(title) and in_inventory == True:
            return self.items.lookat(title)
        else:
            #assume item or feature may be in room and check room items and features
            return self.room.lookat(title)
