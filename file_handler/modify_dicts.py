"""
Filename - modify_dicts.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - This file intends to create a number of functions that 
will allow the user to do perform the following actions

List all the keys in a type of file: room, item
Add a key to a type of file: room, item
Delete a key to a type of file: room, item
Edit a key to a type of file: room, item
"""
from collections import OrderedDict
from name_lists import room_info
from name_lists import item_info
from name_lists import dict_keys
from name_lists import save_info
import file_handler.data_entry as mod_files
import file_handler.file_lib as files
import json
import os

FILES_TO_IGNORE = ["Rooms.md", "Items.md"]
OPTIONAL_KEYS = dict_keys().get_opt_keys()
ROOMS_DIR = room_info().get_dir()
TEMP_ROOMS_DIR = save_info().get_temp_save_dir_rooms()
ITEMS_DIR = item_info().get_dir()
ITEMS_TEMP_DIR = save_info().get_temp_save_dir_items()
ROOM_TITLES = room_info().get_titles()
ITEM_TITLES = item_info().get_titles()

def _list_keys(option):
    """
    This function will iterate through all the room or item template files
    located in the /data/rooms/ or /data/items/ and check that all the files 
    have the same structure.  It will report what rooms are different if any
    and then list all the keys in the room structure
    """
    if option == "rooms":
        src_dir = ROOMS_DIR
        print("Scanning room files")
    elif option == "temprooms":
        src_dir = TEMP_ROOMS_DIR 
        print "Scanning temp room files"
    elif option == "items":
        src_dir = ITEMS_DIR 
        print("Scanning item files")
    elif option == "tempitems":
        src_dir = ITEMS_TEMP_DIR
        print "Scanning temp item files"
    else:
        print("Invalid entry")
        exit()
    response = dict()

    for filename in os.listdir(src_dir):
        if filename not in FILES_TO_IGNORE and not filename.endswith("swp"):
            new_dir = os.path.join(src_dir, filename)
            with open(new_dir, 'r') as open_file:
                try:
                    file_json = json.load(open_file, object_pairs_hook=OrderedDict)
                    if option == "rooms" or option == "temprooms":
                        response.update({filename:_match_keys_room(file_json)})
                    elif option == "items" or option == "tempitems":
                        response.update({filename:_match_keys_items(file_json)})
                except Exception, e:
                    print("File: " + filename + " json could not be parsed")
                    print("Error: " + str(e) + "\n")
                open_file.close()

    _print_invalid(response)
    print("Done validating")

def _print_invalid(response):
    """
    prints out the warnings about keys that were found in files that
    should not exist
    """
    for title in response:
        if response[title]:
            print("In file: " + title.ljust(12) + " invalid or missing key/value pairs found: ")
            print(json.dumps(response[title], indent=4))

def _match_keys_items(file_json):
    """
    checks the passed in json object against the official structure expected of 
    and item
    """
    item_keys = dict_keys().get_item_keys()
    res = dict()

    result = _compare_dict(file_json, item_keys)
    res = _merge_two_dicts(res, result)
    result = _check_verbs(file_json)
    res = _merge_two_dicts(res, result)
    return res

def _check_verbs(file_json):
    """
    checks the verb structure
    """
    verbs = dict_keys().get_verbs()
    verb_keys = dict_keys().get_verb_keys()
    use_keys = dict_keys().get_additional_use_keys()
    response = dict()
    response = _compare_dict(file_json['verbs'], verbs)
    for verb in file_json["verbs"]:
        result = dict()
        if verb == "use":              
            result.update({verb:_compare_dict(file_json["verbs"][verb], use_keys+verb_keys)})
        else:
            result.update({verb:_compare_dict(file_json["verbs"][verb], verb_keys)})
        if result[verb]:
            response = _merge_two_dicts(response, result)
    return response

def _match_keys_room(file_json):
    """
    checks the passed in json object against the official structure expected and if it
    is different returns true if they keys match
    """
    room_keys = dict_keys().get_room_keys()
    response = dict()

    #check the top level of the room file
    result = _compare_dict(file_json, room_keys)
    response = _merge_two_dicts(response, result)
    #check the features structure
    result = _check_features("1", file_json)
    response = _merge_two_dicts(response, result)
    result = _check_features("2", file_json)
    response = _merge_two_dicts(response, result)
    result = _check_connected_rooms(file_json)
    response = _merge_two_dicts(response, result)

    return response

def _check_connected_rooms(file_json):
    """
    check that the structure connected_rooms has all the correct keys
    because the connected rooms are unstructured objects meaning without
    keys, then only collect the keys that are missing, but we'll need to 
    check manually which connected_room it came from
    """
    response = dict()
    keys = dict_keys().get_connected_room_keys()
    if "connected_rooms" in file_json:
        for room in file_json["connected_rooms"]:
            obj = file_json['connected_rooms'][room]
            result = dict()
            result = _compare_dict(obj, keys)
            if result:
                response.update(result)
    if response:
        response = {"connected_rooms":response}
    return response


def _check_features(value, file_json):
    """
    check that the keys in the features are correct
    and that all verbs that are part of those features are also correct
    """
    feature_keys = dict_keys().get_feature_keys()
    verbs = dict_keys().get_verbs()
    verb_keys = dict_keys().get_verb_keys()
    use_keys = dict_keys().get_additional_use_keys()

    response = dict()

    #if the feature e.g. 1 or 2 does not exist don't check the contents
    if value not in file_json["features"]:
        response.update({"features":{value:"missing object: " + value}})
    else:
        #first we'll check the contents of the feature
        result = dict()
        result.update({value:_compare_dict(file_json["features"][value], feature_keys)})
        if result[value]:
            response = _merge_two_dicts(response, result)
        #now we'll check that the feature has all the correct verbs
        result = dict()
        result.update({"feature " + value + " verbs":_compare_dict(file_json["features"][value]["verbs"], verbs)})
        if result["feature " + value + " verbs"]:
            response = _merge_two_dicts(response, result)
        #validate the structure of the verbs in the feature
        for verb in file_json["features"][value]["verbs"]:
            result = dict()
            if verb == "use":              
                result.update({"feature " + value + " " + verb:_compare_dict(file_json["features"][value]["verbs"][verb], use_keys+verb_keys)})
            else:
                result.update({"feature " + value + " " + verb:_compare_dict(file_json["features"][value]["verbs"][verb], verb_keys)})
            if result["feature " + value + " " + verb]:
                response = _merge_two_dicts(response, result)

    return response

def _merge_two_dicts(a, b):
    """
    Cite: https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
    """
    z = a.copy()
    z.update(b)
    return z

def _compare_dict(the_dict, valid_keys):
    """
    compares the dict to the valid keys to make sure they are correct
    """
    response = dict()

    for key in the_dict:
        if key not in valid_keys and key not in OPTIONAL_KEYS:
            response.update({key:the_dict[key]})
    for key in valid_keys:
        if key not in the_dict and key not in OPTIONAL_KEYS:
            response.update({key:key})
    return response


def _update_tree():
    """
    this function will allow the user to update the current structure of a room
    file.  Mainly designed to update the dict of dicts.  Used to refactor the
    current_rooms structure
    """

    while True:
        filename = raw_input("Enter template room or item to edit, q to quit: ")
        filename = str(filename)
        if filename in ROOM_TITLES:
            src_dir = ROOMS_DIR
        elif filename in ITEM_TITLES:
            src_dir = ITEMS_DIR
        if filename == "q":
            break
        if (filename not in FILES_TO_IGNORE and 
                filename in ROOM_TITLES or filename in ITEM_TITLES):
            new_dir = os.path.join(src_dir, filename)
            print new_dir
            with open(new_dir, 'r') as open_file:
                try:
                    obj = json.load(open_file, object_pairs_hook=OrderedDict)
                    open_file.close()
                except Exception, e:
                    print e
            source_order = files.get_order(obj)
            top_key = raw_input('Enter the dict key that you want to edit: ')
            new_key = raw_input('Enter the key whose value will be used as the objects key: ')
            if top_key in obj:
                old_dict = files.gather_dicts(obj, top_key)
                if old_dict is not None:
                    updates = {top_key:{}}
                    dict_sans_key = files.merge(updates, obj)
                    new_dict = files.add_key_before_dicts(old_dict, new_key, top_key)
                    updated_dict = files.merge(new_dict, dict_sans_key)
                    print json.dumps(updated_dict, indent=4)
                    ans = raw_input('Do you want to store this structure y/n: ')
                    if ans == 'y':
                        with open(new_dir, 'w') as open_file:
                            try:
                                json.dump(updated_dict, open_file, indent=4)
                                open_file.close()
                            except Exception, e:
                                print e
            else:
                print 'The top key is not in the structure'

def main(arg=None):
    """
    if an argument is not passed in prints a menu that the user may select from
    to perform the actions listed in the menu
    the argument is the option to perform in the menu
    """
    key_validation = {
            "1":"rooms",
            "2":"items",
            "3":"temprooms",
            "4":"tempitems"
            }
    data_entry = {
            "5":"rooms"
            }
    update_tree = {
            "6":"update"
            }

    print(  "\nWhat would you like to do?\n"
            "1. Validate all keys in template rooms\n"
            "2. Validate all keys in template items\n"
            "3. Validate all keys in temp rooms\n"
            "4. Validate all keys in temp items\n"
            "5. Add data into fields of templates\n"
            "6. Add a keyword in front of a dict structure\n"
            "q. Back\n")
    if arg == None:
        selection = raw_input(":")
    else:
        selection = str(arg)
    if selection in key_validation:
        _list_keys(key_validation[selection])
    elif selection in data_entry:
        mod_files.mod_rooms()
    elif selection in update_tree:
        _update_tree()
    elif selection == "q":
        return

    if arg == None:
        main()

if __name__ == "__main__":
    main()
