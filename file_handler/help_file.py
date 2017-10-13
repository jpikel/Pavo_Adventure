"""
Filename - helpfile
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - 
"""

import sys
import curses
import locale
from name_lists import verb_info

def print_border():

    print_stars_line(40)
    sys.stdout.write("Help")
    print_stars_line(40)
    print_stars_two_cols(35)

    print_stars_line(83)

def print_stars_line(number):
    """
    prints x number of *
    """
    for _ in range(0, number):
        sys.stdout.write("*")

def print_stars_two_cols(num):
    """
    prints two columns of stars spaced 84 chars apart
    """
    for _ in range(0, num):
        sys.stdout.write("*")
        sys.stdout.write("*")
    print "*".ljust(83)

def move_cursor_x(num):
    """
    moves the cursor across the screen x cols
    """


def main():
    """
        a simple print to screen of the help file
    """
    verb_dict = verb_info().get_verb_definitions()
    print_border()
    print("\nVerb       :: Action taken\n\n")
    for key in verb_dict:
        print(key.ljust(10) + " :: " +verb_dict[key])

    print("\n\n")

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()
    main()
