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
    """
    This structure is used for most all the responses sent back to the 
    calling function from inside file_ops class
        structure is
        "title":string
        "description": string
        "move": boolean, whether the move occured
        "distance_from_room": distance travel
    """
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
    """
    This class handles the starting of a new game and saving the current 
    game out to file
    """
    def new_game(self):
        """
        First cleans both the rooms and items folders in the temporary save
        directory.  Then copies the original template files from
        the data folder to the temp save folder for rooms and items
        """
        #Reference - https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
        print("Preparing to make new game")
        src_dir = room_info().get_dir()
        dst_dir = save_info().get_temp_save_dir_rooms()
        self.copy_files(src_dir, dst_dir)
        src_dir = item_info().get_dir()
        dst_dir = save_info().get_temp_save_dir_items()
        self.copy_files(src_dir, dst_dir)


    def copy_files(self, src_dir, dst_dir):
        """
        attemps to copy all the files from the source to the destination
        except those in the ignore list
        """
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
        """
        removes all the files in the directory passed in except those in the
        ignore list
        """
        try:
            for item in os.listdir(dst_dir):
                if item not in ignore:
                    to_del = os.path.join(dst_dir, item)
                    os.remove(to_del)
        except Exception, e:
            print("Something went wrong cleaning the directory")
            print(e)


class file_operations():
    """
    this class interacts with the files, such as room files and item files
    stores the current room as an OrderedDict
    """
    def __init__(self):
        self.current_room = OrderedDict()
        self.temp_dir_rooms = save_info().get_temp_save_dir_rooms()
        self.temp_dir_items = save_info().get_temp_save_dir_items()
        self.items = item_info().get_titles()
        self.item_not_found = "The cold must be making you delirious, you can't seem to find a " 
        self.verb_not_found = "At this very moment you really are not sure how to " 

    def get_room_title(self):
        """
        returns the current room's title
        """
        return str(self.current_room['title'])

    def get_room_long_desc(self):
        """
        returns a string of the long description
        """
        return str(self.current_room['long_description'])

    def get_room_short_desc(self):
        """
        returns a string of the short description
        """
        return str(self.current_room['short_description'])

    def get_visited(self):
        """
        returns the boolean in visited
        """
        return self.current_room['visited']

    def get_room_item_list(self):
        """
        returns a list that are the items in the room
        """
        return self.current_room['items_in_room']

    def store_room(self):
        """
        writes out the current room to its file as a string in the form as json
        to the appropriate room file in the temp save folder
        overwrites the file

        """
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
        """
        opens the room passed in from the temporary save folder.
        reads in the contents into the current_room object part of this class
        """
        try:
            with open(self.temp_dir_rooms+room_title, 'r') as room_file:
                self.current_room = json.load(room_file, object_pairs_hook=OrderedDict)
                print(self.current_room)
                return True
        except Exception, e:
            return False

    def check_connections(self, title_or_direction, items):
        """
        when given an official room title or compass direction, iterates
        through the current room's connected_rooms object to see if the compass
        or room title exist
        checks if an item is required to pass into this room
            if an item is required checks to see if that item is active as in worn or on
        writes the appropriate response into
            description
            move = boolean whether or not the move was successful
            title = the new room's title
            distance_from_room = distance traveled to the new room

        FUTURE implementation: check if the room is accessible or blocked
        """
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
                                break
                            else:
                                response['description'] = str(room['pre_item_description'])
                                break
                    else:
                        response['description'] = str(room['pre_item_description'])
                        break
                else:
                    response['move'] = True
                    response['distance_from_room'] = room['distance_from_room']
                    response['title'] = str(room['title'])
                    break
        return response

    def get_items(self):
        """
        if the room has been searched appropriately and there are items in the room
        then returns the items in the room as a string for descriptive purposes
        """
        text = "Looking around you see "
        if (self.current_room['feature_searched'] == True and 
                self.current_room['items_in_room'].length > 0):
            items = self.current_room['items_in_room']
            for item in items:
                text += "a " + item + ", "
            text = text[:-2]
        else:
            text = "You don't notice anything you could pick up"
        return text

    def is_an_item(self, item_title):
        """
        for the given title passed in returns a bool if the item exists in the list
        of possible items in the game
        """
        if item_title in self.items:
            return True
        else:
            return False

    def item_in_inventory(self, item_title, action):
        """
        called by the verb handler.  Looks up the item file and opens it
        returns the description listed for the particular verb at this moment.
        FUTURE: include additional parts of the structure to return to the game engine

            {
            "description": string
            }
        """
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
        """
            helper called from verb_handler()
            looks up to see if the title passed in is a feature in the current room
            if so and the verb is in the list of possible verbs for that feature then
            returns the description listed in that feature

            returns 
                {
                "description": string
                }
        """
        response = response_struct().get_response_struct()
        for element in self.current_room['features']:
            if title == self.current_room['features'][element]['title']:
                feature = element
        if action in self.current_room['features'][feature]['verbs']:
            response['description'] = str(self.current_room['features'][feature]['verbs'][action]['description'])
        else:
            response['description'] = self.verb_not_found + " " + action + " the " + title
        return response

    def verb_handler(self, title, action, in_inventory):
        """
            if the title has been checked against inventory of player it must be an item
            so return that item description
            otherwise it may be an item sitting in the room.  In that case only allow
            lookat that item
            otherwise the title may be a feature, return that features description
            otherwise see if it is an item and it does not exist in room or inventory
            return a wity response
            else return another witty response
        """
        if in_inventory == True:
            return self.item_in_inventory(title, action)
        elif (title in self.current_room['items_in_room'] and 
                self.current_room['feature_searched'] == True and
                action == "lookat"):
            return self.lookat_item_in_room(title)
        elif (title == self.current_room['features']['1']['title'] 
            or title == self.current_room['features']['2']['title']
            or title in self.current_room['features']['1']['aliases']
            or title in self.current_room['features']['1']['aliases']):
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
        """
            deletes the old temp save folder and creates a new one
            loads the Shore into the current_room
        """
        try:
            save_ops().new_game()
            self.operations.load_room("shore")
            return True
        except Exception, e:
            return False

    def load_game(self):
        """
            Future implementation currently just loads the game trail into the
            current room.  Will need to load the character state to the game engine
            as well
        """
        try:
            return self.operations.load_room("game trail")
        except Exception, e:
            return False

    def get_room_title(self):
        """
            returns the current_room's title
        """
        return self.operations.get_room_title()

    def get_room_desc(self):
        """
            returns either the long or short description 
            if the room has been previously visited
        """
        if self.operations.get_visited() == False:
            return self.operations.get_room_long_desc() + self.operations.get_items()
        else:
            return self.operations.get_room_short_desc() + self.operations.get_items()

    def look(self):
        """
            returns the long description, to be used with the verb look
        """
        return {"description":self.operations.get_room_long_desc()}

    def attempt_move(self, title_or_compass, items_inventory=None):
        """
            tries to move to the passed in room title or compass direction
            also expects a list of items currently held in the inventory
            defaults to None
        """
        result = self.operations.check_connections(title_or_compass, items_inventory)
        if result["move"] == True:
            self.operations.store_room()
            self.operations.load_room(result['title'])
        if result['move'] == False and result['description'] is None:
            result['description'] = "You were not able to move in that direction.  "
            result['description'] += str(self.get_room_desc()) 
        else:
            result['description'] = str(self.get_room_desc())
        return result

    def verb(self, title, verb, in_inventory=False):
        """
            verb handler, given a title of an item or feature, a verb
            and a bool for wether it is in the character's inventory
            returns a json object currently with only a description field
            {
                "decsription":string
            }

        """
        return self.operations.verb_handler(title, verb, in_inventory)
