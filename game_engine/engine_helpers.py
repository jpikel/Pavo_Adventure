"""
Filename - engine_helpers.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description -
"""
import textwrap
import string

#experiment text wrapping
CHARS_PER_LINE = 80

SPLASH_MESSAGE = [
"****************************************************************************",
"",
" ########  ########  ######   #######  ##          ###    ######## ######## ",
" ##     ## ##       ##    ## ##     ## ##         ## ##      ##    ##       ",
" ##     ## ##       ##       ##     ## ##        ##   ##     ##    ##       ",
" ##     ## ######    ######  ##     ## ##       ##     ##    ##    ######   ",
" ##     ## ##             ## ##     ## ##       #########    ##    ##       ",
" ##     ## ##       ##    ## ##     ## ##       ##     ##    ##    ##       ",
" ########  ########  ######   #######  ######## ##     ##    ##    ######## ",
 "",
 "",
"          ##  #######  ##     ## ########  ##    ## ######## ##    ## ",
"          ## ##     ## ##     ## ##     ## ###   ## ##        ##  ##  ",
"          ## ##     ## ##     ## ##     ## ####  ## ##         ####   ",
"          ## ##     ## ##     ## ########  ## ## ## ######      ##    ",
"    ##    ## ##     ## ##     ## ##   ##   ##  #### ##          ##    ",
"    ##    ## ##     ## ##     ## ##    ##  ##   ### ##          ##    ",
"     ######   #######   #######  ##     ## ##    ## ########    ##    ",
"",
"*****************************************************************************",
"Welcome To Desolate Journey",
"What would you like to do?",
"->  New Game",
"->  Load Game",
"->  Quit"]


class response_struct():
    """
    This structure is used for most all the responses sent back to the
        structure is
        "title":string the title being used
        "action": string the action being used
        "artifact": if the verb has an artifact usualy with read put it here
        "description": string the description of the the thing
        "success": boolean, whether the move occured or action occurred
        "distance_from_room": distance travel
    """
    def __init__(self):
        self.response = {
                    "title":None,
                    "action":None,
                    "artifact": [],
                    "description":None,
                    "success":False,
                    "distance_from_room":0
                }

    def get_response_struct(self):
        return self.response


def get_input(comment=''):
    """
    gets some input and returns it to the user
    """
    comment += '\n->'
    return str.lower(raw_input(comment))

def multi_printer(text, player_name=None):
    """
    a generic printer that can handle a list of text and print that to screen
    or a single string
    """
    if isinstance(text, list):
        for line in text:
            if player_name is not None: line = replace_player_name(line, player_name)
            lines = textwrap.wrap(line, CHARS_PER_LINE)
            for wrapped_line in lines: print wrapped_line
    elif isinstance(text, basestring):
        if player_name is not None: text = replace_player_name(text, player_name)
        lines = textwrap.fill(text, CHARS_PER_LINE)
        print lines
    else:
        print 'Error: did not receive list of strings or string'


def replace_player_name(text, player_name):
    """
    searchs the string for <playername> and inserts the player_name passed in
    returns the string
    """
    sub_string = "<playername>"
    return string.replace(text, sub_string, player_name)
