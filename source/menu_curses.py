#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vlc
import util
import time
import sys
import locale
import signal
import curses
from lib import Library
from ui import Ui
# from getch import _Getch

locale.setlocale(locale.LC_ALL, "")

class Menu():
	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('utf8')
		self.const = util.Constant()
		self.datalist = ['搜索歌曲', '搜索艺术家']
		self.datatype = 'main'
		self.lib = Library()
		self.offset = 0
		self.page = 0
		self.player = vlc.VLC()
		self.START = time.time()
		self.step = 10
		self.title = 'KANraoke'
		self.screen = curses.initscr()
		self.ui = Ui()
		signal.signal(signal.SIGWINCH, self.change_term)
		signal.signal(signal.SIGINT, self.send_kill)

	def change_term(self, signum, frame):
		self.screen.clear()
		self.screen.refresh()

	def send_kill(self, signum, fram):
		curses.endwin()
		sys.exit()

	def start(self):
		self.ui.display_list(self.datatype, self.title, self.datalist, self.offset, self.page, self.step, self.START)
		while True:
			self.screen.timeout(500)
			key = self.screen.getch()
			# key = self.screen.getkey()
			# if key != -1:
			# 	print key
			self.screen.refresh()

			# break
			# if key == -1:
				# self.ui.update_size()
			self.ui.display_list(self.datatype, self.title, self.datalist, self.offset, self.page, self.step, self.START)
		pass
