"""
A program for testing methods in the command_parser module
"""

import language_parser.command_parser as parse

test_input = "This is A TEST string!!!!"
print "The test input is: " + test_input
print "The test output after calling _preprocess is: " + parse._preprocess(test_input)

test_input = "paddle"
print "The test input is: " + test_input
print "The parsed command output is:"
print parse.parse_command(test_input)

test_input = "edge of lake"
print "The test input is: " + test_input
print "The parsed command output is:"
print parse.parse_command(test_input)

test_input = "the paddle a dog these geese thesis statement these"
print "The test input is: " + test_input
print "The output without noise words is: " + parse._remove_noise(test_input)