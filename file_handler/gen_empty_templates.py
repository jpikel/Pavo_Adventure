"""
Filename - 
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - 
"""

import os
import json
from collections import OrderedDict
from name_lists import room_info
from name_lists import item_info
from name_lists import verb_info

def create_room(room_name, index, connections):
    """
    Function - 
    Parameters - 
    Preconditions - 
    Postconditions - 
    Description - 
    """
    connection_titles = room_info().get_connection_list()
    room_template = OrderedDict()
    room_template.update({"id":index+1})
    room_template.update({"title":room_name})
    room_template.update({"visited":False})
    room_template.update({"long_description":"Long Description: " + room_name})
    room_template.update({"short_description":"Short Description: " + room_name})
    room_template.update({"feature_1_aliases":["feature_1_aliases"]})
    room_template.update({"feature_1_description":"Feature 1 description: " + room_name})
    room_template.update({"feature_1_verbs":["Feature 1 Verb: "+room_name]})
    room_template.update({"feature_1_action_description":"Feature 1 action description: " + room_name})
    room_template.update({"feature_1_item_required":"Item required feature 1: " + room_name})
    room_template.update({"feature_1_item_combine_description":"na" + room_name})
    room_template.update({"feature_1_attributes_affected":{"condition":5}})
    room_template.update({"feature_2_aliases":["feature 2 aliases: " + room_name]})
    room_template.update({"feature_2_description":"feature 2 description: " + room_name})
    room_template.update({"feature_2_verbs":["feature 2 verbs" + room_name]})
    room_template.update({"feature_2_action_description":"feature 2 action description: " + room_name})
    room_template.update({"feature_2_item_required":"feature 2 item required "+room_name})
    room_template.update({"feature_2_item_combine_description":"na"})
    room_template.update({"feature_1_attributes_affected":{"condition":5}})
    room_template.update({"connected_rooms":[{"id":0, 
                                             "title":connection_titles[room_name][0], 
                                             "aliases":[connection_titles[room_name][0]],
                                             "compass_direction":"",
                                             "item_required":False,
                                             "item_required_title":"",
                                             "pre_item_description":"",
                                             "accessible":True,
                                             "distance_from_room":1,
                                             }]})
    for x in range (1, connections):
        room_template["connected_rooms"].append({"id":0,                                              
                                              "title":connection_titles[room_name][x], 
                                             "aliases":[connection_titles[room_name][x]],
                                             "compass_direction":"",
                                            "item_required":False,
                                             "item_required_title":"",
                                             "pre_item_description":"",
                                             "accessible":True,
                                             "distance_from_room":1,
                                             })
    room_template.update({"items_in_room":[]})
    room_template.update({"feature_searched":False})
    room_template.update({"room_hazards":False})
    room_template.update({"room_hazard_description":""})
    room_template.update({"room_hazard_item":""})
    room_template.update({"room_hazard_occurs_description":""})
    room_template.update({"room_hazard_attributes_affected":""})
    room_template.update({"room_hazard_safe_description":""})

    return room_template

def create_item(item_name, index):
    """
    Function - 
    Parameters - 
    Preconditions - 
    Postconditions - 
    Description - 
    """
    item = OrderedDict()
    item.update({"id":index+1})
    item.update({"title":item_name})
    item.update({"aliases":[item_name]})
    item.update({"description":"description for " + item_name})
    item.update({"item_combination":"other item combination for " + item_name})
    item.update({"room_combination":item_name+" can be used in room"})
    item.update({"feature_combination":item_name+" can be used with feature"})
    item.update({"action_verbs":["use"]})
    item.update({"activate_description":"action description " + item_name})
    item.update({"deactivate_description":"de-action description " + item_name})
    item.update({"active":False})
    item.update({"activatable":False})
    item.update({"attributes_affected_requirement_met":[{}]})
    item.update({"attributes_affected_requirement_not_met":[{}]})
    item.update({"requirement_met":True})
    item.update({"requirement_met_description":"req met " + item_name})
    item.update({"requirement_not_met_description":"req not met "+ item_name})
    return item

def create_verbs():
    verbs = verb_info().get_verbs()
    verb_dict = OrderedDict()
    for verb in verbs:
        verb_dict.update({verb:verb})

    verb_dict = OrderedDict(sorted(verb_dict.items()))
    with open("../data/verbs_dict", 'w') as outfile:
        json.dump(verb_dict, outfile, indent=4)
        outfile.close()


def main():
    """
    Function - 
    Parameters - 
    Preconditions - 
    Postconditions - 
    Description - 
    """
#    rooms = room_info()
#    room_titles = rooms.get_titles()
#    room_connections = rooms.get_connection_amount()
#    room_dir = rooms.get_dir()
#    for room in room_titles:        
#        room_template = create_room(room, room_titles.index(room), room_connections[room_titles.index(room)])
#        with open(room_dir + room, 'w') as outfile:
#            json.dump(room_template, outfile, indent=4)
#            outfile.close()
#

#    items = item_info()
#    item_titles = items.get_titles()
#    item_dir = items.get_dir()
#    for item in item_titles:
#        item_template = create_item(item, item_titles.index(item))
#        with open(item_dir + item, 'w') as outfile:
#            json.dump(item_template, outfile, indent=4)
#            outfile.close()

#    create_verbs()
main()
