import game

import json
import os
import unittest
import sys
import filecmp
import random
import shutil

import file_handler.name_lists as name_lists
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
        self.game_file = game
        self.game_file.USE_CURSES = False
        self.game = self.game_file.Game()
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

        input_3 = "search campfire"
        output_3 = parser.parse_command(input_3)
        expected_output_3 = {
            "type": "feature_action",
            "command": {"action": "search", "feature": "campfire pit"},
            "processed": True
        }
        self.assertEqual(output_3, expected_output_3)

        input_4 = "look at snow-capped island"
        output_4 = parser.parse_command(input_4)
        expected_output_4 = {
            "type": "feature_action",
            "command": {"action": "look at", "feature": "snow capped island"},
            "processed": True
        }
        self.assertEqual(output_4, expected_output_4)

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

class TestPlayerClass(unittest.TestCase):
    def setUp(self):
        files.new_game()
        self.player = player.Player("Bob")
        print ""

    def tearDown(self):
        self.player = None

    def test_Name(self):
        print "TEST getName property:",
        print self.assertEqual(self.player.getName, "Bob")

    def test_Set_Stats(self):
        old_states = {
                "cold":self.player.cold,
                "hunger":self.player.hunger,
                "illness":self.player.illness,
                "name":self.player.getName,
                "rescued":self.player.rescued,
                "dead":self.player.dead,
                "inventory":self.player.get_inventory
                }

        new_states = {
                "cold":99,
                "hunger":99,
                "illness":99,
                "name":"notBob",
                "rescued":True,
                "dead":True,
                "inventory":["1"]
                }
        print "TEST current state not new state",
        print self.assertNotEqual(old_states, new_states)
        update_player = self.player.set_player_stats(new_states)
        update_states = {
                "cold":update_player.cold,
                "hunger":update_player.hunger,
                "illness":update_player.illness,
                "name":update_player.getName,
                "rescued":update_player.rescued,
                "dead":update_player.dead,
                "inventory":update_player.inventory
                }
        print "TEST old state not update state",
        print self.assertNotEqual(old_states, update_states)
        print "TEST new_state is equal to update state",
        print self.assertEqual(new_states, update_states)

    def test_item_action_inventory(self):
        VERBOSE = 0
        print ""
        print "TEST items in inventory against verbs"
        NOT_ABLE = 'You are not able to '
        NOT_SECURE = 'There is no where secure to drop the item.'
        verbs = name_lists.verb_info().get_verbs()
        KEY_ERROR_VERBS = ['look', 'go', 'help', 'inventory']
        items = getItems()
        self.player.inventory = items
        #test each item with all verbs

        for item in items:
            for verb in verbs:
                print verb + ' ' + item['title']
                res = self.player.item_action_inventory(item['title'], verb, True)
                if VERBOSE:
                    print res.description
                if verb not in KEY_ERROR_VERBS:
                    self.assertEqual(res.description, item['verbs'][verb]['description'])
                    if verb != 'use':
                        self.assertEqual(res.modifiers, item['verbs'][verb]['modifiers'])
                else:
                    self.assertEqual(res.description,NOT_ABLE+verb+' '+item['title']+'.')
        #try to drop each item in a non searched room
        for item in items:
            res = self.player.item_action_inventory(item['title'], 'drop', False)
            self.assertEqual(res.description,NOT_SECURE)
            self.assertEqual(res.modifiers, {})

    def test_use_items(self):
        #reset the items
        #use each item to see if we can activate it and get the correct response
        #and that it has been switched to active in the player inventory
        items = getItems()
        self.player.inventory = getItems()
        for item in items:
            print 'use ' + item['title']
            res = self.player.item_action_inventory(item['title'], 'use', False)
            if item['activatable']:
                player_item = self.player.search_inventory(item['title'])
                self.assertEqual(player_item['active'], True)
                self.assertEqual(res.description, item['verbs']['use']['description'])
                if 'act_mods' in item['verbs']['use']:
                    self.assertEqual(res.modifiers, item['verbs']['use']['act_mods'])
            else:
                self.assertEqual(res.description, item['verbs']['use']['description'])
                self.assertEqual(res.modifiers, item['verbs']['use']['modifiers'])

        for item in items:
            print 'use ' + item['title']
            res = self.player.item_action_inventory(item['title'], 'use', False)
            if item['activatable']:
                player_item = self.player.search_inventory(item['title'])
                self.assertEqual(player_item['active'], False)
                self.assertEqual(res.description, item['verbs']['use']['deactivate_description'])
                if 'de_mods' in item['verbs']['use']:
                    self.assertEqual(res.modifiers, item['verbs']['use']['de_mods'])
            else:
                self.assertEqual(res.description, item['verbs']['use']['description'])
                self.assertEqual(res.modifiers, item['verbs']['use']['modifiers'])

    def test_inventory(self):
        print 'testing inventory functions'
        self.player.inventory = getItems()
        item_titles = name_lists.item_info().get_titles()
        titles = self.player.get_items_inventory_titles()
        self.assertEqual(item_titles, titles)

        for title in item_titles:
            print 'searching for ' + title + ' in inventory'
            item = self.player.search_inventory(title)
            self.assertEqual(title, item['title'])

        for title in item_titles:
            print 'removing ' + title + ' from inventory'
            self.player.remove_item_from_inventory(title)
            item = self.player.search_inventory(title)
            self.assertEqual(item, None)



class TestFileLib(unittest.TestCase):
    def setUp(self):
        self.player = player.Player("Bob")
        files.clean_dir(name_lists.save_info().get_temp_save_dir_rooms())
        files.clean_dir(name_lists.save_info().get_temp_save_dir_items())

    def test_new_game(self):
        IGNORE = files.IGNORE
        rooms_dir = os.path.abspath('data/rooms')
        items_dir = os.path.abspath('data/items')
        room_files = os.listdir(rooms_dir)
        item_files = os.listdir(items_dir)
        result = files.new_game()
        new_rooms_dir = name_lists.save_info().get_temp_save_dir_rooms()
        new_items_dir = name_lists.save_info().get_temp_save_dir_items()
        new_room_files = os.listdir(new_rooms_dir)
        new_item_files = os.listdir(new_items_dir)
        print ""
        print "TEST that files were transferred"
        self.assertEqual(result, True)
        for file_ in new_room_files:
            print "File: " + file_ + " in temp save is in template"
            self.assertIn(file_, room_files)
        for file_ in room_files:
            if file_ not in IGNORE:
                print "File: " + file_ + " in temp save is in temp save"
                self.assertIn(file_, new_room_files)
        for file_ in new_item_files:
            print "File: " + file_ + " in temp save is in template"
            self.assertIn(file_, item_files)
        for file_ in item_files:
            if file_ not in IGNORE:
                print "File: " + file_ + " in temp save is in temp save"
                self.assertIn(file_, new_item_files)

        print "TEST compare the room files in both dirs to check that they match"
        match, mismatch, errors = filecmp.cmpfiles(rooms_dir, new_rooms_dir, room_files)
        for name in match:
            self.assertIn(name, room_files)
            self.assertIn(name, new_room_files)
        for name in mismatch:
            self.assertIn(name, IGNORE)

        self.assertEqual(len(mismatch), 0)
        print "TEST compare the item files in both dirs to check that they match"
        match, mismatch, errors = filecmp.cmpfiles(items_dir, new_items_dir, item_files)
        for name in match:
            self.assertIn(name, item_files)
            self.assertIn(name, new_item_files)
        for name in mismatch:
            self.assertIn(name, IGNORE)

        self.assertEqual(len(mismatch), 0)

    def test_save_game(self):
        print ""
        print "TEST the save game of file_lib"
        files.new_game()
        rooms = name_lists.room_info().get_titles()
        items = name_lists.item_info().get_titles()
        title = random.choice(rooms)
        current_room = files.load_room(title)
        new_rooms_dir = name_lists.save_info().get_temp_save_dir_rooms()
        new_items_dir = name_lists.save_info().get_temp_save_dir_items()
        save_rooms_dir = name_lists.save_info().get_save_dir_rooms()
        save_items_dir = name_lists.save_info().get_save_dir_items()
        print "Open each room and edit the visited attribute"
        for title in rooms:
            room = files.load_room(title)
            room['visited'] = True
            files.store_room(room)

        print "Open each item and edit the active attribute"
        for title in items:
            item = files.load_item(title)
            if item['active']:
                item['active'] = False
            else:
                item['active'] = True
            files.store_item(item)

        files.save_game(self.player, current_room, 0)
        print "TEST compare the room files in both dirs to check that they match"
        match, mismatch, errors = filecmp.cmpfiles(save_rooms_dir, new_rooms_dir, rooms)
        for file_ in match:
            self.assertIn(file_, rooms)
        self.assertEqual(len(mismatch), 0)
        self.assertEqual(len(errors), 0)
        print "TEST compare the item files in both dirs to check that they match"
        match, mismatch, errors = filecmp.cmpfiles(save_items_dir, new_items_dir,items)
        for file_ in match:
            self.assertIn(file_, items)
        self.assertEqual(len(mismatch), 0)
        self.assertEqual(len(errors), 0)

        print "TEST that player file exists and that it is a JSON dict"
        save_dir = name_lists.save_info().get_save_dir()
        player_file = os.path.join(save_dir, 'player')
        self.assertEqual(os.path.isfile(player_file), True)
        try:
            with open(player_file, 'r') as player_file:
                player = json.load(player_file)
        except Exception, e:
            player = None

        self.assertIsInstance(player, dict)

    def test_load_save_game(self):
        print ""
        print "TEST load_game functionality, first start a new game."
        print "Make some changes, save the game, start another new game."
        print "Then load game and check that the changes we made are as expected."
        files.new_game()
        rooms = name_lists.room_info().get_titles()
        items = name_lists.item_info().get_titles()
        new_rooms_dir = name_lists.save_info().get_temp_save_dir_rooms()
        new_items_dir = name_lists.save_info().get_temp_save_dir_items()
        save_rooms_dir = name_lists.save_info().get_save_dir_rooms()
        save_items_dir = name_lists.save_info().get_save_dir_items()
        print "Open each room and edit the visited attribute"
        for title in rooms:
            room = files.load_room(title)
            room['visited'] = ""
            files.store_room(room)

        print "Open each item and edit the active attribute"
        for title in items:
            item = files.load_item(title)
            if item['active']:
                item['active'] = False
            else:
                item['active'] = True
            files.store_item(item)

        title = random.choice(rooms)
        current_room = files.load_room(title)
        files.save_game(self.player, current_room, 0)
        files.new_game()
        print "TEST compare the files in temp and save and confirm no match"
        match, mismatch, errors = filecmp.cmpfiles(save_rooms_dir, new_rooms_dir, rooms)
        for file_ in match:
            self.assertNotIn(file_, rooms)
        self.assertEqual(len(match), 0)
        self.assertEqual(len(errors), 0)

        match, mismatch, errors = filecmp.cmpfiles(save_items_dir, new_items_dir,items)
        for file_ in match:
            self.assertNotIn(file_, items)
        self.assertEqual(len(match), 0)
        self.assertEqual(len(errors), 0)

        print "TEST that player file exists and that it is a JSON dict"
        save_dir = name_lists.save_info().get_save_dir()
        player_file = os.path.join(save_dir, 'player')
        self.assertEqual(os.path.isfile(player_file), True)
        try:
            with open(player_file, 'r') as player_file:
                player = json.load(player_file)
        except Exception, e:
            player = None

        self.assertIsInstance(player, dict)

        print "TEST load game"
        p, s, m = files.load_game()
        print "TEST compare the files in temp and save and confirm match"
        match, mismatch, errors = filecmp.cmpfiles(save_rooms_dir, new_rooms_dir, rooms)
        for file_ in match:
            self.assertIn(file_, rooms)
        self.assertEqual(len(mismatch), 0)
        self.assertEqual(len(errors), 0)

        match, mismatch, errors = filecmp.cmpfiles(save_items_dir, new_items_dir,items)
        for file_ in match:
            self.assertIn(file_, items)
        self.assertEqual(len(mismatch), 0)
        self.assertEqual(len(errors), 0)

        self.assertIsInstance(p, dict)
        self.assertEqual(s, True)
        self.assertEqual(m, '')

        print "Remove a room file and an item file and confirm we are able to recover"
        path = os.path.join(save_rooms_dir, 'shore')
        os.remove(path)
        path = os.path.join(save_items_dir, 'rescue whistle')
        os.remove(path)
        p, s, m = files.load_game()
        print "TEST compare the files in temp and save and confirm match"
        match, mismatch, errors = filecmp.cmpfiles(save_rooms_dir, new_rooms_dir, rooms)
        for file_ in match:
            self.assertIn(file_, rooms)
        self.assertEqual(len(mismatch), 0)
        #we should get one error for the missing file!
        self.assertEqual(len(errors), 1)

        match, mismatch, errors = filecmp.cmpfiles(save_items_dir, new_items_dir,items)
        for file_ in match:
            self.assertIn(file_, items)
        self.assertEqual(len(mismatch), 0)
        #we should get one error for the missing file!
        self.assertEqual(len(errors), 1)

        self.assertIsInstance(p, dict)
        self.assertEqual(s, True)
        self.assertEqual(m, '')

        print "Remove the rooms and items dir from save_game dir and confirm recovery"
        shutil.rmtree(save_rooms_dir)
        shutil.rmtree(save_items_dir)
        p,s,m = files.load_game()
        self.assertIsInstance(p, dict)
        self.assertEqual(s, False)
        self.assertEqual(m, 'Rooms missing.Items missing.')
        orig_rooms_dir = os.path.abspath('data/rooms')
        orig_items_dir = os.path.abspath('data/items')
        match, mismatch, errors = filecmp.cmpfiles(orig_rooms_dir, new_rooms_dir, rooms)
        for file_ in match:
            self.assertIn(file_, rooms)
        self.assertEqual(len(mismatch), 0)
        self.assertEqual(len(errors), 0)

        match, mismatch, errors = filecmp.cmpfiles(orig_items_dir, new_items_dir,items)
        for file_ in match:
            self.assertIn(file_, items)
        self.assertEqual(len(mismatch), 0)
        self.assertEqual(len(errors), 0)








#requires the temp_save_game/items to exist and be populated
def getItems():
    item_titles = name_lists.item_info().get_titles()
    items = []
    for title in item_titles:
        items.append(files.load_item(title))
    return items
#ref:
#https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch14s04.html
#ref:
#https://stackoverflow.com/questions/38776104/python-redirect-stdout-and-stderr-to-same-file
def main(out=sys.stderr, verbosity=2):
    #redirect both stderr and stdout into our ouput file!
    sys.stdout = sys.stderr = out
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out,verbosity=verbosity).run(suite)


if __name__ == '__main__':
    with open('results.out', 'w') as f:
        main(f)
    #unittest.main()



# Resources used in writing this code:
# https://docs.python.org/2/library/unittest.html
# https://www.tutorialspoint.com/python/dictionary_get.htm
# https://stackoverflow.com/questions/1911273/is-there-a-better-way-to-compare-dictionary-values/5635309#5635309
# https://stackoverflow.com/questions/8930915/append-dictionary-to-a-dictionary
