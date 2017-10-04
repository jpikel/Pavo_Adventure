"""
A program for testing methods in the command_parser module
"""

import language_parser.command_parser as parse

test_input = "This is A TEST string!!!!"

print "The test input is: " + test_input
print "The test output is: " + parse._preprocess(test_input)

test_input = "boar"

print "The test input is: " + test_input
parse._check_for_exact_match(test_input)

test_input = "paddle"
print "The test input is: " + test_input
print parse.parse_command(test_input)

test_input = "edge of lake"
print "The test input is: " + test_input
print parse.parse_command(test_input)