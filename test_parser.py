"""
A program for testing methods in the command_parser module
"""

import json

import language_parser.command_parser as parse

# # test_input = "This is A TEST string!!!!"
# # print "The test input is: " + test_input
# # print "The test output after calling _preprocess is: " + parse._preprocess(test_input)

test_input = "paddle"
print "The test input is: " + test_input
print "The parsed command output is:"
print parse.parse_command(test_input)
print ""

test_input = "edge of lake"
print "The test input is: " + test_input
print "The parsed command output is:"
print parse.parse_command(test_input)
print ""

# test_input = "the paddle a dog these geese thesis statement these"
# print "The test input is: " + test_input
# print "The output without noise words is: " + parse._remove_noise(test_input)

test_input = "eat oar"
print "The test input is: " + test_input
print "Calling parse command on it..."
print parse.parse_command(test_input)
print ""

test_input = "eat the oar"
print "The test input is: " + test_input
print "Calling parse command on it..."
print parse.parse_command(test_input)
print ""

test_input = "Eat the oar."
print "The test input is: " + test_input
print "Calling parse command on it..."
print parse.parse_command(test_input)
print ""

test_input = "eat board"
print "The test input is: " + test_input
print "Calling parse command on it..."
print parse.parse_command(test_input)
print ""

test_input = "sniff oar"
print "The test input is: " + test_input
print "Calling parse command on it..."
print parse.parse_command(test_input)
print ""

test_input = "bligh blah"
print "The test input is: " + test_input
print "Calling parse command on it..."
print parse.parse_command(test_input)
print ""

test_input = "inventory"
print "The test input is: " + test_input
print "Calling parse command on it..."
print parse.parse_command(test_input)
print ""

test_input = "help"
print "The test input is: " + test_input
print "Calling parse command on it..."
print parse.parse_command(test_input)
print ""

test_input = "search wood pole"
print "The test input is: " + test_input
print "Calling parse command on it..."
print parse.parse_command(test_input)
print ""

test_input = "search campfire"
print "The test input is: " + test_input
print "Calling parse command on it..."
print parse.parse_command(test_input)
print ""