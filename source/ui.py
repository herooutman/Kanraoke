#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import terminalsize

"""curses_util.py: Description of what this file does."""
__author__	  = "Kan Yuan"
__copyright__   = "Copyright 2016, Cry Little Kan"
__version__	 = "0.1"


class Ui():
	def __init__(self):
		self.screen = curses.initscr()
		self.screen.timeout(100)  # the screen refresh every 100ms
		# character break buffer
		curses.cbreak()
		self.screen.keypad(1)
		curses.start_color()
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		# term resize handling
		size = terminalsize.get_terminal_size()
		self.x = max(size[0], 10)
		self.y = max(size[1], 25)
		self.startcol = int(float(self.x) / 5)
		self.indented_startcol = max(self.startcol - 3, 0)
		self.update_space()

	def display_list(self, datatype, title, datalist, offset, page, step, START):
		curses.noecho()
		self.screen.move(5, 1)
		self.screen.clrtobot()
		self.screen.addstr(5, self.startcol, title, curses.color_pair(1))

		if len(datalist) == 0:
			self.screen.addstr(8, self.startcol, '这里什么都没有 -，-')
		else:
			if datatype == 'main':
				for i in range(0, min(len(datalist) - page * step, step)):
					if i == offset:
						self.screen.addstr(i + 8, self.indented_startcol, '-> ' + str((i + 1) % 10) + '. ' + datalist[page * step + i], curses.color_pair(2))
					else:
						self.screen.addstr(i + 9, self.startcol, str((i + 1) % 10) + '. ' + datalist[page * step + i])

	def update_size(self):
		# get terminal size
		size = terminalsize.get_terminal_size()
		self.x = max(size[0], 10)
		self.y = max(size[1], 25)

		# update intendations
		curses.resizeterm(self.y, self.x)
		self.startcol = int(float(self.x) / 5)
		self.indented_startcol = max(self.startcol - 3, 0)
		self.update_space()
		self.screen.clear()
		self.screen.refresh()


	def update_space(self):
		if self.x > 140:
			self.space = "   -   "
		elif self.x > 80:
			self.space = "  -  "
		else:
			self.space = " - "
		self.screen.refresh()
