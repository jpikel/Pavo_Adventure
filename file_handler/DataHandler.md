

Filename: gen_dicts.py

Description: Provides a menu to add a room or item alias
or to regenerate the room dict and item dict
adding a room or item alias adds it the corresponding dict as well
as adding it to the room files that use this room as a connection and
the correct item file
Also allows to add verb aliases to the verb_dict

run as $py gen_dicts.py


Filename: file_lib.py

    example usage shown in example.py

    concept: the idea here is to give the game_engine a single class to interact
    with that will give it access to all the attributes of the room with some
    additional things handled here, such as writting the current room out to file,
    loading and store the next room in an object.  hopefully this will be helpful

    Class: game_ops()
        new_game()
            removes all room files from the temp save folder and copies a 
            complete set of original room files from the /data/rooms directory
            also copies a complete set of item files to the temp save folder
            returns bool on success

        get_room_title()
            returns a string of the room title aka name

        get_room_desc()
            checks if the room has been previously visited and
            returns the appropriate description

        attempt_move(String = Official Room Title, List = item names in inventory)
            validates if the string passed in is a connected room to the
            current room. stores the current room, loads the connecting room.
            validate's against a list of items in the inventory
            
            returns an object
                {
                    "move": boolean, specifies if the move was succesful,
                    "description": string, the new or old room description or failed move,
                    "distance_from_room": integer, distance traveled,
                    "title": string, new room's title

                }

            @alex if the game engine could pass me the list of item names in the
            character's inventory then I can check in the save game file if
            the item has been activated

        look()
           returns
           {
            "description": long description of current room
           }

        verb(title = string, verb = string, in_inventory=boolean)
            title can be an item or feature
            verb can be any verb including lookat

            will return an object that currently holds
            {
                "description":string, of some commentary about the combination of the
                                title and verb
            }
