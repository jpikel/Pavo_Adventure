import game

import json
import os
import unittest
import sys

import file_handler.file_lib as files
import game_engine.engine_helpers as helpers
import game_engine.player as player
import language_parser.master_words as words
import language_parser.command_parser as parser

MASTER_WORDS_FILENAME = "master_words.py"
FEATURES_FILENAME = "feature_dict"
ITEMS_FILENAME = "items_dict"
ROOMS_FILENAME = "rooms_dict"
VERBS_FILENAME = "verbs_dict"

NUM_CARDINAL_DIRECTIONS = 4

class TestProcessCommands(unittest.TestCase):

    def setUp(self):
        self.game = game.Game()
        files.new_game()
        self.game.player = player.Player("Test Player")
        self.game.room.current_room = files.load_room("shore")
        self.game.validate_object(self.game.room.current_room, "shore")

    def test_process_action_only_runs(self):
        """
        Tests that the process_parsed_command method does not crash if the input
        command is any of the actions that the game recognizes.
        NOTE: This test does not check for the proper functioning of the
        process_parsed_command method beyond its ability to take the input
        without crashing.
        """
        # Get all the actions that the game should recognize.
        data_dir = os.path.abspath('data')
        verbs_full_path = os.path.join(data_dir, VERBS_FILENAME)
        with open(verbs_full_path, "r") as verbs_file:
            verbs_dict_str = verbs_file.read()
            verbs_dict = json.loads(verbs_dict_str)
        # Parse each action command, put the parsed results into the format
        # the game engine should expect, and run process_parsed_command.
        for action in verbs_dict:
            print "TESTING COMMAND: " + action
            processed_command = parser.parse_command(action)
            output_type = processed_command["type"]
            top_level = ["item", "room", "feature"]
            title = None
            action = None
            for word in top_level:
                if word in processed_command['command']:
                    title = processed_command['command'][word]
            if "action" in processed_command['command']:
                action = processed_command['command']['action']
            res = self.game.process_parsed_command(output_type, title, action)
            if res:
                self.game.post_process(res)

    def test_process_feature_only_runs(self):
        """
        Tests that the process_parsed_command method does not crash if the input
        command is any of the features that the game recognizes.
        NOTE: This test does not check for the proper functioning of the
        process_parsed_command method beyond its ability to take the input
        without crashing.
        """
        # Get all the features that the game should recognize.
        data_dir = os.path.abspath('data')
        features_full_path = os.path.join(data_dir, FEATURES_FILENAME)
        with open(features_full_path, "r") as features_file:
            features_dict_str = features_file.read()
            features_dict = json.loads(features_dict_str)
        # Parse each feature command, put the parsed results into the format
        # the game engine should expect, and run process_parsed_command().
        for feature in features_dict:
            print "TESTING COMMAND: " + feature
            processed_command = parser.parse_command(feature)
            output_type = processed_command["type"]
            title = None
            action = None
            top_level = ["item", "room", "feature"]
            for word in top_level:
                if word in processed_command['command']:
                    title = processed_command['command'][word]
            if "action" in processed_command['command']:
                action = processed_command['command']['action']
            res = self.game.process_parsed_command(output_type, title, action)
            if res:
                self.game.post_process(res)

    def test_process_item_only_runs(self):
        """
        Tests that the process_parsed_command method does not crash if the input
        command is any of the items that the game recognizes.
        NOTE: This test does not check for the proper functioning of the
        process_parsed_command method beyond its ability to take the input
        without crashing.
        """
        # Get all the items that the game should recognize.
        data_dir = os.path.abspath('data')
        items_full_path = os.path.join(data_dir, ITEMS_FILENAME)
        with open(items_full_path, "r") as items_file:
            items_dict_str = items_file.read()
            items_dict = json.loads(items_dict_str)
        # Parse each item command, put the parsed results into the format
        # the game engine should expect, and run process_item_only().
        for item in items_dict:
            print "TESTING COMMAND: " + item
            processed_command = parser.parse_command(item)
            output_type = processed_command["type"]
            title = None
            action = None
            top_level = ["item", "room", "feature"]
            for word in top_level:
                if word in processed_command['command']:
                    title = processed_command['command'][word]
            if "action" in processed_command['command']:
                action = processed_command['command']['action']
            res = self.game.process_parsed_command(output_type, title, action)
            if res:
                self.game.post_process(res)

    def test_process_room_only_runs(self):
        """
        Tests that the pprocess_parsed_command method does not crash if the input
        command is any of the rooms that the game recognizes (or a cardinal
        direction).
        NOTE: This test does not check for the proper functioning of the
        process_parsed_command method beyond its ability to take the input
        without crashing.
        """
        # Get all the rooms that the game should recognize.
        data_dir = os.path.abspath('data')
        rooms_full_path = os.path.join(data_dir, ROOMS_FILENAME)
        with open(rooms_full_path, "r") as rooms_file:
            rooms_dict_str = rooms_file.read()
            rooms_dict = json.loads(rooms_dict_str)
        # Add the cardinal directions to the rooms dict
        rooms_dict["north"] = "north"
        rooms_dict["east"] = "east"
        rooms_dict["south"] = "south"
        rooms_dict["west"] = "west"
        for room in rooms_dict:
            print "TESTING COMMAND: " + room
            processed_command = parser.parse_command(room)
            output_type = processed_command["type"]
            title = None
            action = None
            top_level = ["item", "room", "feature"]
            for word in top_level:
                if word in processed_command['command']:
                    title = processed_command['command'][word]
            if "action" in processed_command['command']:
                action = processed_command['command']['action']
            res = self.game.process_parsed_command(output_type, title, action)
            if res:
                self.game.post_process(res)

    def test_process_feature_action_runs(self):
        """
        Tests that the process_parsed_command method does not crash if the input
        command is any combination of an action and a feature that the game
        recognizes, separated by a space.
        NOTE: This test does not check for the proper functioning of the
        process_parsed_command method beyond its ability to take the input
        without crashing.
        """
         # Get all the actions that the game should recognize.
        data_dir = os.path.abspath('data')
        verbs_full_path = os.path.join(data_dir, VERBS_FILENAME)
        with open(verbs_full_path, "r") as verbs_file:
            verbs_dict_str = verbs_file.read()
            verbs_dict = json.loads(verbs_dict_str)
        # Get all the features that the game should recognize.
        data_dir = os.path.abspath('data')
        features_full_path = os.path.join(data_dir, FEATURES_FILENAME)
        with open(features_full_path, "r") as features_file:
            features_dict_str = features_file.read()
            features_dict = json.loads(features_dict_str)
        for action in verbs_dict:
            for feature in features_dict:
                combined_command = action + ' ' + feature
                print "TESTING COMMAND: " + combined_command
                processed_command = parser.parse_command(combined_command)
                output_type = processed_command["type"]
                title = None
                action = None
                top_level = ["item", "room", "feature"]
                for word in top_level:
                    if word in processed_command['command']:
                        title = processed_command['command'][word]
                if "action" in processed_command['command']:
                    action = processed_command['command']['action']
                res = self.game.process_parsed_command(output_type, title, action)
                if res:
                    self.game.post_process(res)

    def test_process_item_action_runs(self):
        """
        Tests that the process_parsed_command method does not crash if the input
        command is any combination of an action and an item that the game
        recognizes, separated by a space.
        NOTE: This test does not check for the proper functioning of the
        process_parsed_command method beyond its ability to take the input
        without crashing.
        """
         # Get all the actions that the game should recognize.
        data_dir = os.path.abspath('data')
        verbs_full_path = os.path.join(data_dir, VERBS_FILENAME)
        with open(verbs_full_path, "r") as verbs_file:
            verbs_dict_str = verbs_file.read()
            verbs_dict = json.loads(verbs_dict_str)
        # Get all the features that the game should recognize.
        data_dir = os.path.abspath('data')
        items_full_path = os.path.join(data_dir, ITEMS_FILENAME)
        with open(items_full_path, "r") as items_file:
            items_dict_str = items_file.read()
            items_dict = json.loads(items_dict_str)
        for action in verbs_dict:
            for item in items_dict:
                combined_command = action + ' ' + item
                print "TESTING COMMAND: " + combined_command
                processed_command = parser.parse_command(combined_command)
                output_type = processed_command["type"]
                title = None
                action = None
                top_level = ["item", "room", "feature"]
                for word in top_level:
                    if word in processed_command['command']:
                        title = processed_command['command'][word]
                if "action" in processed_command['command']:
                    action = processed_command['command']['action']
                res = self.game.process_parsed_command(output_type, title, action)
                if res:
                    self.game.post_process(res)

    def test_process_room_action_runs(self):
        """
        Tests that the process_parsed_command method does not crash if the input
        command is any combination of an action and a room that the game
        recognizes (or a cardinal direction), separated by a space.
        NOTE: This test does not check for the proper functioning of the
        process_parsed_command method beyond its ability to take the input
        without crashing.
        """
         # Get all the actions that the game should recognize.
        data_dir = os.path.abspath('data')
        verbs_full_path = os.path.join(data_dir, VERBS_FILENAME)
        with open(verbs_full_path, "r") as verbs_file:
            verbs_dict_str = verbs_file.read()
            verbs_dict = json.loads(verbs_dict_str)
        # Get all the rooms that the game should recognize.
        data_dir = os.path.abspath('data')
        rooms_full_path = os.path.join(data_dir, ROOMS_FILENAME)
        with open(rooms_full_path, "r") as rooms_file:
            rooms_dict_str = rooms_file.read()
            rooms_dict = json.loads(rooms_dict_str)
        # Add the cardinal directions to the rooms dict
        rooms_dict["north"] = "north"
        rooms_dict["east"] = "east"
        rooms_dict["south"] = "south"
        rooms_dict["west"] = "west"
        for action in verbs_dict:
            for room in rooms_dict:
                combined_command = action + ' ' + room
                print "TESTING COMMAND: " + combined_command
                processed_command = parser.parse_command(combined_command)
                output_type = processed_command["type"]
                title = None
                action = None
                top_level = ["item", "room", "feature"]
                for word in top_level:
                    if word in processed_command['command']:
                        title = processed_command['command'][word]
                if "action" in processed_command['command']:
                    action = processed_command['command']['action']
                res = self.game.process_parsed_command(output_type, title, action)
                if res:
                    self.game.post_process(res)

class TestParser(unittest.TestCase):

    def test_master_words_features(self):
        data_dir = os.path.abspath('data')
        features_full_path = os.path.join(data_dir, FEATURES_FILENAME)
        with open(features_full_path, "r") as features_file:
            features_dict_str = features_file.read()
            features_dict = json.loads(features_dict_str)
        # Check that the original feature file dict and the 'features' dict in
        # master_words.py are of the same length
        self.assertEqual(len(words.features), len(features_dict))
        # Check that every word in the original feature file dict is in the
        # 'features' dict in master_words.py (in lower-case form).
        for key in features_dict:
            key_lower = key.lower()
            value = words.features.get(key_lower, None)
            self.assertNotEqual(value, None)

    def test_master_words_items(self):
        data_dir = os.path.abspath('data')
        items_full_path = os.path.join(data_dir, ITEMS_FILENAME)
        with open(items_full_path, "r") as items_file:
            items_dict_str = items_file.read()
            items_dict = json.loads(items_dict_str)
        # Check that the original items file dict and the 'items' dict in
        # master_words.py are of the same length
        self.assertEqual(len(words.items), len(items_dict))
        # Check that every word in the original items file dict is in the
        # 'items' dict in master_words.py (in lower-case form).
        for key in items_dict:
            key_lower = key.lower()
            value = words.items.get(key_lower, None)
            self.assertNotEqual(value, None)

    def test_master_words_rooms(self):
        data_dir = os.path.abspath('data')
        rooms_full_path = os.path.join(data_dir, ROOMS_FILENAME)
        with open(rooms_full_path, "r") as rooms_file:
            rooms_dict_str = rooms_file.read()
            rooms_dict = json.loads(rooms_dict_str)
        # Check that the original rooms file dict is 4 items smaller than the
        # 'rooms' dict in master_words.py (the 4 cardinal directions are added
        # to the rooms dict in master_words.py).
        self.assertEqual(len(words.rooms),
            len(rooms_dict) + NUM_CARDINAL_DIRECTIONS)
        # Check that every word in the original rooms file dict is in the
        # 'rooms' dict in master_words.py (in lower-case form).
        for key in rooms_dict:
            key_lower = key.lower()
            value = words.rooms.get(key_lower, None)
            self.assertNotEqual(value, None)

    def test_master_words_verbs(self):
        data_dir = os.path.abspath('data')
        verbs_full_path = os.path.join(data_dir, VERBS_FILENAME)
        with open(verbs_full_path, "r") as verbs_file:
            verbs_dict_str = verbs_file.read()
            verbs_dict = json.loads(verbs_dict_str)
        # Check that the original verbs file dict is the same size as the
        # 'verbs' dict in master_words.py.
        self.assertEqual(
            len(words.actions),
            len(verbs_dict)
        )
        # Check that every word in the original verbs file dict is in the
        # 'verbs' dict in master_words.py (in lower-case form).
        for key in verbs_dict:
            key_lower = key.lower()
            value = words.actions.get(key_lower, None)
            self.assertNotEqual(value, None)

    def test_parse_action_only(self):
        input_1 = "move"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "action_only",
            "command": {"action": "go"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "eat"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "action_only",
            "command": {"action": "eat"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_parse_feature_action(self):
        input_1 = "look at the leanto"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "feature_action",
            "command": {"action": "look at", "feature": "leanto"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "search safe"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "feature_action",
            "command": {"action": "search", "feature": "locked safe"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_parse_feature_only(self):
        input_1 = "deer"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "feature_only",
            "command": {"feature": "deer carcass"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "island"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "feature_only",
            "command": {"feature": "snow capped island"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_parse_item_action(self):
        input_1 = "search the medical kit"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "item_action",
            "command": {"item": "medical kit", "action": "search"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "eat a candy bar"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "item_action",
            "command": {"item": "candy bar", "action": "eat"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_parse_item_only(self):
        input_1 = "lantern"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "item_only",
            "command": {"item": "lantern"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "map"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "item_only",
            "command": {"item": "old map"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_room_action(self):
        input_1 = "search the mountain summit"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "room_action",
            "command": {"room": "mountain summit", "action": "search"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "look at the stream"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "room_action",
            "command": {"room": "river", "action": "look at"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_room_only(self):
        input_1 = "South"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "room_only",
            "command": {"room": "south"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "Game trail!"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "room_only",
            "command": {"room": "game trail"},
            "processed": True
        }
    #     self.assertEqual(output_2, expected_output_2)

    def test_parse_unknown(self):
        input_1 = "Nothing to see here!"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "other",
            "processed": False

        }
        self.assertEqual(output_1, expected_output_1)
        input_2 = "This isn't something that we should match on..."
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "other",
            "processed": False
        }
        self.assertEqual(output_2, expected_output_2)

if __name__ == '__main__':
    unittest.main()



# Resources used in writing this code:
# https://docs.python.org/2/library/unittest.html
# https://www.tutorialspoint.com/python/dictionary_get.htm
# https://stackoverflow.com/questions/1911273/is-there-a-better-way-to-compare-dictionary-values/5635309#5635309
# https://stackoverflow.com/questions/8930915/append-dictionary-to-a-dictionary

    def test_get_humor_item_feature(self):
        """
        Tests that the get_humor() method works for any item or feature
        that the game recognizes.
        """
        # Get all the features that the game should recognize.
        data_dir = os.path.abspath('data')
        features_full_path = os.path.join(data_dir, FEATURES_FILENAME)
        items_full_path = os.path.join(data_dir, ITEMS_FILENAME)
        # Get all the features and items that the game should recognize.
        with open(features_full_path, "r") as features_file:
            features_dict_str = features_file.read()
            features_dict = json.loads(features_dict_str)
        with open(items_full_path, "r") as items_file:
            items_dict_str = items_file.read()
            items_dict = json.loads(items_dict_str)
        # Put all recognized actions, features, and items into one dict
        all_items_features = {}
        all_items_features.update(features_dict)
        all_items_features.update(items_dict)
        # Parse each command, put the parsed results into the format
        # the game engine should expect, and run get_humor(title, 'noun').
        for command in all_items_features:
            print "TESTING COMMAND: " + command
            processed_command = parser.parse_command(command)
            output_type = processed_command["type"]
            top_level = ["item", "room", "feature"]
            for word in top_level:
                if word in processed_command['command']:
                    title = processed_command['command'][word]
            if "action" in processed_command['command']:
                action = processed_command['command']['action']
            if output_type == "feature_only" or output_type == "item_only":
                res = self.game.get_humor(title, 'noun')
                if res:
                    self.game.post_process(res)
            else:
                # If the output type is not recognized as 'feature_only' or
                # 'item_only', run invalid code that will cause the function
                # call to fail.
                crash_here

    def test_process_room_action(self):
        """
        Tests that the room_action method does not crash if the input
        command is any combination of an action and a room that the game
        recognizes (or a cardinal direction), separated by a space.
        NOTE: This test does not check for the proper functioning of the
        room_action method beyond its ability to take the input
        without crashing.
        """
         # Get all the actions that the game should recognize.
        data_dir = os.path.abspath('data')
        verbs_full_path = os.path.join(data_dir, VERBS_FILENAME)
        with open(verbs_full_path, "r") as verbs_file:
            verbs_dict_str = verbs_file.read()
            verbs_dict = json.loads(verbs_dict_str)
        # Get all the rooms that the game should recognize.
        data_dir = os.path.abspath('data')
        rooms_full_path = os.path.join(data_dir, ROOMS_FILENAME)
        with open(rooms_full_path, "r") as rooms_file:
            rooms_dict_str = rooms_file.read()
            rooms_dict = json.loads(rooms_dict_str)
        # Add the cardinal directions to the rooms dict
        rooms_dict["north"] = "north"
        rooms_dict["east"] = "east"
        rooms_dict["south"] = "south"
        rooms_dict["west"] = "west"
        for action in verbs_dict:
            for room in rooms_dict:
                combined_command = action + ' ' + room
                print "TESTING COMMAND: " + combined_command
                processed_command = parser.parse_command(combined_command)
                output_type = processed_command["type"]
                top_level = ["item", "room", "feature"]
                for word in top_level:
                    if word in processed_command['command']:
                        title = processed_command['command'][word]
                if "action" in processed_command['command']:
                    action = processed_command['command']['action']
                if output_type == "room_action":
                    res = self.game.room_action(title, action)
                    if res:
                        self.game.post_process(res)
                else:
                    # If the output type is not recognized as 'item_only', run
                    # invalid code that will cause the function call to fail.
                    crash_here


class TestParser(unittest.TestCase):

    def test_master_words_features(self):
        data_dir = os.path.abspath('data')
        features_full_path = os.path.join(data_dir, FEATURES_FILENAME)
        with open(features_full_path, "r") as features_file:
            features_dict_str = features_file.read()
            features_dict = json.loads(features_dict_str)
        # Check that the original feature file dict and the 'features' dict in
        # master_words.py are of the same length
        self.assertEqual(len(words.features), len(features_dict))
        # Check that every word in the original feature file dict is in the
        # 'features' dict in master_words.py (in lower-case form).
        for key in features_dict:
            key_lower = key.lower()
            value = words.features.get(key_lower, None)
            self.assertNotEqual(value, None)

    def test_master_words_items(self):
        data_dir = os.path.abspath('data')
        items_full_path = os.path.join(data_dir, ITEMS_FILENAME)
        with open(items_full_path, "r") as items_file:
            items_dict_str = items_file.read()
            items_dict = json.loads(items_dict_str)
        # Check that the original items file dict and the 'items' dict in
        # master_words.py are of the same length
        self.assertEqual(len(words.items), len(items_dict))
        # Check that every word in the original items file dict is in the
        # 'items' dict in master_words.py (in lower-case form).
        for key in items_dict:
            key_lower = key.lower()
            value = words.items.get(key_lower, None)
            self.assertNotEqual(value, None)

    def test_master_words_rooms(self):
        data_dir = os.path.abspath('data')
        rooms_full_path = os.path.join(data_dir, ROOMS_FILENAME)
        with open(rooms_full_path, "r") as rooms_file:
            rooms_dict_str = rooms_file.read()
            rooms_dict = json.loads(rooms_dict_str)
        # Check that the original rooms file dict is 4 items smaller than the
        # 'rooms' dict in master_words.py (the 4 cardinal directions are added
        # to the rooms dict in master_words.py).
        self.assertEqual(len(words.rooms),
            len(rooms_dict) + NUM_CARDINAL_DIRECTIONS)
        # Check that every word in the original rooms file dict is in the
        # 'rooms' dict in master_words.py (in lower-case form).
        for key in rooms_dict:
            key_lower = key.lower()
            value = words.rooms.get(key_lower, None)
            self.assertNotEqual(value, None)

    def test_master_words_verbs(self):
        data_dir = os.path.abspath('data')
        verbs_full_path = os.path.join(data_dir, VERBS_FILENAME)
        with open(verbs_full_path, "r") as verbs_file:
            verbs_dict_str = verbs_file.read()
            verbs_dict = json.loads(verbs_dict_str)
        # Check that the original verbs file dict is the same size as the
        # 'verbs' dict in master_words.py.
        self.assertEqual(
            len(words.actions),
            len(verbs_dict)
        )
        # Check that every word in the original verbs file dict is in the
        # 'verbs' dict in master_words.py (in lower-case form).
        for key in verbs_dict:
            key_lower = key.lower()
            value = words.actions.get(key_lower, None)
            self.assertNotEqual(value, None)

    def test_parse_action_only(self):
        input_1 = "move"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "action_only",
            "command": {"action": "go"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "eat"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "action_only",
            "command": {"action": "eat"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_parse_feature_action(self):
        input_1 = "look at the leanto"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "feature_action",
            "command": {"action": "look at", "feature": "leanto"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "search safe"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "feature_action",
            "command": {"action": "search", "feature": "locked safe"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_parse_feature_only(self):
        input_1 = "deer"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "feature_only",
            "command": {"feature": "deer carcass"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "island"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "feature_only",
            "command": {"feature": "snow capped island"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_parse_item_action(self):
        input_1 = "search the medical kit"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "item_action",
            "command": {"item": "medical kit", "action": "search"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "eat a candy bar"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "item_action",
            "command": {"item": "candy bar", "action": "eat"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_parse_item_only(self):
        input_1 = "lantern"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "item_only",
            "command": {"item": "lantern"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "map"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "item_only",
            "command": {"item": "old map"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_room_action(self):
        input_1 = "search the mountain summit"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "room_action",
            "command": {"room": "mountain summit", "action": "search"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "look at the stream"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "room_action",
            "command": {"room": "river", "action": "look at"},
            "processed": True
        }
        self.assertEqual(output_2, expected_output_2)

    def test_room_only(self):
        input_1 = "South"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "room_only",
            "command": {"room": "south"},
            "processed": True
        }
        self.assertEqual(output_1, expected_output_1)

        input_2 = "Game trail!"
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "room_only",
            "command": {"room": "game trail"},
            "processed": True
        }
    #     self.assertEqual(output_2, expected_output_2)

    def test_parse_unknown(self):
        input_1 = "Nothing to see here!"
        output_1 = parser.parse_command(input_1)
        expected_output_1 = {
            "type": "other",
            "processed": False

        }
        self.assertEqual(output_1, expected_output_1)
        input_2 = "This isn't something that we should match on..."
        output_2 = parser.parse_command(input_2)
        expected_output_2 = {
            "type": "other",
            "processed": False
        }
        self.assertEqual(output_2, expected_output_2)

if __name__ == '__main__':
    unittest.main()



# Resources used in writing this code:
# https://docs.python.org/2/library/unittest.html
# https://www.tutorialspoint.com/python/dictionary_get.htm
# https://stackoverflow.com/questions/1911273/is-there-a-better-way-to-compare-dictionary-values/5635309#5635309
# https://stackoverflow.com/questions/8930915/append-dictionary-to-a-dictionary