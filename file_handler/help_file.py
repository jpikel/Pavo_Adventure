"""
Filename - helpfile
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - 
"""

import sys
USE_CURSES = False
if sys.platform == 'linux' or sys.platform == 'linux2':
    import curses
    USE_CURSES = True

import locale
import random
import time
import os
from name_lists import verb_info

MIN_COLS = 90
MIN_ROWS = 55
VERB_DICT = verb_info().get_verb_definitions()

def print_border(stdscr):

    print_stars(83, stdscr)
    print_stars_two_cols(41, stdscr)

def print_stars(number, stdscr):
    """
    prints x number of *
    """
    col = 1
    color_pair = 1
    for _ in range(0, number):
        stdscr.addstr(0, col, "*", curses.color_pair(color_pair))
        stdscr.addstr(40, col, "*", curses.color_pair(color_pair))
        col += 1
        color_pair +=1
        if color_pair > 4:
            color_pair = 1
        time.sleep(0.03)
        stdscr.refresh()

def print_stars_two_cols(num, stdscr):
    """
    prints two columns of stars spaced 84 chars apart
    """
    row = 0
    color_pair = 1
    for _ in range(0, num):
        stdscr.addstr(row, 1, "*", curses.color_pair(color_pair))
        stdscr.addstr(row, 83, "*", curses.color_pair(color_pair))
        color_pair += 1
        if color_pair > 4:
            color_pair = 1
        row += 1
        time.sleep(0.03)
        stdscr.refresh()

def init_colors():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

def print_text(x, y, text, window, attribute=None):
    """
        prints the text into the window given and refreshes
    """
    for ch in text:
        if attribute == None:
            window.addstr(int(y),int(x),ch)
        else:
            window.addstr(int(y),int(x),ch, attribute)
        x+=1
        time.sleep(random.uniform(0.05, 0.008))
        window.refresh()
    return x, y

def print_help(stdscr):
    """
        prints the actual help menu
    """
    x, y = print_text(4,4,"Verb       ", stdscr, curses.A_BOLD)
    x, y = print_text(x,y,"::", stdscr, curses.color_pair(2))
    x, y = print_text(x,y,"  Explanation of verb usage", stdscr)
    for key in VERB_DICT:
        y += 2
        x = 4
        print_text(x,y,key, stdscr, curses.A_BOLD)
        print_text(15,y,"::", stdscr,  curses.color_pair(2))
        print_text(19,y,VERB_DICT[key], stdscr)

def main_helper(stdscr):
    init_colors()
    print_border(stdscr)
    print_help(stdscr)
    print_text(0,45,"\n", stdscr)
    x = stdscr.getch()
    stdscr.clear()
    stdscr.refresh()
    curses.endwin()

def print_basic():
    print '*'*20,
    print 'Help',
    print '*'*20
    print 'Verb'.ljust(12) + ' :: ' + ' verb definition'
    for key in VERB_DICT:
        print key.ljust(12) + ' ::  ' + VERB_DICT[key]

def terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    if int(rows) < int(MIN_ROWS) or int(columns) < int(MIN_COLS):
        return False
    return True

def main(stdscr=None):
    """
        a simple print to screen of the help file
    """
    if USE_CURSES and terminal_size():
        locale.setlocale(locale.LC_ALL, '')
        code = locale.getpreferredencoding()
        if stdscr == None:
            curses.wrapper(main_helper)
        else:
            main(stdscr)
    else:
        print_basic()
       
if __name__ == "__main__":
    if USE_CURSES and terminal_size():
        curses.wrapper(main)
    else:
        print_basic
