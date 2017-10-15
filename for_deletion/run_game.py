import json
import game_engine.game as game
import game_engine.player as player
from file_handler.file_lib import load_room

current_room = "shore"
current_player = player.Player("Test Player")
current_game = game.Game(current_player, load_room(current_room))

user_choice = current_game.startGame()