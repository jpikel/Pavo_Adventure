"""
Filename - admin_menu.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - A simple menu to help navigate to different parts of handling
dicts, alias entry, validation etc.
"""

import file_handler.gen_dicts as gen_dicts
import file_handler.modify_dicts as modify_dicts




def main():
    """
    the main menu of options
    """
    print("\nWhat would you like to do?\n"
          "1. Add aliases, generate dict files\n"
          "2. Validate files, modify key/values pairs\n"
          "q. Quit\n")
    selection = raw_input(":")
    if selection == "1":
        gen_dicts.main()
    if selection == "2":
        modify_dicts.main()
    if selection == "q":
        exit()

    main()





if __name__ == "__main__":
    main()
