import sys
sys.path.insert(0, "C:\\Users\\Alex\\Desktop\\capstone\\language_parser")
from file_handler.file_lib import game_ops
import language_parser.command_parser as parse
from game import *
def getPlayerName(p=Player):
    print ("Hello dreary traveler.  What is your name? ")
    choice= raw_input("-> ")
    p.name = choice
    print "goodluck ", choice, "\n"
    return p


def getInput(phrase):
    #EMILY PARSES PHRASE
    action = raw_input("What would you like to do?")
    noun = raw_input("To what object")
    return action, noun


def parseMoveString(tar, stemp):
    tar.lower()
    if tar.startswith("sh"):
        stemp = "shore"
    elif tar.startswith("cra"):
        stemp = "crash site"
    elif tar.startswith("gam" or "trai"):
        stemp = "game trail"
    elif tar.startswith("ca"):
        stemp = "cave"
    return stemp

def parseMoveRoom(tar, temp, g=Game):
    tar.lower()
    if tar.startswith("sh"):
        temp = g.shore
        g.cur_room = temp
    elif tar.startswith("cra"):
        temp = g.crash
        g.cur_room = temp
    elif tar.startswith("gam" or "trai"):
        temp = g.trai
        g.cur_room = temp
    elif tar.startswith("ca"):
        temp = g.cave
        g.cur_room = temp
    return temp

#TODO build a initilizaion function for testing purposes
#def testInit():
def print_help():
    print "TODO: Write this function"
    print "This is a stub function for displaying help to the user!"

def print_inventory():
    print "TODO: Write this function"
    print "This is a stub function for displaying the items in the user's inventory!"

def process_item_action(item, action):
    print "TODO: Write this function"
    print "This is a stub function for handling item_action commands!"
    print "Here's the item: " + item
    print "Here's the action: " + action

def process_action_only(action):
    print "TODO: Write this function"
    print "This is a stub function for handling action_only commands!"
    print "Here's the action: " + action
    if action == "help":
        print_help()
    elif action == "inventory":
        print_inventory()
    else:
        "The rest of this function still needs to be written..."

def process_room_action(room, action):
    print "TODO: Write this function"
    print "This is a stub function for handling room_action commands!"
    print "Here's the item: " + item
    print "Here's the action: " + action

def process_exit(direction, name):
    print "TODO: Write this function"
    print "This is a stub function for handling exit commands!"
    print "Here's the direction: " + direction
    print "Here's the exit name: " + name

def process_exit_only(name):
    print "TODO: Write this function"
    print "This is a stub function for handling exit only commands!"
    print "Here's the exit name: " + name

def process_item_only(name):
    print "TODO: Write this function"
    print "This is a stub function for handling item_only commands!"
    print "Here's the item name: " + name

def process_feature_action(feature, action):
    print "TODO: Write this function"
    print "This is a stub function for handling feature_action commands!"
    print "Here's the feature: " + feature
    print "Here's the action: " + action

def process_feature_only(feature):
    print "TODO: Write this function"
    print "This is a stub function for handling feature only commands!"
    print "Here's the feature: " + feature

def process_room_only(room):
    print "TODO: Write this function"
    print "This is a stub function for handling room only commands!"
    print "Here's the room: " + room

# HOW TO USE IN GAME ENGINE
test_user_command = "Eat the oar."
#test_user_command = "HELP!"
#test_user_command = "inventory"
#test_user_command = "eat frozen dead hare"
processed_user_command = parse.parse_command(test_user_command)
processed = processed_user_command["other"]["processed"]
if processed:
    output_type = processed_user_command["type"]
    if output_type == "item_action":
        item = processed_user_command["item"]["name"]
        action = processed_user_command["item"]["action"]
        process_item_action(item, action)
    elif output_type == "action_only":
        action = processed_user_command["general"]["action"]
        process_action_only(action)
    elif output_type == "room_action":
        room = processed_user_command["room"]["name"]
        action = processed_user_command["room"]["action"]
        process_room_action(room, action)
    elif output_type == "exit":
        exit_direction = processed_user_command["exit"]["direction"]
        exit_name = processed_user_command["exit"]["exit"]
        process_exit(exit_direction, exit_name)
    elif output_type == "exit_only":
        exit_name = processed_user_command["exit"]["exit"]
        process_exit_only(exit_name)
    elif output_type == "item_only":
        item_name = processed_user_command["item"]["name"]
        process_item_only(item_name)
    elif output_type == "feature_action":
        feature = processed_user_command["feature"]["name"]
        action = processed_user_command["feature"]["action"]
        process_feature_action(feature, action)
    elif output_type == "feature_only":
        feature = processed_user_command["feature"]["name"]
        process_feature_only(feature)
    elif output_type == "room_only":
        room = processed_user_command["room"]["name"]
        process_room_only(room)
    else:
        "Error command type not supported yet."
else:
    print "I'm sorry. I didn't understand that command. Please enter a different command."
