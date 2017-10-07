#from player import Player
#from room import Room


class Game:

    def __init__(self, player, room1, room2, room3, room4, room5, room6, room7, room8, room9, room10, room11, room12, room13, room14, room15, room16, tod):
        self.player = player
        self.room1 = room1
        self.room2 =  room2
        self.room3 = room3
        self.room4 = room4
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

    #cmds = ["new", "new game", "newgame", "load", "load game", "loadgame", "quit", "close", "exit"]
    newgame = ["new", "new game", "newgame"]
    loadgame = ["load", "load game", "loadgame"]
    quit = ["quit", "close", "exit" , "quit game", "close game", "exit game"]
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

def loadGame():
    print "load game"

def exitGame():
    print "Thanks for playing"

def playGame():
startGame()

