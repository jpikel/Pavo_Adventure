"""
Filename - validator.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description - a json validator for a text file to ensure it is correct json pattern
"""

def add_stack(c):
    print("Adding " + c)
def pop_stack(c):
    print("Popping " + c)

def error_msg(line, c):
    print("Issue with char at byte number: "+ str(line.index(c)))
    print("In line: " + line)
    exit()


with open("../data/items_dict", 'r') as text_file:
    data = text_file.readlines()
    text_file.close()

char_stack = []

for line in data:
    for c in line:
        if c == ",":
            char_stack.append(c)
            add_stack(c)
        elif char_stack and (c == "{" or c == '"') and char_stack[-1] == ",":
            pop_stack(char_stack.pop())
        elif char_stack and char_stack[-1] == ',' and c != ' ':
            error_msg(line, c)
        elif c == '{':
            char_stack.append(c)
            add_stack(c)
        elif c == '}' and char_stack[-1] == '{':
            pop_stack(char_stack.pop())
        elif c == '"' and char_stack[-1] == '"':
            pop_stack(char_stack.pop())
        elif c == '"':
            char_stack.append(c)
            add_stack(c)
        elif c == ":" and char_stack[-1] == '"':
            error_msg(line, c)
        elif c == ",":
            char_stack.append(c)
