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
import json
import os

files_to_ignore = ["Rooms.md", "Items.md"]

def _list_keys(option):
    """
    This function will iterate through all the room or item template files
    located in the /data/rooms/ or /data/items/ and check that all the files 
    have the same structure.  It will report what rooms are different if any
    and then list all the keys in the room structure
    """
    if option == "rooms":
        src_dir = room_info().get_dir()
        print("Scanning room files")
    elif option == "items":
        src_dir = item_info().get_dir()
        print("Scanning item files")
    else:
        print("Invalid entry")
        exit()
    response = dict()

    for filename in os.listdir(src_dir):
        if filename not in files_to_ignore:
            with open(src_dir+filename, 'r') as open_file:
                try:
                    file_json = json.load(open_file, object_pairs_hook=OrderedDict)
                    if option == "rooms":
                        response.update({filename:_match_keys_room(file_json)})

                except Exception, e:
                    print("File: " + filename + " may have incorrect json structure and could not be loaded")
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
        for obj in file_json["connected_rooms"]:
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
        if key not in valid_keys:
            response.update({key:the_dict[key]})
    for key in valid_keys:
        if key not in the_dict:
            response.update({key:key})
    return response

def main():
    accepted_input = {
            "1":"rooms",
            "2":"items"
            }

    print(  "\nWhat would you like to do?\n"
            "1. Validate all keys in rooms\n"
            "2. Validate all keys in item\n"
            "9. Back\n")

    selection = raw_input(":")
    if selection in accepted_input:
        if selection == "1" or selection == "2":
            _list_keys(accepted_input[selection])
    elif selection == "9":
        return

    main()

if __name__ == "__main__":
    main()
