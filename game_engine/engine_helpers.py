"""
Filename - engine_helpers.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description -
"""




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

