import sys
sys.path.insert(0, "C:\\Users\\Alex\\Desktop\\capstone\\language_parser")
from file_handler.file_lib import game_ops
import language_parser.command_parser as parse
from player import Player


def getPlayerName(p=Player):
    print ("Hello dreary traveler.  What is your name? ")
    choice= raw_input("-> ")
    p.name = choice
    print "goodluck ", choice, "\n"
    return p


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
'''
def parseMoveRoom(tar, temp, g=Game):
    tar.lower()
    if tar.startswith("sh"):
        temp = g.shore
        g.cur_room = temp
    elif tar.startswith("cra"):
        temp = g.crash
        g.cur_room = temp
    elif tar.startswith("gam" or "trai"):
        temp = g.trai
        g.cur_room = temp
    elif tar.startswith("ca"):
        temp = g.cave
        g.cur_room = temp
    return temp
'''
#TODO build a initilizaion function for testing purposes
#def testInit():
def processInput(test_user_command_1):
    processed_user_command = parse.parse_command(test_user_command_1)
    processed = processed_user_command["other"]["processed"]
    if processed:
        output_type = processed_user_command["type"]
        if output_type == "item_action":
            item = processed_user_command["item"]["name"]
            action = processed_user_command["item"]["action"]
            #process_item_action(item, action)
        elif output_type == "action_only":
            action = processed_user_command["general"]["action"]
            #process_action_only(action)
        elif output_type == "room_action":
            room = processed_user_command["room"]["name"]
            action = processed_user_command["room"]["action"]
            #process_room_action(room, action)

        else:
            "Error command type not supported yet."
    else:
        print "I'm sorry. I didn't understand that command. Please enter a different command."


def playerRescued():
    print "congrats! you survived"


def playerDead():
    print"YOU DIED"

def exitGame():
    print "Thanks for playing"

