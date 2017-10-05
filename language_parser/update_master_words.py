import json
import os

MASTER_WORDS_FILENAME = "master_words.py"
ITEMS_FILENAME = "items_dict"
ROOMS_FILENAME = "rooms_dict"
VERBS_FILENAME = "verbs_dict"
MASTER_FIELD = "master_word"
WORD_TYPE_FIELD = "type"

def update_master_words():
    """
    Updates the master_words.py file with the contents of individual items,
    rooms, and verbs files generated by the data module. In addition to
    including individual dicts containing the items, rooms, and verbs,
    master_words.py includes an 'all_words' dict that contains all of the
    key-value pairs from those individual dicts
    """
    os.remove(MASTER_WORDS_FILENAME)
    data_dir = os.path.abspath('../data')
    items_full_path = os.path.join(data_dir, ITEMS_FILENAME)
    rooms_full_path = os.path.join(data_dir, ROOMS_FILENAME)
    verbs_full_path = os.path.join(data_dir, VERBS_FILENAME)
    with open(MASTER_WORDS_FILENAME, "a") as master_file:
        with open(items_full_path, "r") as items_file:
            items_dict_str = items_file.read()
            items_dict = json.loads(items_dict_str.lower())
        with open(rooms_full_path, "r") as rooms_file:
            rooms_dict_str = rooms_file.read()
            rooms_dict = rooms_dict = json.loads(rooms_dict_str.lower())
        with open(verbs_full_path, "r") as verbs_file:
            verbs_dict_str = verbs_file.read()
            verbs_dict = json.loads(verbs_dict_str.lower())
        # Save dicts for each word type to the master words file.
        items_dict_str = json.dumps(items_dict, indent=3)
        master_file.write("items = " + items_dict_str + "\n")
        rooms_dict_str = json.dumps(rooms_dict, indent=3)
        master_file.write("rooms = " + rooms_dict_str + "\n")
        verbs_dict_str = json.dumps(verbs_dict, indent=3)
        master_file.write("actions = " + verbs_dict_str + "\n")
        # Create a dict with all of the words
        # This dict will include the word type and the
        # master word (i.e., the word the game engine
        # knows/uses in command processing) for each word.
        expanded_items_dict = {}
        for word, master_word in items_dict.items():
            word_info = {
                MASTER_FIELD: master_word,
                WORD_TYPE_FIELD: "item"
            }
            expanded_items_dict[word] = word_info
        expanded_rooms_dict = {}
        for word, master_word in rooms_dict.items():
            word_info = {
                MASTER_FIELD: master_word,
                WORD_TYPE_FIELD: "room"
            }
            expanded_rooms_dict[word] = word_info
        expanded_verbs_dict = {}
        for word, master_word in verbs_dict.items():
            word_info = {
                MASTER_FIELD: master_word,
                WORD_TYPE_FIELD: "action"
            }
            expanded_verbs_dict[word] = word_info
        # Combine all of the expanded dicts into one master dict.
        all_words = {}
        all_words.update(expanded_items_dict)
        all_words.update(expanded_rooms_dict)
        all_words.update(expanded_verbs_dict)
        all_words_str = json.dumps(all_words, indent=3)
        master_file.write("all_words = " + all_words_str)

if __name__ == "__main__":
    update_master_words()

# Resources used in writing this script:
# https://stackoverflow.com/questions/3758866/python-get-path-to-file-in-sister-directory
# https://stackoverflow.com/questions/7132861/building-full-path-filename-in-python
# http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
# https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
# https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary
# https://docs.python.org/2/library/json.html
# https://stackoverflow.com/questions/20145902/how-to-extract-dictionary-single-key-value-pair-in-variables
# https://stackoverflow.com/questions/33715427/whenever-i-try-parsing-json-file-i-get-keyerror-in-python