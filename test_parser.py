"""
A program for testing methods in the command_parser module
"""

import language_parser.command_parser as parse

test_input = "This is A TEST string!!!!"

print "The test input is: " + test_input
print "The test output is: " + parse._preprocess(test_input)

