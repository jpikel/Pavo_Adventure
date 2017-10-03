"""
Filename - helpfile
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - 
"""

from name_lists import verb_info

class help():
    verb_dict = verb_info().get_verb_definitions()
    def display_help(self):
        print("\n\n*******Help*******\n\n")
        print("Verb       :: Action taken\n\n")
        for key in self.verb_dict:
            print(key.ljust(10) + " :: " + self.verb_dict[key])

        print("\n\n")
