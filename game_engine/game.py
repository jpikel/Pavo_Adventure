from file_handler.file_lib import game_ops, load_room, store_room
import language_parser.command_parser as parse


class Game:

    def __init__(self, player, room):
        self.player = player
        self.current_room = room
        # Inventory will be a list of dicts, each element of which is an item.
        self.inventory = []
        self.current_time = 0
        self.number_of_turns = 0

    #-------------------------------------------------------------------------
    # Methods for managing game start, end, and basic flow
    #-------------------------------------------------------------------------
    def newGame(self):
        print "new Game"
        #gameO = game_ops()
        #gameO.new_game() #TODO: Add back in this functionality
        # New games start at the shore
        if self.current_room is not "shore":
            self.current_room = load_room("shore")
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

        while not choiceLow in cmds[0] and not choiceLow in cmds[1] and not choiceLow in cmds[2]:
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
        while not (self.player.rescued and self.player.dead):
            #print gO.get_room_desc()
            print "TODO: Add room description"
            self.number_of_turns += 1
            self.getTimeOfDay()
            self.updatePlayerCondition()
            self.player.getCondition()
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
            if output_type == "item_action":
                item = processed_command["item"]["name"]
                action = processed_command["item"]["action"]
                self.process_item_action(item, action)
            elif output_type == "action_only":
                action = processed_command["general"]["action"]
                self.process_action_only(action)
            elif output_type == "room_action":
                room = processed_command["room"]["name"]
                action = processed_command["room"]["action"]
                self.process_room_action(room, action)
            elif output_type == "exit":
                exit_direction = processed_command["exit"]["direction"]
                exit_name = processed_command["exit"]["exit"]
                self.process_exit(exit_direction, exit_name)
            elif output_type == "exit_only":
                exit_name = processed_command["exit"]["exit"]
                self.process_exit_only(exit_name)
            elif output_type == "item_only":
                item_name = processed_command["item"]["name"]
                self.process_item_only(item_name)
            elif output_type == "feature_action":
                feature = processed_command["feature"]["name"]
                action = processed_command["feature"]["action"]
                self.process_feature_action(feature, action)
            elif output_type == "feature_only":
                feature = processed_command["feature"]["name"]
                self.process_feature_only(feature)
            elif output_type == "room_only":
                room = processed_command["room"]["name"]
                self.process_room_only(room)
            else:
                "Error command type not supported yet."

    #-------------------------------------------------------------------------
    # Top-level methods for handling user commands.
    #-------------------------------------------------------------------------
    def process_item_action(self, item, action):
        print "TODO: Write this function"
        print "This is a stub function for handling item_action commands!"

    def process_action_only(self, action):
        if action == "eat":
            print "I don't understand what you want to eat. Say something like, 'Eat <item>'."
        elif action == "help":
            self.print_help()
        elif action == "inventory":
            self.print_inventory()
        elif action == "look":
            #TODO: WRITE THIS
            print "TEMP: The rest of this function still needs to be written..."
        elif action == "look at":
            print "I don't understand what you want to look at. Say something like, 'Look at <feature>'."
        elif action == "pull":
            print "I don't understand what you want to pull. Say something like 'Pull the <feature>'."
        elif action == "read":
            print "I don't understand what you want to read. Say something like 'Read <item>'."
        elif action == "search":
            #TODO: WRITE THIS
            print "TEMP: The rest of this function still needs to be written..."
        elif action == "take":
            print "I don't understand what you want to take. Say something like 'Take the <item>'."
        elif action == "use":
            print "I don't understand what you want to use. Say something like 'Use the <item>'."
        else:
            print "Hmm... I don't understand what you'd like to do."

    def process_room_action(self, room, action):
        if action  == "go":
            self.attempt_move(room)
        else:
            print "The rest of this function still needs to be written..."

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
        print "TODO: Write this function"
        print "This is a stub function for handling feature_action commands!"

    def process_feature_only(self, feature):
        print "TODO: Write this function"
        print "This is a stub function for handling feature only commands!"

    def process_room_only(self, room):
        print "TODO: Write this function"
        print "This is a stub function for handling room only commands!"

    #-------------------------------------------------------------------------
    # Helper methods that are used in processing user commands.
    #-------------------------------------------------------------------------
    def attempt_move(self, target_room):
        if target_room == self.current_room["title"]:
            print "You are already there!"
            return False
        rooms_connected_to_current = self.current_room["connected_rooms"]
        for connected_room in rooms_connected_to_current:
            if connected_room["title"] == target_room:
                self.current_room["visited"] = True
                store_room(self.current_room["title"], self.current_room)
                self.current_room = load_room(target_room)
                return True
        print "You cannot reach that location from here"
        return False

    def print_help(self):
        print "TODO: Write this function"
        print "This is a stub function for displaying help to the user!"

    def print_inventory(self):
        print "You have the following items in your inventory:"
        for item in self.inventory:
            print item["title"]

    #-------------------------------------------------------------------------
    # Methods that are used in otherwise managing game flow.
    #-------------------------------------------------------------------------
    def getTimeOfDay(self):
        if self.number_of_turns % 4 == 0:
            print"It is morning."
        elif self.number_of_turns % 4 == 1:
            print"It is afternoon."
        elif self.number_of_turns % 4 == 2:
            print"It is evening."
        elif self.number_of_turns % 4 == 3:
            print"It is night."

    def updatePlayerCondition(self):
        # Degrade the player's condition every three moves.
        if self.number_of_turns % 3 == 0:
            self.player.illness += 1
        if (self.player.illness > 50 or
            self.player.hunger > 50 or
            self.player.cold > 50):
            self.player.dead = True


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



