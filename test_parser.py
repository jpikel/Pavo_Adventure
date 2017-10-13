"""
A program for testing methods in the command_parser module
"""

import json

import language_parser.command_parser as parse

# # test_input = "This is A TEST string!!!!"
# # print "The test input is: " + test_input
# # print "The test output after calling _preprocess is: " + parse._preprocess(test_input)

# test_input = "paddle"
# print "The test input is: " + test_input
# print "The parsed command output is:"
# print parse.parse_command(test_input)
# print ""

# test_input = "edge of lake"
# print "The test input is: " + test_input
# print "The parsed command output is:"
# print parse.parse_command(test_input)
# print ""

# # test_input = "the paddle a dog these geese thesis statement these"
# # print "The test input is: " + test_input
# # print "The output without noise words is: " + parse._remove_noise(test_input)

# test_input = "eat oar"
# print "The test input is: " + test_input
# print "Calling parse command on it..."
# print parse.parse_command(test_input)
# print ""

# test_input = "eat the oar"
# print "The test input is: " + test_input
# print "Calling parse command on it..."
# print parse.parse_command(test_input)
# print ""

# test_input = "Eat the oar."
# print "The test input is: " + test_input
# print "Calling parse command on it..."
# print parse.parse_command(test_input)
# print ""

# test_input = "eat board"
# print "The test input is: " + test_input
# print "Calling parse command on it..."
# print parse.parse_command(test_input)
# print ""

# test_input = "sniff oar"
# print "The test input is: " + test_input
# print "Calling parse command on it..."
# print parse.parse_command(test_input)
# print ""

# test_input = "bligh blah"
# print "The test input is: " + test_input
# print "Calling parse command on it..."
# print parse.parse_command(test_input)
# print ""

# test_input = "inventory"
# print "The test input is: " + test_input
# print "Calling parse command on it..."
# print parse.parse_command(test_input)
# print ""

# test_input = "help"
# print "The test input is: " + test_input
# print "Calling parse command on it..."
# print parse.parse_command(test_input)
# print ""



# HOW TO USE IN GAME ENGINE

def process_item_action(item, action):
    print "This is a stub function for handling item_action commands!"
    print "Here's the item: " + item
    print "Here's the action: " + action

def process_action_only(action):
    print "This is a stub function for handling action_only commands!"
    print "Here's the action: " + action

def process_room_action(room, action):
    print "This is a stub function for handling room_action commands!"
    print "Here's the item: " + item
    print "Here's the action: " + action


test_user_command_1 = "Eat the oar."
processed_user_command = parse.parse_command(test_user_command_1)
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
    else:
        "Error command type not supported yet."
else:
    print "I'm sorry. I didn't understand that command. Please enter a different command."