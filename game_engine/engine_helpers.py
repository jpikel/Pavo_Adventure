"""
Filename - engine_helpers.py
Team - Pavo
Group Members - Emily Caveness, Alexander Laquitara, Johannes Pikel
Class - CS467-400 Capstone
Term - Fall 2017
Description -
"""
#REFERENCES:
#https://stackoverflow.com/questions/4197805/python-for-loop-look-ahead
#https://docs.python.org/2/howto/curses.html

import textwrap
import string
import sys
import os
import subprocess
import time
import random
import file_handler.name_lists as info
USE_CURSES = False
if sys.platform == 'linux' or sys.platform == 'linux2':
	import curses
	USE_CURSES = True

#DEFINE GLOBAL FOR THE VARIOUS CURSES WINDOWS
MIN_COLS = 121
MIN_ROWS = 50
MAIN_WIN_ROWS = 30
MAIN_WIN_COLS = 86
TIME_WIN_ROWS = 11
TIME_WIN_COLS = 30
STAT_WIN_ROWS = 18
STAT_WIN_COLS = 30
INPUT_WIN_ROWS = 3 
INPUT_WIN_COLS = 117
#USED IN THE PRINT HELP MENU
VERB_DICT = info.verb_info().get_verb_definitions()

#experiment text wrapping
CHARS_PER_LINE = 80
#The main splash screen
SPLASH_MESSAGE = [ 
"****************************************************************************",
"",
" ########  ########  ######   #######  ##          ###    ######## ######## ",
" ##     ## ##       ##    ## ##     ## ##         ## ##      ##    ##       ",
" ##     ## ##       ##       ##     ## ##        ##   ##     ##    ##       ",
" ##     ## ######    ######  ##     ## ##       ##     ##    ##    ######   ",
" ##     ## ##             ## ##     ## ##       #########    ##    ##       ",
" ##     ## ##       ##    ## ##     ## ##       ##     ##    ##    ##       ",
" ########  ########  ######   #######  ######## ##     ##    ##    ######## ",
 " ",
"          ##  #######  ##     ## ########  ##    ## ######## ##    ## ",
"          ## ##     ## ##     ## ##     ## ###   ## ##        ##  ##  ",
"          ## ##     ## ##     ## ##     ## ####  ## ##         ####   ",
"          ## ##     ## ##     ## ########  ## ## ## ######      ##    ",
"    ##    ## ##     ## ##     ## ##   ##   ##  #### ##          ##    ",
"    ##    ## ##     ## ##     ## ##    ##  ##   ### ##          ##    ",
"     ######   #######   #######  ##     ## ##    ## ########    ##    ",
"",
"*****************************************************************************",
"Welcome To Desolate Journey",
"What would you like to do?",
"->  New Game",
"->  Load Game",
"->  Quit"]

#Theses are part of curses to write out DESOLATE JOURNEY as the game progesses
CHAR_D = [ "######", "##****##", "##****##", "##****##", "######"]
CHAR_E = [ "########", "##", "######", "##", "########"]
CHAR_S = [ "**######", "##", "**####", "******##", "######"]
CHAR_O = [ "**####", "##****##", "##****##", "##****##", "**####"]
CHAR_L = [ "##", "##", "##", "##", "########"]
CHAR_A = [ "**####", "##****##", "########", "##****##", "##****##"]
CHAR_T = [ "##########", "****##", "****##", "****##", "****##"]
CHAR_J = [ "******##", "******##", "******##", "##****##", "**####"]
CHAR_U = [ "##****##", "##****##", "##****##", "##****##", "**####"]
CHAR_R = [ "######", "##****##", "######", "##****##", "##****##"]
CHAR_N = [ "##******##", "####****##", "##**##**##", "##****####", "##******##"]
CHAR_Y = [ "##******##", "**##**##", "****##", "****##", "****##"]
ART_COLS = [5, 15, 25, 35, 45, 55, 65, 77, 25, 35, 45, 55, 65, 77, 87]
ART = [CHAR_D, CHAR_E, CHAR_S, CHAR_O, CHAR_L, CHAR_A, CHAR_T, CHAR_E,
		CHAR_J, CHAR_O, CHAR_U, CHAR_R, CHAR_N, CHAR_E, CHAR_Y]
#only used in curses to present an image with the time of day
MORNING =[" "," "," ",
		"     \\ | /",
		"      .-.               .-.",
		"  -==(   )==-          ( (",
		"----------------------------",
		"",
		"It is morning. "]

AFTERNOON = [" ",
		"           \\ | /",
		"            .-.",
		"        -==(   )==-",
		"            '-'",
		"           / | \\",
		"----------------------------",
		" ",
		"It is afternoon. "]

EVENING = [" "," "," ",
		"                   \\ | /",
		"  .-.               .-.",
		" ( (            -==(   )==-",
		"----------------------------",
		" ",
		"It is evening. "]
NIGHT = [" ", " ",
		"   *      .-.    *",
		"     *   ( (         *",
		" *        '-' ",
		"               *        *",
		"----------------------------",
		" ", 
		"It is night. "]
		
FIREWORKS =["       :_\/_:   _\(/_  .:.*_\/_*",
		"  .''.:  /\ :   ./)\   ':'* /\ *",
		" :_\/_:'.:::.	 ' *''*	   ",
		" : /\  ::::::	  *_\/_*	 ",
		"  '..'	 ':::'	  * /\ *	 ",
		"	  *			   *..*	",
		"	   *",
		"           *",]
PAVO =["                          _______        ___",
	    "                       _ /     |   \_   (  .)",
	    "                    _/   \     |     \ /    > >",
	    "                 / \      \    |     /   }",
	    "                /      \     _ - -  /    }}",
		"               | -  _    \-/            )}",
		"             / _ _ _ _> \             /",
		"             |__________ \   / /  / /",
		"                          \_/_/___/",
		"                            |   |",
		"                            |   |",
		"                            |   |",
		"                           /!\ /!\ "]

class response_struct():
	"""
	This structure is used for most all the responses sent back to the
		structure is
		"title":string the title being used
		"action": string the action being used
		"artifact": if the verb has an artifact usualy with read put it here
		"description": string the description of the the thing
		"success": boolean, whether the move occured or action occurred
		"distance_from_room": distance travel
	"""
	def __init__(self):
		self.response = {
					"title":None,
					"action":None,
					"artifact": [],
					"description":None,
					"success":False,
					"distance_from_room":0,
					"modifiers": {},
					"room_artifact":{}
				}
	@property
	def response(self):
		return self.response
	@property
	def title(self):
		return self.response['title']
	@title.setter
	def title(self, title):
		self.response['title'] = title
	@property
	def action(self):
		return self.response['action']
	@action.setter
	def action(self, action):
		self.response['action'] = action
	@property
	def success(self):
		return self.response['success']
	@success.setter
	def success(self, value):
		self.response['success'] = value
	@property
	def artifact(self):
		return self.response['artifact']
	@artifact.setter
	def artifact(self, artifact):
		self.response['artifact'] = artifact
	@property
	def description(self):
		return self.response['description']
	@description.setter
	def description(self, description):
		self.response['description'] = description
	@property
	def distance_from_room(self):
		return self.response['distance_from_room']
	@distance_from_room.setter
	def distance_from_room(self, dist):
		self.response['distance_from_room'] = dist
	@property
	def modifiers(self):
		return self.response['modifiers']
	@modifiers.setter
	def modifiers(self, value):
		self.response['modifiers'] = value
	@property
	def room_artifact(self):
		return self.response['room_artifact']
	@room_artifact.setter
	def room_artifact(self, value):
		self.response['room_artifact'] = value


def get_input(comment=''):
	"""
	gets some input and returns it to the user
	"""
	comment += '\n->'
	return str.lower(raw_input(comment))

def multi_printer(text, player_name=None):
	"""
	a generic printer that can handle a list of text and print that to screen
	or a single string
	"""
	if isinstance(text, list):
		for line in text:
			if line == ' ': print ''
			if player_name is not None: line = replace_player_name(line, player_name)
			lines = textwrap.wrap(line, CHARS_PER_LINE)
			for wrapped_line in lines: print wrapped_line
	elif isinstance(text, basestring):
		if player_name is not None: text = replace_player_name(text, player_name)
		lines = textwrap.fill(text, CHARS_PER_LINE)
		print lines
	else:
		print 'Error: did not receive list of strings or string'


def replace_player_name(text, player_name):
	"""
	searchs the string for <playername> and inserts the player_name passed in
	returns the string
	"""
	sub_string = "<playername>"
	return string.replace(text, sub_string, player_name)

def print_basic():
	text = []
	text.append('*'*20 + 'Help' + '*'*20)
	text.append('Verb'.ljust(12) + '  :: ' + ' verb definition')
	for key in VERB_DICT:
		text.append(key.ljust(12) + ' ::  ' + VERB_DICT[key])
	multi_printer(text)

def remove_punc(word):
	if isinstance(word, str):
		return word.translate(None, string.punctuation)
	else:
		return word.encode('utf-8').translate(None, string.punctuation)


	#------------------------------------------------------
	#This starts the UI curses section
	#------------------------------------------------------
class ui():
	"""
	the UI class holds all the functions to write to the various curses
	windows. Initializes the curses main window and handles errors.
	"""
	ROW = 0
	COL = 1
	def __init__(self):
		self.back_win = None
		self.main_win = None
		self.input_win = None
		self.stat_win = None
		self.time_win = None
		self.main_row = 0
		self.stat_row = 0
		self.index_loc = 0

	def init_windows(self, stdscr):
		"""
		initializes the game windows as new windows and initializes some color pairs
		"""
		if USE_CURSES and self.terminal_size():
			self.back_win = stdscr
			self.fill_back()
			self.main_win = curses.newwin(MAIN_WIN_ROWS, MAIN_WIN_COLS, 2, 2)
			self.input_win = curses.newwin(INPUT_WIN_ROWS, INPUT_WIN_COLS, 33, 2)
			self.stat_win = curses.newwin(STAT_WIN_ROWS, STAT_WIN_COLS, 14, 89)
			self.time_win = curses.newwin(TIME_WIN_ROWS, TIME_WIN_COLS, 2, 89)
			self.init_colors()

	def fill_back(self):
		"""
		fills the terminal window with * for 121 columns and 50 rows
		"""
		row =0
		for _ in range(1,MIN_ROWS):
			text = '*'*121
			self.back_win.addstr(row, 0, text, curses.A_BOLD)
			row += 1
		self.back_win.refresh()

	def reset_art(self):
		"""
		removes the art work written to the main window
		"""
		self.fill_back()
		self.index_loc = 0

	def write_art(self):
		"""
		writes out DESOLATE JOURNEY in the bottom of the back window
		"""
		if self.index_loc < len(ART):
			row = 37
			col = ART_COLS[self.index_loc]
			letter = ART[self.index_loc]
			if self.index_loc >= 8:
				row = 43
			for line in letter:
				self.back_win.addstr(row, col, line, curses.A_BOLD)
				row += 1
			self.back_win.refresh()
			self.index_loc += 1

	def write_main(self, text, player_name=None, row=1, col=1):
		"""
		erases the main game window, then either writes the list or the string
		to the main window wrapping the text to fit
		the last row written to is stored in self
		"""
		self.main_win.erase()
		if isinstance(text, list):
			for line in text:
				if line == " ": row += 1
				if player_name is not None: line = replace_player_name(line, player_name)
				self.main_win.addstr(row, col, line, curses.A_BOLD)
				row +=1
				if row >= MAIN_WIN_ROWS: break
		elif isinstance(text, basestring):
			if player_name is not None: text = replace_player_name(text, player_name)
			lines = textwrap.wrap(text, CHARS_PER_LINE)
			for line in lines:
				self.main_win.addstr(row, col, line, curses.A_BOLD)
				row += 1
				if row >= MAIN_WIN_ROWS: break
		else:
			self.main_win.addstr('Error: did not receive list of strings or string')
		self.main_row = row

	def write_main_artifact(self, text):
		"""
		one row below the most recent row written to writes out a 
		list of strings to the main window
		"""
		row = self.main_row + 1
		if isinstance(text, list):
			for line in text:
				if line == " ": row += 1
				self.main_win.addstr(row, ui.COL, line, curses.A_BOLD)
				row +=1
				if row >= MAIN_WIN_ROWS: break

	def write_main_mid(self, text):
		"""
		handles writting a string to middle of the main window starting 1 row below
		the main body of text
		"""
		row = self.main_row + 1
		lines = textwrap.wrap(text, CHARS_PER_LINE)
		for line in lines:
			self.main_win.addstr(row, ui.COL, line, curses.A_BOLD)
			row += 1
			if row >= MAIN_WIN_ROWS: break
		if row < MAIN_WIN_ROWS:
			blank_line = " "*int(MAIN_WIN_COLS-2)
			for _ in range(row, MAIN_WIN_ROWS-1):
				self.main_win.addstr(row, ui.COL,blank_line)
		self.main_win.refresh()

	def write_main_bottom(self, text):
		"""
		writes a signle line of text less that the length of the main window
		to the last row of the main window
		"""
		if len(text) > MAIN_WIN_COLS-2: text = text[:MAIN_WIN_COLS-2]
		blank_line = ' '*40
		self.main_win.addstr(MAIN_WIN_ROWS-1, ui.COL, blank_line)
		self.main_win.addstr(MAIN_WIN_ROWS-1, ui.COL, text, curses.color_pair(4))
		self.main_win.refresh()

#    def write_input(self, text, row=0, col= 30):
#        self.input_win.addstr(row, col, text)

	def write_stat(self, text):
		"""
		writes to the stat window that typically contains the character's illness,
		hunger and cold.  Inventory also gets written to this window
		stores the last row written to in this window
		stops if we get to the last row
		"""
		self.stat_win.erase()
		row = 1
		lines = textwrap.wrap(text, 26)
		for line in lines:
			line = line[:STAT_WIN_COLS-1]
			self.stat_win.addstr(row, ui.COL, line, curses.color_pair(2))
			row += 1
			if row >= STAT_WIN_ROWS: 
				self.stat_win.refresh()
				break
		self.stat_win.refresh()
		self.stat_row = row

	def write_stat_append(self, text):
		"""
		appends to what is currently in the stat window.  This function is not currently
		called anywhere
		"""
		row = self.stat_row
		lines = textwrap.wrap(text, 26)
		for line in lines:
			self.stat_win.addstr(row, ui.COL, line, curses.color_pair(3))
			row += 1
			if row >= STAT_WIN_ROWS: 
				self.stat_win.refresh()
				break
		self.stat_win.refresh()

	def write_time(self, text):
		"""
		writes a list or string to the time window
		stops when we get to the bottom of the window
		"""
		self.time_win.erase()
		row = 1
		for line in text:
			self.time_win.addstr(row, ui.COL, line, curses.color_pair(4))
			row += 1
			if row >= TIME_WIN_ROWS:
				break

	def refresh_all(self):
		"""
		refreshes all screens except the back window
		"""
		self.stat_win.refresh()
		self.input_win.refresh()
		self.time_win.refresh()
		self.main_win.refresh()

	def end_windows(self):
		"""
		ends all screens
		"""
		curses.endwin()

	def get_input(self, comment=''):
		"""
		turns on echo, erases what ever is in the input window
		writes the passed argument to the window if anything
		otherwise prints the carot and then waits for a string
		accepts strings up to 80 characters long
		turns of echo and returns the string gotten
		"""
		curses.echo()
		self.input_win.erase()
		self.input_win.addstr(0, 1, comment, curses.color_pair(5))
		self.input_win.addstr(2, 1, '->', curses.color_pair(2))
		self.input_win.refresh()
		text = self.input_win.getstr(2, 4, 80)
		curses.noecho()
		return text

	def terminal_size(self):
		"""
		validates that the terminal is a large enough size to play 
		the game in curses
		"""
#        rows, columns = os.popen('stty size', 'r').read().split()
		try:
			rows, columns = subprocess.check_output(['stty','size']).decode().split()
			if int(rows) >= int(MIN_ROWS) and int(columns) >= int(MIN_COLS):
				return True 
			return False
		except Exception:
			return False

	def init_colors(self):
		"""
		initializes some colors pairs for curses to be used when printing text
		"""
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
	
	def print_help(self):
		"""
			prints the actual help menu
			in curses in the main window
		"""
		self.main_win.erase()
		x, y = self.print_text(4,2,"Verb       ", curses.A_BOLD)
		x, y = self.print_text(x,y,"::", curses.color_pair(2))
		x, y = self.print_text(x,y,"  Explanation of verb usage")
		for key in VERB_DICT:
			y += 2
			x = 4
			self.print_text(x,y,key, curses.A_BOLD)
			self.print_text(15,y,"::",  curses.color_pair(2))
			self.print_text(19,y,VERB_DICT[key])
	
	def roll_credits(self):
		"""
			prints the final credits
			in curses in the main window
		"""
		credits =["DESLOATE JOURNEY", "Created by Team Pavo", "Emily Caveness", "Alexander Laquitara", "Johannes Pikel" ]
		self.main_win.erase()
		x, y = self.print_text(4,2,"Credits      ", curses.A_BOLD)
		
		for key in credits:
			y += 2
			x = 25
			self.print_text(x,y,key, curses.A_BOLD)
		self.write_main_artifact(PAVO)

	def print_text(self, x, y, text, attribute=None):
		"""
			a helper function to the print_help function to make the curses help
			menu seem like it is being typed one letter at a time
			prints the text into the window given and refreshes
		"""
		for ch in text:
			if attribute == None:
				self.main_win.addstr(int(y),int(x),ch)
			else:
				self.main_win.addstr(int(y),int(x),ch, attribute)
			x+=1
			time.sleep(random.uniform(0.03, 0.005))
			self.main_win.refresh()
		return x, y
	
	#------------------------------------------------------
	#This ends the UI curses section
	#------------------------------------------------------

