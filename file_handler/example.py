from file_lib import game_ops


game = game_ops()
#game.new_game()
if game.load_game():
    items = ["Boat Paddle"]
    #print(game.get_room_title())
    #print(game.get_room_desc())
    print(game.check_move("Cave", items))
    #print(game.get_room_title())
    #print(game.get_room_desc())
    print(game.check_move("W", items))
    print(game.get_room_items())
    print(game.lookat("Rescue Whistle", False))
    #print(game.get_room_title())
    #rint(game.get_room_desc())
    #not a connected place
    print(game.check_move("Ranger Station", items))
    #print(game.get_room_title())
    #print(game.get_room_desc())
    print(game.check_move("Game Trail", items))
    #print(game.get_room_title())
    #print(game.get_room_desc())
    print(game.get_room_items())
    print(game.use("Lantern", "use", True))
    print(game.use("Lantern", "use", True))
    print(game.use("pickaxe", "use", False))
    print(game.lookat("Lantern", True))
    print(game.lookat("feature_1_aliases", False))
    print(game.lookat("feature 2 aliases: Game Trail", False))
    print(game.lookat("Rescue Whistle", False))
    print(game.lookat("Dusty old map", False))
