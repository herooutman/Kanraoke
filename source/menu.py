#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import util
import math
import sys
from time import sleep
from vlc import VLC
from lib_db import Library
from user import User
from sound import Sound
from util import color
from util import readline
from util import read_single_keypress as getch
# from util import getch
# from getch import _Getch

class Menu():
	def __init__(self):
		self.const = util.Constant()
		self.player = VLC()
		self.lib = Library()
		self.user = User()
		self.sound = Sound()

	def start(self):
		while True:
			with color("blue"):
				print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
				print  """        __ __                             __      """
				print  """       / //_/___ _____  _________ _____  / /_____ """
				print  """      / ,< / __ `/ __ \/ ___/ __ `/ __ \/ //_/ _ \\"""
				print  """     / /| / /_/ / / / / /  / /_/ / /_/ / ,< /  __/"""
				print  """    /_/ |_\__,_/_/ /_/_/   \__,_/\____/_/|_|\___/ """
				print  """                                                  """
				print
			with color('yellow'):
				print "输入首字母搜索   (B)浏览歌曲   (V)原唱/伴唱   (N)下一首   (P)暂停/继续"
			print "\n\n\n\n"
			cmd = readline("Kanraoke > ")
			cmd = cmd.strip()
			if cmd:
				if cmd == "quit" or cmd == "q":
					break
				else:
					self._process_cmd(cmd)


	# def alert(self, msg):
	# 	if platform.system() == 'Darwin':
	# 		os.system('/usr/bin/osascript -e \'display notification "Karaoke open..."sound name "/System/Library/Sounds/Ping.aiff"\'')

	# def start_fork(self):
	# 	pid = os.fork()
	# 	if pid == 0:
	# 		Menu().alert("")
	# 	else:
	# 		Menu().start()

	def _process_cmd(self, cmd):
		cmd = re.sub('\s+', ' ', cmd)
		parts = cmd.split(" ")
		cmd = parts[0]
		if len(parts) > 1:
			params = parts[1:]
		else:
			params = None
		if cmd == "clear":
			self._clear_list()
		elif cmd == "next" or cmd == "n":
			self._next()
		elif cmd == "browse" or cmd == "b":
			self._browse()
		elif cmd == "pause" or cmd == "p":
			self._pause()
		elif cmd == "full" or cmd == "f":
			self._full(params)
		elif cmd == "vocal" or cmd == "v":
			self._vocal(params)
		elif cmd == "laugh" or cmd == "l":
			self._laugh()
		elif cmd == "woo" or cmd == "w":
			self._woo()
		elif cmd == "applause" or cmd == "a":
			self._applause()
		elif cmd == "replay" or cmd == "r":
			self._replay()
		elif cmd == "s" or cmd == "search":
			self._search(params)
		else:
			self._search([cmd])

	def _full(self, param):
		if param:
			param = " ".join(param).strip().lower()
			if param == "on":
				self.player.fullscn()
			elif param == "off":
				self.player.fullscn(False)
		else:
			self.player.fullscn()

	def _vocal(self, param):
		if param:
			param = " ".join(param).strip().lower()
			if param == "on":
				self.player.change_atrack(1)
			elif param == "off":
				self.player.change_atrack(2)
		else:
			self.player.change_atrack(None)

	def _laugh(self):
		self.sound.laugh()

	def _applause(self):
		self.sound.applause()

	def _woo(self):
		self.sound.woo()

	def _next(self):
		self.player.next()

	def _pause(self):
		self.player.pause()

	def _replay(self):
		self.player.replay()

	def _clear_list(self):
		while True:
			resp = getch("Are you sure to clear the list? [Y/N] ")
			resp = resp.lower()
			print
			if resp == "y":
				self.player.clear()
				return
			elif resp == "n":
				return

	def _browse(self):
		songs = self.lib.browse()
		return self.display_list(songs, "song")

	def _search(self, param):
		if param:
			param = " ".join(param).strip()
			items = [("搜索歌曲", self._search_song), ("搜索歌手", self._search_artist)]
			self.display_list(items, "menu", param)

	def _search_artist(self, param):
		artists = self.lib.search_artist(param)
		return self.display_list(artists, "artist")
		# if artist:
		# 	name = artist["name"]
		# 	songs = self.lib.get_song_by_artist(name)
		# 	song = Menu.display_list(songs, "song")
		# 	if song:
		# 		loc = str(song["loc"])
		# 		src_dir, f = os.path.split(loc)
		# 		self.player.add_to_playlist(src_dir, f)
				# src_dir, f = os.path.split(loc)
				# self.player.add_to_playlist(src_dir, f)

	def _search_song(self, param):
		songs = self.lib.search_song(param)
		return self.display_list(songs, "song")

	@staticmethod
	def display_menu(item, prefix):
		if prefix is not None:
			print str(prefix) + ". " + item[0]
		else:
			print item[0]

	def display_list(self, l, operation_type, param=None):
		if l:
			size = len(l)
			max_page = int(math.ceil(size / 10.0))
			page = 0
			to_main = False
			while not to_main:
				if operation_type == "menu":
					print "===================="
				else:
					print "\n"*50+"========= PAGE: %d/%d ===========" % (page+1, max_page)
				for i in range(10):
					if page * 10 + i >= size:
						break
					item = l[page * 10 + i]
					prefix = i + 1 if i < 9 else 0
					if operation_type == "song":
						Library.display_song(item, prefix)
					elif operation_type == "artist":
						Library.display_artist(item, prefix)
					elif operation_type == "menu":
						Menu.display_menu(item, prefix)
				print "===================="
				print "(Nums)选择   (N)下一页   (P)上一页   (B)后退   (M)主菜单\n"
				valid_selection = False
				sys.stdout.write("please select > ")
				while not valid_selection:
					select = getch()
					if select == "b":
						return
					if select == "m":
						return True
					elif select == "n":
						new_page = min(page + 1, max_page - 1)
						if page != new_page:
							page = new_page
							valid_selection = True
						continue
					elif select == "p":
						new_page = max(page - 1, 0)
						if page != new_page:
							page = new_page
							valid_selection = True
						continue
					elif select.isdigit():
						choice_str = select
						select = int(select)
						select = select - 1 if select > 0 else 9
						idx = page * 10 + select
						if idx < size:
							res = l[idx]
							print choice_str
							to_main = self._select(res, operation_type, param)
							valid_selection = True
						else:
							continue
					else:
						pass
			return True
		else:
			with color("pink"):
				print "\n"
				print "\tMMMMMMMMMMMMMMMMMMMMMWNK0kxdooooooodxk0XNWMMMMMMMMMMMMMMMMMM"
				print "\tMMMMMMMMMMMMMMMWWNKkoc;'...............,:lx0NWMMMMMMMMMMMMMM"
				print "\tMMMMMMMMMMMMWNX0d:'.........................;lkXWMMMMMMMMMMM"
				print "\tMMMMMMMMMMWNKkl,........,:clodddddooc:,'.......;d0WMMMMMMMMM"
				print "\tMMMMMMMMWXKkc'......;ldOKXXXXXXXXXXXXXKOxl;......'l0WMMMMMMM"
				print "\tMMMMMMWXKOo'.....'lkKXXXXXXXXXXXXXXXXXXXXXKko;.....,dXMMMMMM"
				print "\tMMMMWNX0k:.....,oOXXXXXXXXXXXXXXXXK0KXXXXXXXX0d;.....:0WMMMM"
				print "\tMMMWNK0x;.....cOXXXXXXK00XXXXXXXKx:':xKXXXXXXXX0o,....,kWMMM"
				print "\tMMMNKKk;....'oKXXXXXXKo,,lOXXXNX0l....:xKXXXXXXXXk:....'xWMM"
				print "\tMMNKKO:....'dKXXXXXXKo...,xXXXXXXKx;....:kKXXXXXXXOc....,OWM"
				print "\tMWKK0o.....oKXXXXXX0l...'dKXXXXXXXX0l'....ckKXXXXXXO:....:KM"
				print "\tWXKKk;....:0XXXXXX0c....lKXXXXXXXXXXKk:....'oKXXXXXXk,....dN"
				print "\tWXKKd'....dXXXXXXO:....c0XXXXXXXXXXXXX0o,..'xXXXXXXXKl....:K"
				print "\tNKK0l....,kXXXXXXOc...;OXXXXXXXXXXXXXXXXOc;dKXXXXXXXXx'...'k"
				print "\tNKK0l....;OXXXXXXX0d,,xXXXXXXXXXXXXXXXXXXK0XXXXXXXXXXk;....d"
				print "\tNKK0l....;OXXXXXXXXXOOXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXO;....o"
				print "\tNKK0o....'xXXXXXXXXXXXXXXXXXKKK00OOkkxddollclkXXXXXXXk,....d"
				print "\tWKKKx,....lKXXXXXXXOdoollc::;,,,''..........'xXXXXXXXd....'k"
				print "\tWXKKOc....;kXXXXXXXx'.......................;OXXXXXX0:....:K"
				print "\tMNKK0x,....c0XXXXXXKl.....';::ccllloddc.....lKXXXXXKd.....xW"
				print "\tMWXKK0l.....l0XXXXXXk,....l0XXXXXXXXXXx'....dXXXXXXx,....cXM"
				print "\tMMWXKKOc.....cOXXXXXKo....;OXXXXXXXXXXx'...,kXXXXKd,....;0WM"
				print "\tMMMWXKKOl.....;xKXXXXO:....dXXXXXXXXXXd....:0XXX0l'....;OWMM"
				print "\tMMMMWXKK0o'.....ckKXXXd'...:0XXXXXXXXXd....lKX0d;.....:0WMMM"
				print "\tMMMMMWNKK0x:......:d0X0c...'dXXXXXXXXXo...'dOo;.....'oXMMMMM"
				print "\tMMMMMMMWNKKOd;......,cdl'...c0XXXXXXXXo....,'......c0WMMMMMM"
				print "\tMMMMMMMMMWXKKOd:............'lxxkkxxdl;.........'lONMMMMMMMM"
				print "\tMMMMMMMMMMMWNXK0xl;..........................':dKWMMMMMMMMMM"
				print "\tMMMMMMMMMMMMMMWNXX0koc;'.................':lxKNMMMMMMMMMMMMM"
				print "\tMMMMMMMMMMMMMMMMMWWNNXKOkdolc:::::cclodkOXNWMMMMMMMMMMMMMMMM"
				print "\tMMMMMMMMMMMMMMMMMMMMMMMWWWWWNNNNNNWWMMMMMMMMMMMMMMMMMMMMMMMM"
				print "\n"
			getch("It seems your query does not match any record in our library, press ENTER to continue...  ")
			return

	def _select(self, selection, t, param):
		if t == "song":
			song = selection
			if song and util.add_to_playlist(self.player, song):
				with color('yellow'):
					sys.stdout.write("\nSong added: ")
					Library.display_song(song)
					print
					sleep(.5)
			else:
				print "Song not found!"
		elif t == "artist":
			artist = selection
			if artist:
				aid = artist["id"]
				songs = self.lib.get_song_by_artist(aid)
				return self.display_list(songs, "song")
		elif t == "menu":
			if selection:
				return selection[1](param)
