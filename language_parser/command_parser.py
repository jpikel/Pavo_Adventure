import json
import re

import noise_words as noise
import master_words as words

class REGEX_PATTERNS:
    KNOWN_ACTION_AND_ITEM = "recognized_action_and_recognized_item"
    KNOWN_ACTION_AND_ROOM = "recognized_action_and_recognized_room"
    KNOWN_ACTION_AND_FEATURE = "recognized_action_and_recognized_feature"
    NO_MATCH = "no_match"

class WORD_TYPES:
    ACTION = "action"
    FEATURE = "feature"
    ITEM = "item"
    ROOM = "room"

class COMMAND_TYPES:
    ACTION_ONLY = "action_only"
    FEATURE_ACTION = "feature_action"
    FEATURE_ONLY = "feature_only"
    ITEM_ACTION = "item_action"
    ITEM_ONLY = "item_only"
    OTHER = "other"
    ROOM_ACTION = "room_action"
    ROOM_ONLY = "room_only"

class OUTPUT_FIELDS:
    ACTION = "action"
    FEATURE = "feature"
    ITEM = "item"
    NAME = "name"
    PROCESSED = "processed"
    COMMAND = "command"
    RECOGNIZED_WORDS = "command"
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
    # Convert any hyphens to spaces
    preprocessed_string = re.sub('-', ' ', preprocessed_string)
    # Remove any character that is not a number, letter, or space.
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

    Returns: A dict containing information about the input. See the help for
    parse_command for information about the format of the dict.
    """
    input_word = input_string
    word_type = words.all_words[input_word]["type"]
    master_word = words.all_words[input_word]["master_word"]
    # All of these dicts will have processed equal True.
    output_dict = {
        OUTPUT_FIELDS.PROCESSED: True
    }
    # Build the rest of the output dict based on the word type of the command.
    if word_type == WORD_TYPES.ACTION:
        output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.ACTION_ONLY
        command_dict = {
            OUTPUT_FIELDS.ACTION: master_word
        }
    elif word_type == WORD_TYPES.FEATURE:
        output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.FEATURE_ONLY
        command_dict = {
            OUTPUT_FIELDS.FEATURE: master_word
        }
    elif word_type == WORD_TYPES.ITEM:
        output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.ITEM_ONLY
        command_dict = {
            OUTPUT_FIELDS.ITEM: master_word
        }
    elif word_type == WORD_TYPES.ROOM:
        output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.ROOM_ONLY
        command_dict = {
            OUTPUT_FIELDS.ROOM: master_word
        }
    else:
        # Construct an output dict with the processd value equal to False,
        # which tells the game engine that the parser could not interpret
        # the command.
        output_dict = {}
        output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.OTHER
        output_dict[OUTPUT_FIELDS.PROCESSED] = False
        return output_dict
    output_dict[OUTPUT_FIELDS.COMMAND] = command_dict
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
    # Remove the noise words if they are the beginning of the input string and
    # followed by a space, between two spaces, or at the end of the input
    # string and preceeded by a space. That is, if a word is within another
    # word (e.g., 'the' is within 'theater'), do not remove it.
    noise_at_start_of_string = '^(' + re_noise_words + ') '
    string = re.sub(noise_at_start_of_string, '', string, count=1)
    noise_at_end_of_string = ' (' + re_noise_words + ')$'
    string = re.sub(noise_at_end_of_string, '', string, count=1)
    noise_in_middle_of_string = ' (' + re_noise_words + ') '
    string = re.sub(noise_in_middle_of_string, ' ', string)
    # If removing the noise leaves more than one space between words, remove
    # that extra space.
    string = re.sub(' +', ' ', string)
    return string

def _generate_length_ordered_keys(input_dict):
    """
    Sorts the keys in the input_dict in reversed order of length (i.e., longest
    key first).

    Returns: List of the keys in the input_dict sorted in reverse order of length.
    """
    all_keys = []
    for key in input_dict:
        all_keys.append(key)
    sorted_keys = reversed(sorted(all_keys, key=len))
    return sorted_keys

def _generate_full_match_regex_patterns():
    """
    Generates a dict in which the keys are names of recognized input patterns
    and the values are regular expressions that describe those patterns.

    Returns: A dict of regex patterns and their labels.
    """
    patterns = {}
    # Generate '|'-separated lists of each word type, ordered by word length,
    # from longest to smallest. Ordering is necessary to ensure that the
    # longest matching word/phrase is used. (i.e., match on 'look at' instead
    # of 'look').
    action_or = '|'.join(_generate_length_ordered_keys(words.actions))
    feature_or = '|'.join(_generate_length_ordered_keys(words.features))
    item_or = '|'.join(_generate_length_ordered_keys(words.items))
    room_or = '|'.join(_generate_length_ordered_keys(words.rooms))
    # Create list of different patterns that consist entirely of
    # known words.
    patterns[REGEX_PATTERNS.KNOWN_ACTION_AND_ITEM] = \
        '\\b(' + action_or + ')\\b \\b(' + item_or + ')\\b'
    patterns[REGEX_PATTERNS.KNOWN_ACTION_AND_ROOM] = \
        '\\b(' + action_or + ')\\b \\b(' + room_or + ')\\b'
    patterns[REGEX_PATTERNS.KNOWN_ACTION_AND_FEATURE] = \
        '\\b(' + action_or + ')\\b \\b(' + feature_or + ')\\b'
    return patterns

def _match_user_input_pattern(input_string, regex_patterns):
    """
    Determines whether any of the regex patterns specified match the input
    string and outputs a tuple identifying the matching pattern and matching
    words (if any).

    Returns: If a match was found, returns a tuple containing the pattern key,
    which identifies the matching pattern, and a list of the groups that
    matched. If no match was found, returns a ("no_match", []) tuple.
    """
    for pattern_key, pattern in regex_patterns.iteritems():
        match = re.match(pattern, input_string)
        if match:
            return (pattern_key, list(match.groups()))
    return (REGEX_PATTERNS.NO_MATCH, [])

def _generate_output_from_pattern_key(pattern_key, matched_words):
    """
    Takes the output from _match_user_input_pattern, which consists of a tuple
    containing (a) the name of the regex pattern that matched on the input
    command, and (b) a list of the recognized words that matched, and uses
    that information to generate an output dict with information about the
    user-input command.

    Returns: A dict containing information about the input. See the help for
    parse_command for information about the format of the dict.
    """
    output_dict = {}
    if pattern_key == REGEX_PATTERNS.NO_MATCH:
        command_type = COMMAND_TYPES.OTHER
        processed = False
    else:
        processed = True
        if pattern_key == REGEX_PATTERNS.KNOWN_ACTION_AND_ITEM:
            # Given the pattern key, we know that the first
            # word matched is an action and the second word matched is an
            # item.
            command_type = COMMAND_TYPES.ITEM_ACTION
            action_matched = matched_words[0]
            item_matched = matched_words[1]
            # Translate the words that matched into the "master" words that are
            # recognized by the game.
            # This step is needed to translate aliases to official game words.
            action = words.all_words[action_matched]["master_word"]
            item = words.all_words[item_matched]["master_word"]
            output_dict[OUTPUT_FIELDS.COMMAND] = \
                {"action": action, "item": item}
        elif pattern_key == REGEX_PATTERNS.KNOWN_ACTION_AND_ROOM:
            # Given the pattern key, we know that the first
            # word matched is an action and the second word matched is a room.
            command_type = COMMAND_TYPES.ROOM_ACTION
            action_matched = matched_words[0]
            room_matched = matched_words[1]
            # Translate the words that matched into the "master" words that are
            # recognized by the game.
            # This step is needed to translate aliases to official game words.
            action = words.all_words[action_matched]["master_word"]
            room = words.all_words[room_matched]["master_word"]
            output_dict[OUTPUT_FIELDS.COMMAND] = \
                {"action": action, "room": room}
        elif pattern_key == REGEX_PATTERNS.KNOWN_ACTION_AND_FEATURE:
            # Given the pattern key, we know that the first
            # word matched is an action and the second word matched is a feature.
            command_type = COMMAND_TYPES.FEATURE_ACTION
            action_matched = matched_words[0]
            feature_matched = matched_words[1]
            # Translate the words that matched into the "master" words that are
            # recognized by the game.
            # This step is needed to translate aliases to official game words.
            action = words.all_words[action_matched]["master_word"]
            feature = words.all_words[feature_matched]["master_word"]
            output_dict[OUTPUT_FIELDS.COMMAND] = \
                {"action": action, "feature": feature}
    # Every pattern will have a "type" and "processed" key.
    output_dict[OUTPUT_FIELDS.TYPE] = command_type
    output_dict[OUTPUT_FIELDS.PROCESSED] = processed
    return output_dict

def _generate_output_for_partial_or_no_match(input_string):
    """
    Takes an input string that does not match on any of the known input patterns
    and generates an output dict that includes 'other' as the 'command_type',
    a 'processed' value of False, and a list of words in the input string that
    are recognized by the game (if any).

    This method should be called only after the program has attempted to match
    on the known input patterns but has not matched on any of them.

    Returns: A dict containing information about the input. See the help for
    parse_command for information about the format of the dict.
    """
    # Break input string into individual words.
    input_words = input_string.split()
    # Check if each word is on the master words list.
    recognized_words = {}
    for word in input_words:
        # If a word is on the master words list, add its corresponding
        # master word and type to the recognized words dict.
        if word in words.all_words:
            master_word = words.all_words[word]["master_word"]
            word_type = words.all_words[word]["type"]
            recognized_words[master_word] = word_type
    # Construct an output dict.
    output_dict = {}
    output_dict[OUTPUT_FIELDS.TYPE] = COMMAND_TYPES.OTHER
    output_dict[OUTPUT_FIELDS.PROCESSED] = False
    if recognized_words:
        output_dict[OUTPUT_FIELDS.RECOGNIZED_WORDS] = recognized_words
    return output_dict

# Public function
# ----------------------------------------------------------------------------
def parse_command(command):
    """
    Produces an output dict with information about the input command that is
    in a format that the game engine can use.

    Returns: A dict containing information about the input, which has the following
        key-value pairs:
        {
            "type": <one of the COMMAND_TYPES>,
            "command": {
                <dict with the applicable WORD_TYPES as keys and recognized words
                of that type as the values>
            },
            "processed": <boolean value indicating whether the parser was
            able to 'understand' the command>
        }

    """
    command = _preprocess(command)
    # Exit early if the input string consists of a single, recognized word.
    # In that case, no other processing/matching is necessary.
    if (_check_for_exact_match(command)):
        return _build_exact_match_output(command)
    command = _remove_noise(command)
    # Try matching recognized words with the full user input.
    full_patterns = _generate_full_match_regex_patterns()
    match_info = _match_user_input_pattern(command, full_patterns)
    # If a match against the full user input was found, generate the
    # output dict based on that match.
    output_dict = {}
    if (match_info[0]) is not REGEX_PATTERNS.NO_MATCH:
        output_dict = _generate_output_from_pattern_key(match_info[0], match_info[1])
    # Otherwise, analyze the user input for a partial match.
    else:
        output_dict = _generate_output_for_partial_or_no_match(command)
    return output_dict


# Resources used in writing this module:
# https://stackoverflow.com/questions/6343330/importing-a-long-list-of-constants-to-a-python-file
# https://stackoverflow.com/questions/6797984/how-to-convert-string-to-lowercase-in-python
# https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
# https://docs.python.org/2/library/re.html
# https://stackoverflow.com/questions/22741526/how-do-i-turn-a-list-of-words-into-a-sentence-string
# https://www.tutorialspoint.com/python/string_join.htm
# https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops
# https://stackoverflow.com/questions/11789877/regexp-match-sequence-that-not-contains-list-of-words-net
# https://stackoverflow.com/questions/1546226/a-simple-way-to-remove-multiple-spaces-in-a-string-in-python
# https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list
# https://developers.google.com/edu/python/regular-expressions
# https://www.regular-expressions.info/alternation.html
# https://stackoverflow.com/questions/43198074/how-to-sort-a-list-of-words-by-length
# https://stackoverflow.com/questions/3940128/how-can-i-reverse-a-list-in-python
# https://stackoverflow.com/questions/4173787/string-exact-match