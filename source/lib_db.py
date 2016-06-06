#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite
from singleton import Singleton
from util import Constant
from util import text_width

class Library(Singleton):

	def __init__(self):
		if hasattr(self, '_init'):
			return
		self._init = True
		self.__db = None
		self.__load_lib()

	def __load_lib(self):
		self.__db = sqlite.connect(Constant.db_lib_file)

	def browse(self):
		return sqlite.browse(self.__db)

	def search_artist(self, query):
		return sqlite.search_artist(self.__db, query)

	def search_song(self, query):
		return sqlite.search_song(self.__db, query)

	def get_song_by_artist(self, aid):
		return sqlite.get_song_by_artist(self.__db, aid)

	@staticmethod
	def display_items(items, operation_type):
		if operation_type == "song":
			pass
		elif operation_type == "artist":
			pass
		elif operation_type == "menu":
			pass

# FIXME: to be moved to menu

	@staticmethod
	def display_song(song, prefix=None):
		SONG_WIDTH = 36
		ARTIST_WIDTH = 16
		LANG_WIDTH = 4
		SPACE = 2
		name = song["name"]
		ntw = text_width(name)
		if ntw > SONG_WIDTH - SPACE:
			name += "..."
		while ntw > SONG_WIDTH - SPACE:
			name = name[:-4] + "..."
			ntw = text_width(name)


		artists = '/'.join(song["artists"])
		atw = text_width(artists)
		if atw > ARTIST_WIDTH - SPACE:
			artists += "..."
		while atw > ARTIST_WIDTH - SPACE:
			artists = artists[:-4] + "..."
			atw = text_width(artists)

		lang = song["lang"]
		time = song["time"]

		if prefix is not None:
			print str(prefix) + ". " + "".join((name.ljust(SONG_WIDTH-ntw+len(name)), artists.ljust(ARTIST_WIDTH-atw+len(artists)), lang.ljust(LANG_WIDTH), time))
		else:
			print "\t".join((song["name"], '/'.join(song["artists"]), song["lang"], song["time"]))

	@staticmethod
	def display_artist(artist, prefix=None):
		if prefix is not None:
			print str(prefix) + ". " + "\t".join((artist["name"], "%d songs" % artist["song_number"]))
		else:
			print "\t".join((artist["name"], "%d songs" % artist["song_number"]))
