"""
Filename - engine_helpers.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description -
"""
#REFERENCES:
#https://stackoverflow.com/questions/4197805/python-for-loop-look-ahead
#https://docs.python.org/2/howto/curses.html

import textwrap
import string
import curses
import sys
import os
import subprocess
import time
import random
import file_handler.name_lists as info
USE_CURSES = False
if sys.platform == 'linux' or sys.platform == 'linux2':
    import curses
    USE_CURSES = True

MIN_COLS = 121
MIN_ROWS = 50
VERB_DICT = info.verb_info().get_verb_definitions()
ROOM_SINGLES = info.room_info().get_singles()
ROOM_TITLES = info.room_info().get_titles()
ITEM_SINGLES = info.item_info().get_singles()
ITEM_TITLES = info.item_info().get_titles()

#experiment text wrapping
CHARS_PER_LINE = 80

SPLASH_MESSAGE = [ 
"****************************************************************************",
" ",
" ########  ########  ######   #######  ##          ###    ######## ######## ",
" ##     ## ##       ##    ## ##     ## ##         ## ##      ##    ##       ",
" ##     ## ##       ##       ##     ## ##        ##   ##     ##    ##       ",
" ##     ## ######    ######  ##     ## ##       ##     ##    ##    ######   ",
" ##     ## ##             ## ##     ## ##       #########    ##    ##       ",
" ##     ## ##       ##    ## ##     ## ##       ##     ##    ##    ##       ",
" ########  ########  ######   #######  ######## ##     ##    ##    ######## ",
 " ",
 " ",
"          ##  #######  ##     ## ########  ##    ## ######## ##    ## ",
"          ## ##     ## ##     ## ##     ## ###   ## ##        ##  ##  ",
"          ## ##     ## ##     ## ##     ## ####  ## ##         ####   ",
"          ## ##     ## ##     ## ########  ## ## ## ######      ##    ",
"    ##    ## ##     ## ##     ## ##   ##   ##  #### ##          ##    ",
"    ##    ## ##     ## ##     ## ##    ##  ##   ### ##          ##    ",
"     ######   #######   #######  ##     ## ##    ## ########    ##    ",
" ",
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
            if line == ' ': print ''
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

def print_basic():
    text = []
    text.append('*'*20 + 'Help' + '*'*20)
    text.append('Verb'.ljust(12) + '  :: ' + ' verb definition')
    for key in VERB_DICT:
        text.append(key.ljust(12) + ' ::  ' + VERB_DICT[key])
    multi_printer(text)

def remove_punc(word):
    if isinstance(word, str):
        return word.translate(None, string.punctuation)
    else:
        return word.encode('utf-8').translate(None, string.punctuation)


    #------------------------------------------------------
    #This starts the UI curses section
    #------------------------------------------------------
class ui():
    """
    the UI class holds all the functions to write to the various curses
    windows. Initializes the curses main window and handles errors.
    """
    ROW = 0
    COL = 1
    def __init__(self):
        self.back_win = None
        self.main_win = None
        self.input_win = None
        self.stat_win = None
        self.time_win = None
        self.main_row = 0


    def init_windows(self, stdscr):
        if USE_CURSES and self.terminal_size():
            self.back_win = stdscr
            self.fill_back()
            self.input_win = curses.newwin(3, 117, 33, 2)
            self.stat_win = curses.newwin(9, 30, 23, 89)
            self.time_win = curses.newwin(20, 30, 2, 89)
            self.main_win = curses.newwin(30, 86, 2, 2)
            self.init_colors()

    def fill_back(self):
        row =0
        for _ in range(0,38):
            text = '*'*121
            self.back_win.addstr(row, 0, text)
            row += 1
        self.back_win.refresh()

    def write_main(self, text, player_name=None, row=1, col=1):
        self.main_win.erase()
        if isinstance(text, list):
            for line in text:
                if line == " ": row += 1
                if player_name is not None: line = replace_player_name(line, player_name)
                self.main_win.addstr(row, col, line, curses.A_BOLD)
                row +=1
        elif isinstance(text, basestring):
            if player_name is not None: text = replace_player_name(text, player_name)
            lines = textwrap.wrap(text, CHARS_PER_LINE)
            for line in lines:
                self.main_win.addstr(row, col, line, curses.A_BOLD)
                row += 1
        else:
            self.main_win.addstr('Error: did not receive list of strings or string')
        self.main_row = row

    def write_main_artifact(self, text):
        row  = self.main_row + 1
        if isinstance(text, list):
            for line in text:
                if line == " ": row += 1
                self.main_win.addstr(row, ui.COL, line)
                row +=1

    def write_main_mid(self, text):
        row = self.main_row + 1
        lines = textwrap.wrap(text, CHARS_PER_LINE)
        for line in lines:
            self.main_win.addstr(row, ui.COL, line)
            row += 1
        self.main_win.refresh()

    def write_main_bottom(self, text):
        self.main_win.addstr(29, 1, text, curses.color_pair(4))
        self.main_win.refresh()

    def write_input(self, text, row=0, col= 30):
        self.input_win.addstr(row, col, text)

    def write_stat(self, text):
        self.stat_win.erase()
        row = 1
        lines = textwrap.wrap(text, 26)
        for line in lines:
            self.stat_win.addstr(row, ui.COL, line)
            row += 1
        self.stat_win.refresh()

    def write_time(self, text):
        self.time_win.erase()
        row = 1
        for line in text:
            self.time_win.addstr(row, ui.COL, line)
            row += 1

    def refresh_all(self):
        self.stat_win.refresh()
        self.input_win.refresh()
        self.time_win.refresh()
        self.main_win.refresh()

    def end_windows(self):
        curses.endwin()


    def get_input(self, comment=''):
        curses.echo()
        self.input_win.erase()
        self.input_win.addstr(0, 0, comment)
        self.input_win.addstr(2, 1, '->')
        self.input_win.refresh()
        text = self.input_win.getstr(2, 3, 80)
        curses.noecho()
        return text

    def terminal_size(self):
        """
        validates that the terminal is a large enough size to play 
        the game in curses
        """
#        rows, columns = os.popen('stty size', 'r').read().split()
        rows, columns = subprocess.check_output(['stty','size']).decode().split()
        if int(rows) >= int(MIN_ROWS) and int(columns) >= int(MIN_COLS):
            return True 
        return False

    def init_colors(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    def print_help(self):
        """
            prints the actual help menu
        """
        self.main_win.erase()
        x, y = self.print_text(4,2,"Verb       ", curses.A_BOLD)
        x, y = self.print_text(x,y,"::", curses.color_pair(2))
        x, y = self.print_text(x,y,"  Explanation of verb usage")
        for key in VERB_DICT:
            y += 2
            x = 4
            self.print_text(x,y,key, curses.A_BOLD)
            self.print_text(15,y,"::",  curses.color_pair(2))
            self.print_text(19,y,VERB_DICT[key])

    def print_text(self, x, y, text, attribute=None):
        """
            prints the text into the window given and refreshes
        """
        for ch in text:
            if attribute == None:
                self.main_win.addstr(int(y),int(x),ch)
            else:
                self.main_win.addstr(int(y),int(x),ch, attribute)
            x+=1
            time.sleep(random.uniform(0.03, 0.005))
            self.main_win.refresh()
        return x, y


    #------------------------------------------------------
    #This ends the UI curses section
    #------------------------------------------------------

