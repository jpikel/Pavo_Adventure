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
        returns OrderedDict that is the room structure in json
    """
    connection_titles = room_info().get_connection_list()
    room_template = OrderedDict()
    room_template.update({"id":index+1})
    room_template.update({"title":room_name})
    room_template.update({"visited":False})
    room_template.update({"long_description":"Long Description: " + room_name})
    room_template.update({"short_description":"Short Description: " + room_name})
    room_template.update({"features":{
                                        "1":{
                                            "title":"feature_1_title",
                                            "aliases":["feature_1_aliases"],
                                            "verbs":{
                                                    "look at":{
                                                        "description":"look at description for feature 1 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "use":{
                                                        "description":"use description for feature 1 " + room_name,
                                                        "deactivate_description":"use deactivate for feature 1 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "eat":{
                                                        "description":"eat description for feature 1 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "pull":{
                                                        "description":"pull description for feature 1 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "read":{
                                                        "description":"read for feature 1 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "search":{
                                                        "description":"read for feature 1 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "take":{
                                                        "description":"take for feature 1 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "drop":{
                                                        "description":"drop for feature 1" + room_name,
                                                        "modifiers":{}
                                                        }
                                                    }
                                             },
                                        "2":{
                                            "title":"feature_2_title",
                                            "aliases":["feature_2_aliases"],
                                            "verbs":{
                                                    "look at":{
                                                        "description":"look at description for feature 2 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "use":{
                                                        "description":"use description for feature 2 " + room_name,
                                                        "deactivate_description":"use deactivate for feature 2 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "eat":{
                                                        "description":"eat description for feature 2 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "pull":{
                                                        "description":"pull description for feature 2 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "read":{
                                                        "description":"read for feature 2 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "search":{
                                                        "description":"read for feature 2 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "take":{
                                                        "description":"take for feature 2 " + room_name,
                                                        "modifiers":{}
                                                        },
                                                    "drop":{
                                                        "description":"drop for feature 2" + room_name,
                                                        "modifiers":{}
                                                        }
                                                    }
                                             }
                                        }
                                    })
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
    for x in range (0, connections):
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
        returns an OrderedDict that is the structure of an item file in json
    """
    item = OrderedDict()
    item.update({"id":index+1})
    item.update({"title":item_name})
    item.update({"aliases":[item_name]})
    item.update({"verbs":{
                                "look at":{
                                    "description":"look at description for " + item_name,
                                    "modifiers":{}
                                    },
                                "use":{
                                    "description":"use description for " + item_name,
                                    "deactivate_description":"use deactivate for " + item_name,
                                    "modifiers":{}
                                    },
                                "eat":{
                                    "description":"eat description for " + item_name,
                                    "modifiers":{}
                                    },
                                "pull":{
                                    "description":"pull description for " + item_name,
                                    "modifiers":{}
                                    },
                                "read":{
                                    "description":"read for " + item_name,
                                    "modifiers":{}
                                    },
                                "take":{
                                    "description":"take for " + item_name,
                                    "modifiers":{
                                        "player":{
                                            "inventory":"add"
                                            },
                                        "room":{
                                            "title":"any",
                                            "items_in_room":"add"
                                            }
                                        }
                                    },
                                "search":{
                                    "description":"search for " + item_name,
                                    "modifiers":{}
                                    },
                                "drop":{
                                    "description":"drop for " + item_name,
                                    "modifiers":{
                                        "player":{
                                            "inventory":"drop"
                                            },
                                        "room":{
                                            "title":"any",
                                            "items_in_room":"drop"
                                            }
                                        }
                                    }
                                }})
    item.update({"active":False})
    item.update({"activatable":False})
    item.update({"attributes_affected_requirement_met":[{}]})
    item.update({"attributes_affected_requirement_not_met":[{}]})
    item.update({"requirement_met":True})
    item.update({"requirement_met_description":"req met " + item_name})
    item.update({"requirement_not_met_description":"req not met "+ item_name})
    item.update({"item_combination":"other item combination for " + item_name})
    item.update({"room_combination":item_name+" can be used in room"})
    item.update({"feature_combination":item_name+" can be used with feature"})
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


def make_rooms():
    rooms = room_info()
    room_titles = rooms.get_titles()
    room_titles = ["cave"]
    room_connections = rooms.get_connection_amount()
    for room in room_titles:        
        room_dir = "../data/rooms"
        room_template = create_room(room, room_titles.index(room), room_connections[room_titles.index(room)])
        room_dir = os.path.join(room_dir, room)
        with open(room_dir, 'w') as outfile:
            json.dump(room_template, outfile, indent=4)
            outfile.close()

def make_items():
    items = item_info()
    item_titles = items.get_titles()
    for item in item_titles:
        item_dir = "../data/items"
        item_template = create_item(item, item_titles.index(item))
        item_dir = os.path.join(item_dir, item)
        with open(item_dir, 'w') as outfile:
            json.dump(item_template, outfile, indent=4)
            outfile.close()

def main():
    """
        recreates all the room template files as blanks
        reacreates all the item template files as blanks
        make sure you really want to do this.  Will overwrite all the previous
        information!
        also creates a base template file for all the verbs if uncommented
    """
#    make_rooms()
#    make_items()
#    create_verbs()
main()

print("Nothing happened this file will wipe out all the template files at present")
print("Only run if you really mean too.  Requires uncommenting the function in this script")
