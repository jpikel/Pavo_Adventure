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
        "title":string
        "description": string
        "move": boolean, whether the move occured
        "distance_from_room": distance travel
    """
    def __init__(self):
        self.response = {
                    "title":None,
                    "description":None,
                    "success":False,
                    "distance_from_room":0
                }

    def get_response_struct(self):
        return self.response

