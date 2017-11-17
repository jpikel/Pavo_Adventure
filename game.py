#!/usr/bin/python2.7
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
import pdb  #toggle off in main
import file_handler.file_lib as files
import language_parser.command_parser as parse
import game_engine.player as player
import game_engine.room as room
import game_engine.engine_helpers as helpers
import random

#FOR DELETEION
#from file_handler.name_lists import verb_info as verbs
#from game_engine.engine_helpers import response_struct
#import file_handler.help_file as help_file
#ALL_VERBS = verbs().get_verbs()
#END FOR DELETION

USE_CURSES = False
if sys.platform == 'linux' or sys.platform == 'linux2':
    import curses
    USE_CURSES = True
    game_ui = helpers.ui()
    if game_ui.terminal_size() == False:
        USE_CURSES = False

DO_WHAT = 'What would you like to do?'

#DEBUG SECTION, you can set these values to 1 to get the desired affect
#later in the game engine
#if set to 1 prints the value returned from the parser
DEBUG_PARSE = 0
#if set to 1 prints the value in the response json from the action_item etc
DEBUG_RESPONSE = 0
#prints the entire room json after it has been updated in post process
DEBUG_ROOM = 0
#prints the current room's title at the begining of each cycle
#comes after the description etc
DEBUG_PRINT_ROOM_TITLE = 0
#loads into a specific room set in the newGame()
LOAD_SPECIFIC_ROOM_ON_NEW_GAME = 0
SPECIFIC_ROOM = 'river'
#this stops all the player attributes from being updated each round
#such as illness, wounds and cold, allows rescue but not death
GOD_MODE = 0
#toggle on/off to randomize player input
RANDOM_TESTER = 0
#mirror input for testing purposes only
MIRROR_INPUT = 0
#player is automatically rescued after 1 turn for testing purposes
PLAYER_RESCUED =0

if DEBUG_PARSE or DEBUG_ROOM:
    USE_CURSES = False


class Game():
    def __init__(self):
        self.player = player.Player()
        self.room = room.Room()
        # Inventory will be a list of dicts, each element of which is an item.
        self.current_time = 0
        self.number_of_turns = 0
        self.saved = False

    #-------------------------------------------------------------------------
    # Methods for managing game start, end, and basic flow
    #-------------------------------------------------------------------------
    def startGame(self, is_new_game):
        """
        Prints a splash to the screen and allows the user to load a game
        or start a new game
        """
        newgame = ["new", "new game", "n", "newgame"]
        loadgame = ["load", "load game", "l", "loadgame"]
        quit = ["quit", "q", "close", "exit" , "quit game", "close game", "exit game"]
        cmds = [newgame, loadgame, quit]
        invalid_message = "Please choose new game, load game or quit: "
        #preload choiceLow so we get the invalid message automatically when
        #not a new game
        choiceLow = ""

        if is_new_game:
            #print the big splash page here!
            self.write_main_handler(helpers.SPLASH_MESSAGE, col=5)
            self.ui_refresh()
            choiceLow = self.input_handler()
        while (not choiceLow in cmds[0] and
            not choiceLow in cmds[1] and
            not choiceLow in cmds[2]):
            choiceLow = self.input_handler(invalid_message)
        if choiceLow in cmds[0]:
            self.newGame()
            self.gameCycle()
        elif choiceLow in cmds[1]:
            self.load_from_file()
            self.gameCycle()
        else:
            self.exitGame()

    def newGame(self):
        """
        copies the files over from template dir to the temp save dir
        and starts a new player
        """
        files.new_game()
        self.player = self.gen_player()
        #New games start at the shore
        self.room.current_room = files.load_room("shore")
        self.validate_object(self.room.current_room, 'shore')
        #for testing purposes load a specific room and start from there
        if LOAD_SPECIFIC_ROOM_ON_NEW_GAME:
            self.room.current_room = files.load_room(SPECIFIC_ROOM)
            self.validate_object(self.room.current_room, SPECIFIC_ROOM)

    def load_from_file(self):
        """
        gets the player and room files from the save game dir.  moves the room and items
        files to the temp save dir.  Restores the player state
        """
        p, success, msg = files.load_game()
        if success == True and p is not None and 'current_room' in p:
            r = files.load_room(p['current_room'])
            self.validate_object(r, p['current_room'])
        elif success == False:
            r = files.load_room('shore')
            self.validate_object(r, 'shore')
            self.write_main_bottom_handler(msg)
        else:
            text = 'Something went wrong loading the rooms in loadgame.'
            self.write_main_handler(text)
            self.exitGame()
        #if something went wrong returning the player from the
        #checking for False because p could return as False if the files did not
        #get copied correctly
        self.room.current_room = r
        if p is None:
            self.player = self.gen_player()
        else:
            #load player info from saved game
            self.player = self.player.set_player_stats(p)
            self.number_of_turns = p['turns']
            self.reset_art()

    def exitGame(self):
        """
            prints a good bye message and exits
        """
        if USE_CURSES: game_ui.end_windows()
        helpers.multi_printer("Thanks for playing")
        exit()

    def gen_player(self):
        """
        this function asks the player to enter a name and then creates a new player
        object that the game holds on to for future use
        """
        player_name = self.input_handler('Hello dreary traveler. What is your name? ')
        return player.Player(player_name)
    
    
    def gameCycle(self):
        """
        This is the big game cycle
            get user input
                check if savegame, loadgame, or quit
            otherwise send to parser
            process the parsed command
            output to screen
            update player
            update rooms
            update items
            check if dead or rescued
        """
        #inital room description after new game or loading game
        self.player.updatePlayerCondition(self.number_of_turns, 0)
        self.write_main_handler(self.room.get_room_desc)
        self.write_main_artifact_handler(self.room.get_room_artifact)
        self.write_time_handler(self.getTimeOfDay())
        self.write_stat_handler(self.player.getCondition())
        self.ui_refresh()
        #updated this while loop the previous one did not seem to evaluate the
        #dead correctly
        while True:
            if DEBUG_PRINT_ROOM_TITLE:
                self.write_main_bottom_handler('Room: '+self.room.title)

            processed_command = self.input_cycle()
            # If the game understands the user's command, process that command
            # according to the command type.
            output_type = processed_command["type"]
            #this is temporary and may very well be removed
            #just a possible option to help with assigning title and action
            title = None
            action = None
            top_level = ["item", "room", "feature"]
            for word in top_level:
                if word in processed_command['command']:
                    title = processed_command['command'][word]
            if "action" in processed_command['command']:
                action = processed_command['command']['action']

            res = self.process_parsed_command(output_type, title, action)

            if res: self.post_process(res)

            if self.player.get_death_status() or self.player.get_rescue_status():
                #would be good to add a restart loop in here
                #this break should be all that is needed and then we can startGame
                #again to allow loadgame or newgame
                #we submit False to let startGame know this is not a newGame
                #it will not print the Splash screen again
                #works well.  rescued myself with the flare gun !
                break
        self.startGame(False)

    def input_cycle(self):
        """The input cycle continues to request input until we have a valid
        processed command
        """

        processed_command = None
        while True:
            self.validate_curses()
            if (processed_command is not None and
                    processed_command['processed'] == False ):
                text = "Sorry I did not understand that.\n " + DO_WHAT
            else:
                text = DO_WHAT
            if RANDOM_TESTER:
                userInput = random_input_tester()
            else:
                userInput = self.input_handler(text)
                userInput = self.check_save_load_quit(userInput)
            #if we have no userInput skip to asking and check_save_load_quit again
            if userInput == None:
                continue
            processed_command = parse.parse_command(userInput)
            #line below for testing
            if DEBUG_PARSE:
                print json.dumps(processed_command, indent=4)
            if processed_command['processed'] == True:
                return processed_command

    def process_parsed_command(self, output_type, title, action):
        """
        This is the decider than once the parser gives us a result our 
        branching functions are here
        """
        res = None
        if output_type == "item_action":
                if title in self.player.get_items_inventory_titles():
                    res = (self.player.item_action_inventory(
                        title,action,self.room.feature_searched))
                else:
                    res = self.item_action_room(title, action)
        elif output_type == "action_only":
            if action == "look":
                res = helpers.response_struct()
                res.action = 'look'
                res.description = self.room.long_desc
            elif action == "inventory":
                self.write_stat_handler(self.player.print_inventory())
            elif action == "help":
                if USE_CURSES: game_ui.print_help()
                else: helpers.print_basic()
            else:
                #also sent to the funny script writer
                res = self.get_humor(action, 'action')
        elif output_type == "room_action":
            res = self.room_action(title, action)
        elif output_type == "item_only":
            res = self.get_humor(title, 'noun')
        elif output_type == "feature_action":
            res = self.room.feature_action(title, action)
        elif output_type == "feature_only":
            res = self.get_humor(title, 'noun')
        elif output_type == "room_only":
            res = self.room_action(title, 'go')
        else:
            self.write_main_bottom_handler('Error command type not supported yet.')

        return res


    #-------------------------------------------------------------------------
    # This is the check for savegame, loadgame, quit function
    #-------------------------------------------------------------------------
    def check_save_load_quit(self, userInput):
        """
        this functions handles the commands savegame, loadgame and quit when entered
        into the game during play
        """
        #save
        if userInput == "savegame":
            text = 'Are you sure you wish to save y/n'
            checkYes = self.input_handler(text)
            if checkYes == "y":
                files.save_game(self.player, self.room.current_room,self.number_of_turns)
                self.saved = True
                userInput = None
                self.write_main_bottom_handler('Game saved successfully')
            else:
                self.write_main_bottom_handler('continuing game...')
        #load
        elif userInput == "loadgame":
            text = "Loading will exit game current game. Are you sure you wish to load? y/n"
            checkYes = self.input_handler(text)
            self.saved = False 
            if checkYes == "y":
                self.load_from_file()
                userInput = None
                self.write_main_bottom_handler('Game loaded successfully')
                #adding this here so after we successfully load a game we get something
                #back and not just the what do you want to do... maybe better some
                #where else
                res = helpers.response_struct()
                res.description = self.room.long_desc
                res.room_artifact = self.room.get_room_artifact
                res.action = 'look'
                self.post_process(res)
            else:
                self.write_main_bottom_handler('continuing game...')
        #quit
        elif userInput == "quit":
            userInput = None
            if self.saved ==False:
                text = "Are you sure you want to quit without saving? y/n"
                checkYes = self.input_handler(text)
                if checkYes == "y":
                    self.exitGame()
                else:
                    text = 'Do you wish to save and quit? y/n'
                    checkYes = self.input_handler(text)
                    if checkYes == "y":
                        files.save_game(self.player, self.room.current_room, self.number_of_turns)
                        self.exitGame()
                    else:
                        self.write_main_bottom_handler('continuing game...')
            else:
                text = 'Are you sure you want to quit? y/n'
                checkYes = self.input_handler(text)
                if checkYes == "y":
                    self.exitGame()
        else:
            #if one of the above commands was not found we want to reset saved to False
            #because we may have changed something in the game
            self.saved = False
        return userInput

    #-------------------------------------------------------------------------
    # This ends the check for savegame, loadgame, quit
    #-------------------------------------------------------------------------
    #-------------------------------------------------------------------------
    # The post process function, handles printing descriptive text
    # and assigning the various update functions as necessary
    #-------------------------------------------------------------------------
    def post_process(self, res):
        """
        divides handling printing, updating character, inventory
        updating room's dynamically
        """
        self.validate_curses()

        if res.success:
            self.number_of_turns += 1
            if USE_CURSES and self.number_of_turns < 16: game_ui.write_art()
        #at some point in the future hopefully this will be where
        #we can send parts to the room to be updated if appropriate
        #and the player state if for instance the player has
        #eaten something and gets a boost to hunger

        #set DEBUG_RESPONSE to 1 for debuggin
        if DEBUG_RESPONSE:
            print(json.dumps(res.__dict__, indent=4))

        if 'modifiers' in res.response:
            #update the player with any particular modifiers from the action
            self.update_player(res)
            #update the room dict through recursion
            self.update_room(res)
            #update the items dict
            self.update_item(res)

        #after modifiers have been applied update the player's condition
        room_temp = int(self.room.temp)
        if not GOD_MODE:
            self.player.updatePlayerCondition(self.number_of_turns,room_temp)
        if PLAYER_RESCUED:
            self.player.set_rescue(True)
        if DEBUG_ROOM:
            print(json.dumps(self.room.current_room, indent=4))
        #print the messages to screen here
        self.write_main_handler(res.description, self.player.getName)
        if not self.player.get_death_status() and not self.player.get_rescue_status():
            self.write_time_handler(self.getTimeOfDay())
            self.write_stat_handler(self.player.getCondition())
            if res.artifact:
                self.write_main_artifact_handler(res.artifact)
            elif res.action == 'go' or res.action == 'look':
                self.write_main_artifact_handler(self.room.get_room_artifact)
            if res.warning:
                self.write_main_bottom_handler(res.warning)
        elif self.player.get_death_status():
           msg = self.player.get_reason_for_death()
           if USE_CURSES: game_ui.write_main_mid(msg)
           else: helpers.multi_printer(msg)
        elif self.player.get_rescue_status():
            self.write_main_bottom_handler('Press enter to roll the credits')
            userInput = self.input_handler()
            msg= "Congratulations, you survived the Desolate Journey" 
            self.write_stat_handler(msg) 
            self.write_time_handler(helpers.FIREWORKS)
            self.roll_credits_handler()
        self.ui_refresh()

        #description should always come with process functions so we
        #automatically print out something to the user
    #------------------------------------------------------------------------
    # These two functions are in game.py because they deal with loading
    # rooms and items and so we need to validate that a room and item
    # have been successfully loaded.
    #------------------------------------------------------------------------

    def room_action(self, title_or_compass, action):
        """
            tries to move to the passed in room title or compass direction
            also expects a list of items currently held in the inventory
            defaults to None
        """
        res = self.room.check_connections(title_or_compass, self.player.inventory)
        res.action = action
        if action == "go":
            res.action = 'go'
            if res.success == True:
                #before we leave the room we set the field visited to true
                self.room.visited = True
                files.store_room(self.room.current_room)
                self.room.current_room = files.load_room(res.title)
                self.validate_object(self.room.current_room, res.title)
                res.description = self.room.get_room_desc
            elif title_or_compass == self.room.title:
                res.description = 'You are already in that room.'
            elif res.success == False and res.description is None:
                res.description = "You were not able to move in that direction.  "
        elif action == 'look':
            res.action = 'look'
            res.description = self.room.long_desc
            if title_or_compass != self.room.title:
                res.warning = 'You are not in '+title_or_compass+'. But you can look around ' + self.room.title + '.'
        else:
            res.description = "You can't " + action + " the " + title_or_compass+". "
        return res

    def item_action_room(self, title, verb):
        """
        acts on an item in the room only the look at verb is allowed at this moment
        adds the item to the inventory as well if it is
        """
        res = helpers.response_struct()
        res.title = title
        allowed_verbs = ["look at", "take"]
        if self.room.feature_searched and verb in allowed_verbs:
            if title in self.room.current_room['items_in_room']:
                item = files.load_item(title)
                self.validate_object(item, title)
                res.description = item['verbs'][verb]['description']
                res.modifiers = item['verbs'][verb]['modifiers']
            else:
                text = "You can't find the " + title + " to " + verb +". "
                res.description = text
        elif self.room.feature_searched and verb not in allowed_verbs:
            res.description = "You need to be holding " + title + " to " + verb + " it."
        else:
            res.description = "You don't see any items around. "
        return res
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
        if "room" in res.modifiers:
            mods = res.modifiers['room']
            if self.room.title == mods['title'] or "any" == mods['title']:
                if "items_in_room" in mods and mods['items_in_room'] == "add":
                    if self.room.title == 'rapids':
                        res.description += " You watch it float away and it is gone..."
                    else:
                        self.room.add_item_to_room(res.title)
                elif "items_in_room" in mods and mods['items_in_room'] == "drop":
                    self.room.remove_item_from_room(res.title)

        #This is the test of the the dynamic room updates
        #Since all titles are unique that is our identifier!! very important
        #it can only currently update the room the player is in, so no
        #outside rooms, but we could easily change that
        #we just need to make sure that our rules about what can change
        #what are consistent.  that comes from the way the 'updates' dict
        #is written in the 'modifiers' dict for a particular verb of a feature
        #or an item
        if 'room_updates' in res.modifiers:
            for key in res.modifiers['room_updates']:
                updates = res.modifiers['room_updates'][key]
                if self.room.title == key:
                    self.room.current_room = files.update(updates,self.room.current_room)
                #affect any room that is a room other than the current room
                elif key in files.ROOM_TITLES:
                    self.update_external_room(updates, key)
        #this field is used in the modifiers field to only update adjacent rooms
        #this will also validate that the room specified is the current room
        if 'adjacent_room_updates' in res.modifiers:
            if self.room.title == res.modifiers['adjacent_room_updates']['self']:
                for key in res.modifiers['adjacent_room_updates']:
                    if key in self.room.current_room['connected_rooms']:
                        updates = res.modifiers['adjacent_room_updates'][key]
                        self.update_external_room(updates, key)

        #hopefully file_lib will have a method where we can pass the
        #modifiers dict to and it will do the remaining processing returning
        #the updated room so we can just do

    def update_external_room(self, updates, key):
        """
           opens the room file named in the key, updates that room and then
           stores that room back to file
        """
        other_room = files.load_room(key)
        self.validate_object(other_room, key)
        other_room = files.update(updates, other_room)
        files.store_room(other_room)

    def update_player(self, res):
        """
        This function is used to update player state variables, including
        player inventory
        """
        if 'player' in res.modifiers:
            modifiers = res.modifiers['player']
            if 'inventory' in modifiers and modifiers['inventory'] == 'add':
                item = files.load_item(res.title)
                self.validate_object(item, res.title)
                self.player.add_item_to_inventory(item)
            elif 'inventory' in modifiers and modifiers['inventory'] == 'drop':
                #when the player drops the item it gets written to file
                item = self.player.search_inventory(res.title)
                if item:
                    files.store_item(item)
                self.player.remove_item_from_inventory(res.title)
            if not GOD_MODE:
                if 'illness' in modifiers:
                    self.player.add_to_illness(int(modifiers['illness']))
                if 'hunger' in modifiers:
                    self.player.add_to_hunger(int(modifiers['hunger']))
                if 'cold' in modifiers:
                    self.player.add_to_cold(int(modifiers['cold']))
            if 'rescued' in modifiers:
                self.player.set_rescue(modifiers['rescued'])

    def update_item(self, res):
        """
        this function is used to update an item's dict.
        it requires that the field modifiers and item_updates are in the response
        received.  The item must have the same structure as that of an actual item
        file.  The dict trees will be updated with the new information recursively
        """
        if 'item_updates' in res.modifiers:
            for key in res.modifiers['item_updates']:
                updates = res.modifiers['item_updates'][key]
                #first check if the item is in the player inventory and update that
                item = self.player.search_inventory(key)
                if item is not None:
                    item = files.update(updates, item)
                #if the item is not in the player inventory maybe it is in the room
                #and we can act upon it.  This maybe needs to go away
                elif key in self.room.current_room['items_in_room']:
                    item = files.load_item(key)
                    self.validate_object(item, key)
                    item = files.update(updates, item)
                    files.store_item(item)

    def getTimeOfDay(self):
        if USE_CURSES:
            text = []
            if self.player.get_rescue_status():
                text= helpers.FIREWORKS
            else:
                if self.number_of_turns % 4 == 0:
                    text = helpers.MORNING
                elif self.number_of_turns % 4 == 1:
                    text = helpers.AFTERNOON
                elif self.number_of_turns % 4 == 2:
                    text = helpers.EVENING
                elif self.number_of_turns % 4 == 3:
                    text = helpers.NIGHT
        else:
            if self.number_of_turns % 4 == 0:
                text = "It is morning. "
            elif self.number_of_turns % 4 == 1:
                text = "It is afternoon. "
            elif self.number_of_turns % 4 == 2:
                text = "It is evening. "
            elif self.number_of_turns % 4 == 3:
                text = "It is night. "
        return text

    #-------------------------------------------------------------------------
    # This begins the humorous section
    #-------------------------------------------------------------------------
    def get_humor(self, word, type_of):
        """
        depending on whether it is an action or noun puts together a random
        string to return
        """
        action_prefix = ['Sadly you cannot ', 'Nope maybe try to ',
                'Wait... hold on a sec... nope you cannot just ']
        action_post = [' yourself.', ' something in the real world.',
                ' -- every DM ever.']
        noun_prefix = ['The ', 'That ', 'Try doing something to the ']
        noun_post = [' is a thing in the world you are correct sir.',
                ' might be nearby but you need to perform something on it.',
                ' something imaginary.']
        index = random.randint(0,2)
        text = ''

        res = helpers.response_struct()
        if type_of == 'noun':
            text += noun_prefix[index] + word + noun_post[index]
        elif type_of == 'action':
            text += action_prefix[index] + word + action_post[index]
        res.description = text
        return res

    #------------------------------------------------------
    #This section for the write function so it checks for curses
    #these are the output and input handlers
    #------------------------------------------------------
    def reset_art(self):
        """
        if curses is being used reset's the art work
        """
        if USE_CURSES:
            game_ui.reset_art()
            for _ in range(0, self.number_of_turns):
                game_ui.write_art()

    def ui_refresh(self):
        """
        if curses refreshes all windows
        """
        if USE_CURSES: game_ui.refresh_all()
    def write_main_bottom_handler(self, msg):
        """
        checks if curses is available and writes to the last line of the main window
        otherwise sends to the multi_printer
        """
        if USE_CURSES: game_ui.write_main_bottom(msg)
        else: helpers.multi_printer(msg)

    def write_main_handler(self, msg, player_name=None, row=1, col=1):
        """
        checks if curses is available and sends the text to the main ouput screen
        otherwise send the msg to the multi_printer
        """
        if USE_CURSES: game_ui.write_main(msg, player_name, row, col)
        else: helpers.multi_printer(msg)

    def write_main_mid(self, msg):
        """
        write to the middle of the main screen
        """
        if USE_CURSES: game_ui.write_main_mid(msg)
        else: helpers.multi_printer(msg)

    def input_handler(self, msg=''):
        """
        prints the message to screen and returns the input received
        """
        if USE_CURSES: 
            text = game_ui.get_input(msg).lower()
        else: 
            text = raw_input('\n'+msg+'\n->').lower()
        if MIRROR_INPUT: 
            helpers.multi_printer(text)
        return text

    def write_time_handler(self, text):
        """
        delegates writing to the time window or to the multi_printer
        """
        if USE_CURSES: game_ui.write_time(text)
        else: helpers.multi_printer(text)

    def write_stat_handler(self, text):
        """
        delegates writing to the stat window or to the multi_printer
        """
        if USE_CURSES: game_ui.write_stat(text)
        else: helpers.multi_printer(text)

    def write_main_artifact_handler(self, content):
        """
        if curses sends to the artifact writer otherwise sends it to the multi_printer
        """
        if USE_CURSES: game_ui.write_main_artifact(content)
        else: helpers.multi_printer(content)

    def roll_credits_handler(self):
        if USE_CURSES: game_ui.roll_credits()
        else: helpers.roll_credits_basic()


    def validate_curses(self):
        """
        check throughout the game cycle if the terminal size is too small
        and if so end curses if it was running to begin with
        """
        global USE_CURSES
        if USE_CURSES and game_ui.terminal_size() == False:
            USE_CURSES = False
            game_ui.end_windows()
            helpers.multi_printer('TERMINAL WINDOW TOO SMALL. EXITING CURSES')

    #------------------------------------------------------
    #This ends the curses handlers section
    #------------------------------------------------------
    #------------------------------------------------------
    #This is a validator function to validate that we got back
    #a json object instead of none when loading a room or item
    #------------------------------------------------------

    def validate_object(self, obj, title):
        if not isinstance(obj, dict):
            if USE_CURSES: game_ui.end_windows()
            text = 'The file: ' + title + ', in the temp_save_game directory.'
            text += ' May be malformed and we cannot continue.'
            text += ' Exiting the game.'
            helpers.multi_printer(text)
            exit(1)


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
#Generates random input in gameCycle in hopes of causing a crash
def random_input_tester():
    #here are the possbile verbs that a user could input
    verbs =["look", "look at", "search", "go", "take ", "drop","use", "pull", "eat", "read" ]#"inventory", "help"]
    #here are the possbile nouns that a user could input
    nouns =[ "rescue whistle", "field", "medical kit", "cave", "candy bar", "flare gun", "heavy winter parka", "lantern", "old map",  "can of sweetened condensed milk", "notepad"]
    locations=["north", "south", "east", "west"]#"shore", "crash site", "camp", "woods", "waterfall", "river", "game trail", "dense brush", "field", "mountain base", "mountain path", "mountain summit", "fire tower", "rapids", "ranger station", "cave"]
    features = ["driftwood", "snow capped island", "dog sled","campfire pit", "blood stained snow", "bent pine", "small shelf", "wood pole", "tree stump", "bent pine" "small shelf", "tree stump", "bent pine", "hunting blind", "leanto", "animal corral", "deer carcass", "hay roll", "wolves", "sign", "clumps of bloody fur", "stone marker", "storage shed", "overlook", "locked safe", "look out", "cooler"]
    rand_verb = random.choice(verbs)
    '''
    if rand_verb == "look" or "look at" or "go"
        rand_loc = random.choice(locations)
        return (rand_verb + rand_loc)
    elif rand_verb== ""
    '''
    a=random.randrange(3)
    if a == 0:
        rand_noun = random.choice(nouns)
        input= rand_verb + " "+ rand_noun
    elif a == 1:
        rand_feat= random.choice(features)
        input= rand_verb + " " + rand_feat
    else:
        rand_loc = random.choice(locations)
        input= rand_verb + " " + rand_loc
    print input
    return input


#def testParse():
#    test_input = "go cave"
#    print "The test input is: " + test_input
#    print "The parsed command output is:"
#    print parse.parse_command(test_input)
#    print parse.parse_command(test_input)['room']['action']
#    print parse.parse_command(test_input)['room']['name']
#    print parse.parse_command(test_input)['other']['processed']
#    print parse.parse_command(test_input)['room']['action']
#    # parse.parse_command(test_input[0,0])
#    print ""
#

#random_input_tester()


def main():
    if USE_CURSES:
        curses.wrapper(game_ui.init_windows)
    else:
        text = [' ', 'Not using curses. ' +
                'Requires linux and '+str(helpers.MIN_COLS)+' columns' +
                ' by ' + str(helpers.MIN_ROWS) + ' rows.',' ']
        helpers.multi_printer(text)
    random.seed()
    current_game = Game()
    current_game.startGame(True)

if __name__ == "__main__":
    #pdb.set_trace() #toggle for debugging
    main()
