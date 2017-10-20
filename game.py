"""
Filename: game.py
Team: Pavo
Members: Emily Caveness, Alexander Laquitara, Johannes Pikel
Class: CS467-400
Assignment: CMD1:Adventure
Description:
"""
import sys
import json
import file_handler.file_lib as files
import file_handler.help_file as help_file
from file_handler.name_lists import verb_info as verbs
import language_parser.command_parser as parse
import game_engine.player as player
from game_engine.engine_helpers import response_struct

#experiment text wrapping
import textwrap
CHARS_PER_LINE = 80

ALL_VERBS = verbs().get_verbs()

class Game:
    def __init__(self, player):
        self.player = player
        self.current_room = None
        # Inventory will be a list of dicts, each element of which is an item.
        self.current_time = 0
        self.number_of_turns = 0

    #-------------------------------------------------------------------------
    # Methods for managing game start, end, and basic flow
    #-------------------------------------------------------------------------
    def newGame(self):
        print "new Game"
        files.new_game()
        #New games start at the shore
        self.current_room = files.load_room("shore")

        #for testing purposes load a specific room and start from there
        #self.current_room = files.load_room('river')
        self.gameCycle()

    def loadGame(self):
        print "load game"
        gO = game_ops()
        if gO.load_game():
           #here we need to load in all the saved data to engine
           g = Game(None, None, None, None, None, "night")
           self.gameCycle()
        return

    def exitGame(self):
        print "Thanks for playing"

    def startGame(self):
        print"****************************************************************************"
        print""
        print" ########  ########  ######   #######  ##          ###    ######## ######## "
        print" ##     ## ##       ##    ## ##     ## ##         ## ##      ##    ##       "
        print" ##     ## ##       ##       ##     ## ##        ##   ##     ##    ##       "
        print" ##     ## ######    ######  ##     ## ##       ##     ##    ##    ######   "
        print" ##     ## ##             ## ##     ## ##       #########    ##    ##       "
        print" ##     ## ##       ##    ## ##     ## ##       ##     ##    ##    ##       "
        print" ########  ########  ######   #######  ######## ##     ##    ##    ######## "
        print ""
        print ""
        print"          ##  #######  ##     ## ########  ##    ## ######## ##    ## "
        print"          ## ##     ## ##     ## ##     ## ###   ## ##        ##  ##  "
        print"          ## ##     ## ##     ## ##     ## ####  ## ##         ####   "
        print"          ## ##     ## ##     ## ########  ## ## ## ######      ##    "
        print"    ##    ## ##     ## ##     ## ##   ##   ##  #### ##          ##    "
        print"    ##    ## ##     ## ##     ## ##    ##  ##   ### ##          ##    "
        print"     ######   #######   #######  ##     ## ##    ## ########    ##    "
        print""
        print"*****************************************************************************"
        print"Welcome To Desolate Journey"
        print"What would you like to do?"
        print"->  New Game"
        print"->  Load Game"
        print"->  Quit"

        choice = raw_input("-> ")
        choiceLow=str.lower(choice)

        newgame = ["new", "new game", "n", "newgame"]
        loadgame = ["load", "load game", "l", "loadgame"]
        quit = ["quit", "q", "close", "exit" , "quit game", "close game", "exit game"]
        cmds = [newgame, loadgame, quit]

        while (not choiceLow in cmds[0] and 
                not choiceLow in cmds[1] and 
                not choiceLow in cmds[2]):
            print "Please Choose from the menu"
            print"  New Game"
            print"  Load Game"
            print"  Quit"
            choice = raw_input("-> ")
            choiceLow = str.lower(choice)

        if choiceLow in cmds[0]:
            self.newGame()
        elif choiceLow in cmds[1]:
            self.loadGame()
        else:
            self.exitGame()

    def gameCycle(self):
        #inital room description after new game or loading game
        lines = textwrap.wrap(self.get_room_desc(), CHARS_PER_LINE)
        for line in lines: print line
        print self.getTimeOfDay()
        self.player.updatePlayerCondition(self.number_of_turns)
        print self.player.getCondition()
        #updated this while loop the previous one did not seem to evaluate the 
        #dead correctly
        while True:
            print "What would you like to do?"
            userInput = raw_input("->")
            processed_command = parse.parse_command(userInput)
            # If the game does not understand the user's command, prompt the
            # user for a new command.
            while processed_command['other']['processed'] == False:
                print "Sorry I did not understand that."
                print "What would you like to do?"
                userInput = raw_input("->")
                processed_command = parse.parse_command(userInput)
            # If the game understands the user's command, process that command
            # according to the command type.
            output_type = processed_command["type"]

            #line below for testing
            #print json.dumps(processed_command, indent=4)

            #this is temporary and may very well be removed
            #just a possible option to help with assigning title and action
            top_level = ["item", "room", "feature", "general"]
            for word in top_level:
                if word in processed_command:
                    if "name" in processed_command[word]:
                        title = processed_command[word]["name"]
                    if "action" in processed_command[word]:
                        action = processed_command[word]["action"]

            if output_type == "item_action":
                self.process_item_action(title, action)
            elif output_type == "action_only":
                self.process_action_only(action)
            elif output_type == "room_action":
                self.process_room_action(title, action)
            elif output_type == "exit":
                exit_direction = processed_command["exit"]["direction"]
                exit_name = processed_command["exit"]["exit"]
                self.process_exit(exit_direction, exit_name)
            elif output_type == "exit_only":
                exit_name = processed_command["exit"]["exit"]
                self.process_exit_only(exit_name)
            elif output_type == "item_only":
                self.process_item_only(title)
            elif output_type == "feature_action":
                self.process_feature_action(title, action)
            elif output_type == "feature_only":
                self.process_feature_only(title)
            elif output_type == "room_only":
                self.process_room_only(title)
            else:
                "Error command type not supported yet."

            if self.player.get_death_status() or self.player.get_rescue_status():
                break

    #-------------------------------------------------------------------------
    # Top-level methods for handling user commands.
    #-------------------------------------------------------------------------
    def process_item_action(self, title, action):
        if title in self.player.get_items_inventory_titles():
            res = self.item_action_inventory(title, action)
        else:
            res = self.item_action_room(title, action)
        self.post_process(res)

    def process_action_only(self, action):
        res = response_struct().get_response_struct()
        if action == "look":
            res['description'] = self.get_room_long_desc()
        elif action == "inventory":
            res['description'] = self.player.print_inventory()
        elif action == "help":
            help_file.main()
            return
        else:
            #also sent to the funny script writer
            res['description'] = "place holder for funny + verb"
        self.post_process(res)
        
    def process_room_action(self, room, action):
        res = self.room_action(room, action)
        self.post_process(res)

    def process_exit(self, exit, name):
        print "TODO: Write this function"
        print "This is a stub function for handling exit commands!"

    def process_exit_only(self, name):
        print "TODO: Write this function"
        print "This is a stub function for handling exit only commands!"

    def process_item_only(self, name):
        print "TODO: Write this function"
        print "This is a stub function for handling item_only commands!"

    def process_feature_action(self, feature, action):
        res = self.feature_action(feature, action)
        self.post_process(res)

    def process_feature_only(self, feature):
        print "TODO: Write this function"
        print "This is a stub function for handling feature only commands!"

    def process_room_only(self, room):
        print "TODO: Write this function"
        print "This is a stub function for handling room only commands!"

    #-------------------------------------------------------------------------
    # The post process function, handles printing descriptive text
    # and assigning the various update functions as necessary
    #-------------------------------------------------------------------------
    def post_process(self, res):
        """
        divides handling printing, updating character, inventory
        updating room's dynamically
        """
        self.number_of_turns += 1
        #at some point in the future hopefully this will be where
        #we can send parts to the room to be updated if appropriate
        #and the player state if for instance the player has 
        #eaten something and gets a boost to hunger

        #uncomment for troubleshooting
        #print(json.dumps(res, indent=4))

        #update the player with any particular modifiers from the action
        self.update_player(res)
        self.update_room(res)
        #print self.current_room['items_in_room']
        self.update_item(res)
        lines = textwrap.wrap(res['description'], CHARS_PER_LINE)
        for line in lines: print line
        if 'artifact' in res:
            lines = res['artifact']
            for line in lines: print line
        if not self.player.get_death_status():
            print self.getTimeOfDay()
            print self.player.getCondition()

        #description should always come with process functions so we 
        #automatically print out something to the user

    #-------------------------------------------------------------------------
    # This section dedicated to functions relating to moving from one
    # room to another
    #-------------------------------------------------------------------------
    def room_action(self, title_or_compass, action):
        """
            tries to move to the passed in room title or compass direction
            also expects a list of items currently held in the inventory
            defaults to None
        """
        res = self.check_connections(title_or_compass)
        if action == "go":
            if res["success"] == True:
                files.store_room(self.current_room)
                self.current_room = files.load_room(res['title'])
                res['description'] = self.get_room_desc()
            elif res['success'] == False and res['description'] is None:
                res['description'] = "You were not able to move in that direction.  "
        else:
            res['description'] = "You can't " + action + " the " + title_or_compass+". "
        return res

    def check_connections(self, title_or_direction):
        """
        when given an official room title or compass direction, iterates
        through the current room's connected_rooms object to see if the compass
        or room title exist
        checks if an item is required to pass into this room
        Also checks if the rooms is accessible meaning passable
        if an item is required checks to see if that item is active as in worn or on
        writes the appropriate response into
        description
        move = boolean whether or not the move was successful
        title = the new room's title
        distance_from_room = distance traveled to the new room
        """
        res = response_struct().get_response_struct()
        res['success'] = False
        items = self.player.get_items_inventory_titles()
        for room_key in self.current_room['connected_rooms']:
            #this line added as a result of the connected_rooms refactoring
            #all other functionality remains the same
            room = self.current_room['connected_rooms'][room_key]
            if (title_or_direction == room['title']
                or title_or_direction == room['compass_direction']
                or title_or_direction in room['aliases']):
                res['title'] = room['title']
                if 'modifiers' in room:
                    res['modifiers'] = room['modifiers']
                if (room['item_required'] == True and
                    room['item_required_title'] in items and
                    room['accessible'] == True):
                        item = self.player.search_inventory(room['item_required_title'])
                        if item['active'] == True:
                            res['success'] = True
                            res['distance_from_room'] = room['distance_from_room']
                        else:
                            res['description'] = room['pre_item_description']
                elif room['item_required'] == False and room['accessible'] == True:
                    res['success'] = True
                    res['distance_from_room'] = room['distance_from_room']
                    res['description'] = room['pre_item_description']
                else:
                    res['description'] = room['pre_item_description']
        return res
    #------------------------------------------------------------------------
    # This ends the movement related functions
    #------------------------------------------------------------------------
    #------------------------------------------------------------------------
    # This begins room getters section
    #------------------------------------------------------------------------

    def get_room_desc(self):
        """
            returns either the long or short description
            if the room has been previously visited
        """
        if self.get_visited() == False:
            return self.get_room_long_desc()
        else:
            return self.get_room_short_desc()

    def get_room_long_desc(self):
        """
        returns a string of the long description and items in room
        """
        return self.current_room['long_description'] + self.get_items_in_room()

    def get_room_short_desc(self):
        """
        returns a string of the short description and items in room
        """
        return self.current_room['short_description'] + self.get_items_in_room()

    def get_items_in_room(self):
        """
        if the room has been searched appropriately and there are items in the room
        then returns the items in the room as a string for descriptive purposes
        """
        text = " Looking around you see "
        if (self.current_room['feature_searched'] == True and
                self.current_room['items_in_room']):
            items = self.current_room['items_in_room']
            for item in items:
                text += "a " + item + ", "
            text = text[:-2]
        else:
            text = ""
        return text

    def get_visited(self):
        """
        returns the boolean in visited
        """
        return self.current_room['visited']
    #------------------------------------------------------------------------
    # This ends room getters section
    #------------------------------------------------------------------------
    #------------------------------------------------------------------------
    # This begins room modifiers section
    #------------------------------------------------------------------------
    def remove_item_from_room(self, title):
        """
        removes an items from the inventory of a room
        do not attempt to remove something not already there
        """
        if title in self.current_room['items_in_room']:
            self.current_room['items_in_room'].remove(title)

    def add_item_to_room(self, title):
        """
        adds an item to the room, does not allowed for duplicates
        """
        if title not in self.current_room['items_in_room']:
            self.current_room['items_in_room'].append(title)
    #------------------------------------------------------------------------
    # This ends the room  section
    #------------------------------------------------------------------------
    #------------------------------------------------------------------------
    # This begins the feature related section
    #------------------------------------------------------------------------

    def feature_action(self, title, verb):
        """
            looks up to see if the title passed in is a feature in the current room
            if so and the verb is in the list of possible verbs for that feature then
        """
        res = response_struct().get_response_struct()
        features = self.current_room['features']
        for element in features:
            if title == features[element]['title']:
                feature = element
        if feat is not None and verb in feature['verbs']:
            text = feature['verbs'][verb]['description']
            res['description'] = text
            res['modifiers'] = feature['verbs'][verb]['modifiers']
        else:
            res['description'] = self.verb_not_found + " " + verb + " the " + title
        return res
    #------------------------------------------------------------------------
    # This ends the feature section
    #------------------------------------------------------------------------
    #------------------------------------------------------------------------
    # This section relates to item actions
    #------------------------------------------------------------------------

    def item_action_inventory(self, item_title, action):
        """
        called by the verb handler.  Looks up the item file and opens it
        returns the description listed for the particular verb at this moment.
        FUTURE: include additional parts of the structure to return to the game engine
            {
            "description": string
            }
        """
        res = response_struct().get_response_struct()
        item = self.player.search_inventory(item_title)
        res['title'] = item_title
        res["description"] = item['verbs'][action]['description']
        res['modifiers'] = item['verbs'][action]['modifiers']
        res["success"] = True
        if 'artifact' in item['verbs'][action]:
            res['artifact'] = item['verbs'][action]['artifact']
        if action == "use" and item['activatable'] == True:
            if item['active'] == True:
                item['active'] = False
                res['description'] = item['verbs']['use']['deactivate_description']
            else:
                item['active'] = True
        elif action == "drop" and self.current_room['feature_searched'] == False:
            res['description'] = "There is no where secure to drop the item"
            res['modifiers'] = {}
        return res

    def item_action_room(self, title, verb):
        """
        acts on an item in the room only the look at verb is allowed at this moment
        adds the item to the inventory as well if it is 
        """
        res = response_struct().get_response_struct()
        res['title'] = title
        allowed_verbs = ["look at", "take"]
        if self.current_room['feature_searched'] and verb in allowed_verbs:
            if title in self.current_room['items_in_room']:
                item = files.load_item(title)
                #print item
                res['description'] = item['verbs'][verb]['description']
                res['modifiers'] = item['verbs'][verb]['modifiers']
                res["success"] = True
            else:
                text = "You can't find the " + title + " to " + verb +". "
                res['description'] = text
        elif self.current_room['feature_searched'] and verb not in allowed_verbs:
            res['description'] = "Trying picking up " + title + " to " + verb + " it."
        else:
            res['description'] = "You don't see any items around. "
        return res

    #------------------------------------------------------------------------
    # This ends the items and inventory section
    #------------------------------------------------------------------------

    #-------------------------------------------------------------------------
    # Methods that are used in otherwise managing game flow.
    # and updating the room, player and items
    #-------------------------------------------------------------------------
    def update_room(self, res):
        """
        this function is used to update the current room's parameters
        """
        #this is the add and rop to rooms
        #if dropping is allowed is handled above in the item_action_room
        if "modifiers" in res and "room" in res['modifiers']:
            mods = res['modifiers']['room']
            if self.current_room['title'] == mods['title'] or "any" == mods['title']:
                if "items_in_room" in mods and mods['items_in_room'] == "add":
                    self.add_item_to_room(res['title'])
                elif "items_in_room" in mods and mods['items_in_room'] == "drop":
                    self.remove_item_from_room(res['title'])

        #This is the test of the the dynamic room updates
        #Since all titles are unique that is our identifier!! very important
        #it can only currently update the room the player is in, so no
        #outside rooms, but we could easily change that
        #we just need to make sure that our rules about what can change
        #what are consistent.  that comes from the way the 'updates' dict
        #is written in the 'modifiers' dict for a particular verb of a feature
        #or an item
        if 'modifiers' in res and 'room_updates' in res['modifiers']:
            for key in res['modifiers']['room_updates']:
                updates = res['modifiers']['room_updates'][key]
                if self.current_room['title'] == key:
                    self.current_room = files.update(updates, self.current_room)
                #for now we can only affect adjacent rooms so check if the key is 
                #in the set of connected_rooms for the current_room
                elif key in self.current_room['connected_rooms']:
                    other_room = files.load_room(key)
                    other_room = files.update(updates, other_room)
                    files.store_room(other_room)

        #hopefully file_lib will have a method where we can pass the 
        #modifiers dict to and it will do the remaining processing returning 
        #the updated room so we can just do 

    def update_player(self, res):
        """
        This function is used to update player state variables, including
        player inventory
        """

        if 'modifiers' in res and 'player' in res['modifiers']:
            modifiers = res['modifiers']['player']
            if 'inventory' in modifiers and modifiers['inventory'] == 'add':
                item = files.load_item(res['title'])
                self.player.add_item_to_inventory(item)
            elif 'inventory' in modifiers and modifiers['inventory'] == 'drop':
                #when the player drops the item it gets written to file
                item = self.player.search_inventory(res['title'])
                if item:
                    files.store_item(item)
                self.player.remove_item_from_inventory(res['title'])
            if 'illness' in modifiers:
                self.player.set_illness(int(modifiers['illness']))

        #after modifiers have been applied update the player's condition
        self.player.updatePlayerCondition(self.number_of_turns)
        #maybe incorporate the player condition updates here so we can
        #include things like hunger, illness etc in the modifiers

    def update_item(self, res):
        """
        this function is used to an item's dict.
        """
        if 'modifiers' in res and 'item_updates' in res['modifiers']:
            for key in res['modifiers']['item_updates']:
                updates = res['modifiers']['item_updates'][key]
                #first check if the item is in the player inventory and update that
                item = self.player.search_inventory(key)
                if item is not None:
                    item = files.update(updates, item)
                #if the item is not in the player inventory maybe it is in the room
                #and we can act upon it.  This maybe needs to go away
                elif key in self.current_room['items_in_room']:
                    print 'item is in room'
                    item = files.load_item(key)
                    item = files.update(updates, item)
                    files.store_item(item)

    def getTimeOfDay(self):
        if self.number_of_turns % 4 == 0:
            text = " It is morning. "
        elif self.number_of_turns % 4 == 1:
            text = " It is afternoon. "
        elif self.number_of_turns % 4 == 2:
            text = " It is evening. "
        elif self.number_of_turns % 4 == 3:
            text = " It is night. "
        return text

    #suggest update player conditions relocated to the helper file player.py
#    def updatePlayerCondition(self):
#        # Degrade the player's condition every three moves.
#        if self.number_of_turns % 3 == 0:
#            self.player.illness += 1
#        if (self.player.illness > 50 or
#            self.player.hunger > 50 or
#            self.player.cold > 50):
#            self.player.dead = True


    #-------------------------------------------------------------------------
    # Temporary code used for testing
    #-------------------------------------------------------------------------

def testParse():
    test_input = "go cave"
    print "The test input is: " + test_input
    print "The parsed command output is:"
    print parse.parse_command(test_input)
    print parse.parse_command(test_input)['room']['action']
    print parse.parse_command(test_input)['room']['name']
    print parse.parse_command(test_input)['other']['processed']
    print parse.parse_command(test_input)['room']['action']
    # parse.parse_command(test_input[0,0])
    print ""


#testParse()
#startGame()
#loadGame()
#newGame()
#playerDead()
#testNew()
#print(sys.path)


def main():
    current_player = player.Player("Test Player")
    current_game = Game(current_player)
    user_choice = current_game.startGame()


if __name__ == "__main__":
    main()
