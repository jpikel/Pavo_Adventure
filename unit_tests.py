import json
import os
import unittest

import language_parser.master_words as words
import language_parser.command_parser as parser

# Constants used in testing the language parser
# ---------------------------------------------------------------------------
MASTER_WORDS_FILENAME = "master_words.py"
FEATURES_FILENAME = "feature_dict"
ITEMS_FILENAME = "items_dict"
ROOMS_FILENAME = "rooms_dict"
VERBS_FILENAME = "verbs_dict"

NUM_CARDINAL_DIRECTIONS = 4

class TestMasterParser(unittest.TestCase):

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

    # def test_master_words_verbs(self):
    # TODO: Write this test

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

    # def test_parse_feature_action(self):
    # TODO: Write this test

    # def test_parse_feature_only(self):
    # TODO: Write this test

    # def test_parse_item_action(self):
    # TODO: Write this test

    # def test_parse_item_only(self):
    # TODO: Write this test

    # def test_room_action(self):
    # TODO: Write this test

    # def test_room_only(self):
    # TODO: Write this test

    # def test_parse_unknown(self):
    # TODO: Write this test


if __name__ == '__main__':
    unittest.main()



# Resources used in writing this code:
# https://docs.python.org/2/library/unittest.html
# https://www.tutorialspoint.com/python/dictionary_get.htm
# https://stackoverflow.com/questions/1911273/is-there-a-better-way-to-compare-dictionary-values/5635309#5635309