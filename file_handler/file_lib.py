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

    def get_response_struct(self):
        return self.response

class save_ops():
    def new_game(self):
        #Reference - https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
        print("Preparing to make new game")
        src_dir = room_info().get_dir()
        dst_dir = save_info().get_temp_save_dir_rooms()
        self.copy_files(src_dir, dst_dir)
        src_dir = item_info().get_dir()
        dst_dir = save_info().get_temp_save_dir_items()
        self.copy_files(src_dir, dst_dir)


    def copy_files(self, src_dir, dst_dir):
        try:
            print("Cleaning" + dst_dir)
            self.clean_dir(dst_dir)
            print("Copying from " +src_dir+ " to temp " + dst_dir)
            for item in os.listdir(src_dir):
                if item not in ignore:
                    src = os.path.join(src_dir, item)
                    dst = os.path.join(dst_dir, item)
                    shutil.copy2(src,dst)
        except Exception, e:
            print("Something went horribly wrong creating the temp save file")
            print(e)

    def clean_dir(self, dst_dir):
        try:
            for item in os.listdir(dst_dir):
                if item not in ignore:
                    to_del = os.path.join(dst_dir, item)
                    os.remove(to_del)
        except Exception, e:
            print("Something went wrong cleaning the directory")
            print(e)


class file_operations():
    def __init__(self):
        self.current_room = OrderedDict()
        self.temp_dir_rooms = save_info().get_temp_save_dir_rooms()
        self.temp_dir_items = save_info().get_temp_save_dir_items()
        self.items = item_info().get_titles()
        self.item_not_found = "The cold must be making you delirious, you can't seem to find a " 
        self.verb_not_found = "At this very moment you really are not sure how to " 

    def get_room_title(self):
        return str(self.current_room['title'])

    def get_room_long_desc(self):
        return str(self.current_room['long_description'])

    def get_room_short_desc(self):
        return str(self.current_room['short_description'])

    def get_visited(self):
        return self.current_room['visited']

    def get_room_item_list(self):
        return self.current_room['items_in_room']

    def store_room(self):
        try:
            room_title = self.current_room['title']
            self.current_room['visited'] = True
            with open(self.temp_dir_rooms+room_title, 'w') as room_file:
                room_file.seek(0)
                json.dump(self.current_room, room_file, indent=4)
                room_file.close()
        except Exception, e:
            raise e

    def load_room(self, room_title):
        try:
            with open(self.temp_dir_rooms+room_title, 'r') as room_file:
                self.current_room = json.load(room_file, object_pairs_hook=OrderedDict)
                return True
        except Exception, e:
            return False

    def check_connections(self, title_or_direction, items):
        response = response_struct().get_response_struct()
        for room in self.current_room['connected_rooms']:
            if (title_or_direction == str(room['title']) 
                or title_or_direction == room['compass_direction']
                or title_or_direction in room['aliases']):
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
                            else:
                                response['description'] = str(room['pre_item_description'])
                    else:
                        response['description'] = str(room['pre_item_description'])
                else:
                    response['move'] = True
                    response['distance_from_room'] = room['distance_from_room']
                    response['title'] = str(room['title'])
                break
        return response

    def get_items(self):
        text = "Looking around you see "
        if self.current_room['feature_searched'] == True:
            items = self.current_room['items_in_room']
            for item in items:
                text += "a " + item + ", "
            text = text[:-2]
        else:
            text = "You don't notice anything you could pick up"
        return text

    def is_an_item(self, item_title):
        if item_title in self.items:
            return True
        else:
            return False

    def item_in_inventory(self, item_title, action):
        response = response_struct().get_response_struct()
        if item_title in self.items:
            with open(self.temp_dir_items+item_title, 'r+') as item_file:
                item = json.load(item_file, object_pairs_hook=OrderedDict)
                if action in item['verbs']:
                    if action == "use" and item['activatable'] == True:
                        if item['active'] == True:
                            item['active'] = False
                            response["description"] = str(item['verbs']['use']['deactivate_description'])
                        else:
                            item['active'] = True
                            response["description"] = str(item['verbs']['use']['description'])

                        item_file.close()
                        with open(self.temp_dir_items + item_title, 'w') as item_file:
                            json.dump(item, item_file, indent=4)
                            item_file.close()
                    else:
                        response['description'] = str(item['verbs'][action]['description'])
                else:
                    response['description'] = str(self.verb_not_found + " the " + item_title)
        else:
            response["description"] = str( self.item_not_found + item_title)
        return response

    def feature_in_room(self, title, action):
        response = response_struct().get_response_struct()
        if (title == self.current_room['feature_1_title'] or
                title in self.current_room['feature_1_aliases'] and
                action in self.current_room['feature_1_verbs']):
            response['description'] = str(self.current_room['feature_1_verbs'][action]['description'])
        elif (title == self.current_room['feature_2_title'] or
                title in self.current_room['feature_2_aliases'] and
                action in self.current_room['feature_2_verbs']):
            response['description'] = str(self.current_room['feature_2_verbs'][action]['description'])
        else:
            response['description'] = self.verb_not_found + " " + action + " the " + title
        return response

    def verb_handler(self, title, action, in_inventory):
        if in_inventory == True:
            return self.item_in_inventory(title, action)
        elif title in self.current_room['items_in_room'] and self.current_room['feature_searched'] == True:
            return self.lookat_item_in_room(title)
        elif (title in self.current_room['feature_1_aliases'] 
            or title in self.current_room['feature_2_aliases']
            or title == self.current_room['feature_1_title']
            or title == self.current_room['feature_2_title']):
            return self.feature_in_room(title, action)
        elif title not in self.items:
            response = response_struct().get_response_struct()
            response['description'] = self.item_not_found + title + " to " + action
            return response
        else:
            response = response_struct().get_response_struct()
            response['description'] = self.verb_not_found + " " + action + " the " + title
            return response


class game_ops():
    def __init__(self):
        self.operations = file_operations()

    def new_game(self):
        try:
            save_ops().new_game()
            self.operations.load_room("Shore")
            return True
        except Exception, e:
            return False

    def load_game(self):
        try:
            return self.operations.load_room("Game Trail")
        except Exception, e:
            return False

    def get_room_title(self):
        return self.operations.get_room_title()

    def get_room_desc(self):
        if self.operations.get_visited() == False:
            return self.operations.get_room_long_desc() + self.operations.get_items()
        else:
            return self.operations.get_room_short_desc() + self.operations.get_items()

    def look(self):
        return {"description":self.operations.get_room_long_desc()}

    def attempt_move(self, title_or_compass, items_inventory):
        result = self.operations.check_connections(title_or_compass, items_inventory)
        if result["move"] == True:
            self.operations.store_room()
            self.operations.load_room(result['title'])
        if result['description'] is None:
            result['description'] = str(self.get_room_desc()) 
        return result

    def verb(self, title, verb, in_inventory=False):
            return self.operations.verb_handler(title, verb, in_inventory)
