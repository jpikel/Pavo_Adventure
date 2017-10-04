import re

import noise_words as noise
import prepositions as prep
import master_words as words


# Private functions
# ----------------------------------------------------------------------------
def _preprocess(input_string):
    """
    Makes string lower case and removes any characters other than letters,
    numbers, and a space.
    """
    preprocessed_string = input_string.lower()
    # Remove any character that is not a number or letter.
    preprocessed_string = re.sub('[^A-Za-z0-9 ]', '', preprocessed_string)
    return preprocessed_string

def _check_for_exact_match(input_string):
    """
    TODO: Write docs
    """
    return 0

def _remove_noise(input_string):
    """
    TODO: Write docs
    """
    return 0

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










# Resources used in writing this module:
# https://stackoverflow.com/questions/6343330/importing-a-long-list-of-constants-to-a-python-file
# https://stackoverflow.com/questions/6797984/how-to-convert-string-to-lowercase-in-python
# https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
# https://docs.python.org/2/library/re.html

