#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite
from singleton import Singleton
from util import Constant

class Library(Singleton):

	def __init__(self):
		if hasattr(self, '_init'):
			return
		self._init = True
		self.__db = None
		self.__load_lib()

	def __load_lib(self):
		self.__db = sqlite.connect(Constant.db_lib_file)


import json

if os.path.isfile(Constant.db_lib_file):
	db = sqlite.connect(Constant.db_lib_file)
else:
	db = sqlite.connect(Constant.db_lib_file)
	sqlite.init_lib(db)
with open(Constant.lib_file, "r") as fd:
	old_lib = json.load(fd)
	artists = old_lib["artists"]
	songs = old_lib["songs"]

	# sqlite.insert_songs(db, songs)
	# sqlite.insert_artists(db, artists, songs)

	sqlite.test(db)