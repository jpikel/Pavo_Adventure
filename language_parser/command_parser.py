import re

import noise_words as noise
import prepositions as prep
import master_words as words

class WORD_TYPES:
    ACTION = "action"
    EXIT = "exit"
    FEATURE = "feature"
    ITEM = "item"
    ROOM = "room"

class COMMAND_TYPES:
    ACTION_ONLY = "action_only"
    EXIT = "exit"
    EXIT_ONLY = "exit_only"
    FEATURE_ACTION = "feature_action"
    FEATURE_ONLY = "feature_only"
    ITEM_ACTION = "item_action"
    ITEM_ONLY = "item_only"
    OTHER = "other"
    ROOM_ACTION = "room_action"
    ROOM_ONLY = "room_only"

class OUTPUT_FIELDS:
    ACTION = "action"
    DIRECTION = "direction"
    EXIT = "exit"
    FEATURE = "feature"
    GENERAL = "general"
    ITEM = "item"
    NAME = "name"
    OTHER = "other"
    PROCESSED = "processed"
    ROOM = "room"
    TYPE = "type"

# Private functions
# ----------------------------------------------------------------------------
def _preprocess(input_string):
    """
    Makes string lower case and removes any characters other than letters,
    numbers, and a space.

    Returns: A processed string.
    """
    preprocessed_string = input_string.lower()
    # Remove any character that is not a number or letter.
    preprocessed_string = re.sub('[^A-Za-z0-9 ]', '', preprocessed_string)
    return preprocessed_string

def _check_for_exact_match(input_string):
    """
    Checks whether the input_string matches one (and only one) of the
    words recognized by the program directly. If so, the parser
    can bypass all of the other text processing and matching functions
    and go directly to building an output dict.

    Returns: A boolean specifying whether there was an exact match.
    """
    if input_string in words.all_words:
        return True
    return False

def _build_exact_match_output(input_string):
    """
    Where the input_string consists of a single word recognized by the program,
    creates and returns an output dict for that word.

    Returns: A dict containing information about the input. The format of the
             output dict varies depending on the type of the word input.
    """
    #TODO: Add error handling for situation in which word is not actually in dict?
    input_word = input_string
    word_type = words.all_words[input_word]["type"]
    master_word = words.all_words[input_word]["master_word"]
    # All of these dicts will have processed equal True.
    output_dict = {
        OUTPUT_FIELDS.OTHER: {
            OUTPUT_FIELDS.PROCESSED: True
        }
    }
    # Build the rest of the output dict based on the word type of the command.
    if word_type == WORD_TYPES.ACTION:
        output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.ACTION_ONLY
        action_dict = {
            OUTPUT_FIELDS.ACTION: master_word
        }
        output_dict[OUTPUT_FIELDS.GENERAL] = action_dict
    if word_type == WORD_TYPES.EXIT:
        output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.EXIT_ONLY
        exit_dict = {
            OUTPUT_FIELDS.EXIT: master_word
        }
        output_dict[OUTPUT_FIELDS.EXIT] = exit_dict
    if word_type == WORD_TYPES.FEATURE:
        output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.FEATURE_ONLY
        feature_dict = {
            OUTPUT_FIELDS.NAME: master_word
        }
        output_dict[OUTPUT_FIELDS.FEATURE] = feature_dict
    if word_type == WORD_TYPES.ITEM:
        output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.ITEM_ONLY
        item_dict = {
            OUTPUT_FIELDS.NAME: master_word
        }
        output_dict[OUTPUT_FIELDS.ITEM] = item_dict
    if word_type == WORD_TYPES.ROOM:
        output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.ROOM_ONLY
        room_dict = {
            OUTPUT_FIELDS.ROOM: master_word
        }
        output_dict[OUTPUT_FIELDS.ROOM] = room_dict
    return output_dict

def _remove_noise(input_string):
    """
    Returns a copy of the input string with any words that are on the noise
    words list removed.

    Returns: A string with the noise words removed.
    """
    string = input_string
    noise_words = noise.noise_words
    re_noise_words = '|'.join(word for word in noise_words)
    print re_noise_words
    # Remove the noise words if they are the beginning of the input string and
    # followed by a space, between two spaces, or at the end of the input
    # string and preceeded by a space. That is, if a word is within another
    # word (e.g., 'the' is within 'theater'), do not remove it.
    noise_at_start_of_string = '\A' + re_noise_words + ' '
    string = re.sub(noise_at_start_of_string, '', string, count=1)
    noise_at_end_of_string = ' (' + re_noise_words + ')$'
    string = re.sub(noise_at_end_of_string, '', string, count=1)
    noise_in_middle_of_string = ' (' + re_noise_words + ') '
    string = re.sub(noise_in_middle_of_string, ' ', string)
    return string

def _normalize(input_string):
    """
    TODO: Write docs
    """
    return 0

def _match_user_input_pattern(input_string):
    """
    TODO: Write docs
    """
    return 0

    # TODO: Add additional methods to generate output dicts depending on match

# Public function
# ----------------------------------------------------------------------------
def parse_command(command):
    """
    TODO: Write docs
    """
    current_string = _preprocess(command)
    # Exit early if the input string consists of a single, recognized word.
    # In that case, no other processing/matching is necessary.
    if (_check_for_exact_match(current_string)):
        return _build_exact_match_output(current_string)
    current_string = _remove_noise(current_string)












# Resources used in writing this module:
# https://stackoverflow.com/questions/6343330/importing-a-long-list-of-constants-to-a-python-file
# https://stackoverflow.com/questions/6797984/how-to-convert-string-to-lowercase-in-python
# https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
# https://docs.python.org/2/library/re.html
# https://stackoverflow.com/questions/22741526/how-do-i-turn-a-list-of-words-into-a-sentence-string
# https://www.tutorialspoint.com/python/string_join.htm