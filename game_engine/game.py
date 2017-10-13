import os, sys, inspect
from helpers import *
from player import Player
from room import *
from item import Item
sys.path.insert(0, "C:\\Users\\Alex\\Desktop\\capstone\\file_handler")  #https://askubuntu.com/questions/470982/how-to-add-a-python-module-to-syspath
sys.path.insert(0, "C:\\Users\\Alex\\Desktop\\capstone\\language_parser")
from file_handler.file_lib import game_ops
import language_parser.command_parser as parse



class Game:

    items = [Item(1, "boat Paddle", "row", "use")]
    shore = Room("shore", items[0], "its a beach", "a beach", True, 1)
    crash = Room("crash site", None, "its a crash!", "a crash", False, 2)
    trail = Room("game trail", None, "its a trail", "a trail", False, 2)
    cave = Room("cave", None, "its a cave", "a cave", False, 2)
    person = Player(None, shore, items, "well", "thirsty")
    ri = room_info()
    room_titles = ["shore", "crash site", "game trail", "field", "dense brush", "camp", "woods",
                   "cave", "mountain base", "fire tower", "river", "waterfall", "mountain ascent",
                   "mountain summit", "rapids", "ranger station"]
    room_connections = [1, 3, 2, 2, 2, 3, 3, 2, 2, 1, 3, 1, 2, 2, 2, 1]

    cur_room = Room(None, None, None, None, None, None)

    #def __init__(self, player, room1, room2, room3, room4, room5, room6, room7, room8, room9, room10, room11, room12, room13, room14, room15, room16, tod):
    def __init__(self, player, room1, room2, room3, room4, tod):
        self.player = player
        self.room1 = room1
        self.room2 = room2
        self.room3 = room3
        self.room4 = room4
        '''
        self.room5 = room5
        self.room6 = room6
        self.room7 = room7
        self.room8 = room8
        self.room9 = room9
        self.room10 = room10
        self.room11 = room11
        self.room12 = room12
        self.room13 = room13
        self.room14 = room14
        self.room15 = room15
        self.room16 = room16
        self.map = map  #list of connecting rooms
        '''
        self.tod = tod  #time of day



def startGame():

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
        newGame()

    elif choiceLow in cmds[1]:
        loadGame()

    else:
        exitGame()


def newGame():
    print "new Game"
    #little bit of manual testing of local structures
    gameO = game_ops()
    gameO.new_game()
    items = [Item(1, "boat Paddle", "row", "use")]
    shore = Room("shore", items[0], "its a beach", "a beach", True, 1)
    crash = Room("crash site", None, "its a crash!", "a crash", False, 2)
    trail = Room("game trail", None, "its a trail", "a trail", False, 2)
    cave = Room("cave", None, "its a cave", "a cave", False, 2)
    person = Player(None, shore, items, "well", "thirsty")
    getPlayerName(person)
    game =Game(Player, shore, crash, trail, cave, "night")
    game.cur_room = shore
    gameCycle(game, gameO)
    '''
    game.cur_room = person.getLocation()
    print "description"
    print "Current Location: ",person.getLocation()
    print (gameO.get_room_desc())
    print "Moving to crash site"
    print "description"
    print "Inventory: ", person.inventory[0].title
    person.location = crash
    print "Current Location: ", person.getLocation()
    gameO.attempt_move("crash site", items)
    print (gameO.get_room_desc())
    #gameO.get_room_title()
    '''

def loadGame():
    print "load game"
    gO = game_ops()

    if gO.load_game():
       #here we need to load in all the saved data to engine
       g = Game(None, None, None, None, None, "night")
       gameCycle(g,gO)

    return

def exitGame():
    print "Thanks for playing"

def playGame():
    print "play Game"

def testNew():
    g = game_ops()
    g.new_game()
    print g.get_room_title()

def gameCycle(g=Game, gO=game_ops):

    while (g.person.isRescued == False and g.person.condition != "dead"):
        print gO.get_room_desc()
        #getInput(action, noun)

        print "What would you like to do?"
        userInput = raw_input("->")
        parse.parse_command(userInput)
        while parse.parse_command(userInput)['other']['processed'] == False:
            print "sorry I did not understand"
            print "What would you like to do?"
            userInput = raw_input("->")
            parse.parse_command(userInput)

        if parse.parse_command(userInput)['room']['action']  == "go":
            noun =parse.parse_command(userInput)['room']['name']
            move(noun, g,gO)



        #g.person.isRescued = True

def move(tar, g = Game, gO=game_ops):
    startRoom = g.cur_room
    stemp=""
    temp = g.cur_room
    stemp = parseMoveString(tar, stemp)
    temp = parseMoveRoom(tar, temp, g)
    moveP(startRoom, temp, g)
    gO.attempt_move(stemp,g.person.inventory)
    g.cur_room.visited = True
    print "Player Location", g.person.location.title
    print "current room", g.cur_room.title
    print "game ops room", gO.get_room_title()


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

def parseMoveString(tar, stemp):
    tar.lower()
    if tar.startswith("sh"):
        stemp = "shore"
    elif tar.startswith("cra"):
        stemp = "crash site"
    elif tar.startswith("gam" or "trai"):
        stemp = "game trail"
    elif tar.startswith("ca"):
        stemp = "cave"
    return stemp

def parseMoveRoom(tar, temp, g=Game):
    tar.lower()
    if tar.startswith("sh"):
        temp = g.shore
        g.cur_room = temp
    elif tar.startswith("cra"):
        temp = g.crash
        g.cur_room = temp
    elif tar.startswith("gam" or "trai"):
        temp = g.trail
        g.cur_room = temp
    elif tar.startswith("ca"):
        temp = g.cave
        g.cur_room = temp
    return temp

def moveP( cur= Room, tar=Room, g=Game):
        con = g.ri.isConnected(cur.title, tar.title)
        if con:
            g.person.location = tar
            g.cur_room = tar
        else:
            print "You cannot reach that location from here"
            g.person.location = cur
            g.cur_room = cur

#testParse()
startGame()
#loadGame()
#newGame()
#playerDead()
#testNew()
#print(sys.path)



