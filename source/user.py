#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import util
import json
from singleton import Singleton


""": Description of what this file does."""
__author__      = "Kan Yuan"
__copyright__   = "Copyright 2015, Cry Little Kan"
__version__     = "0.1"


NL = '\n'

class User(Singleton):
	def __init__(self):
		if hasattr(self, '_init'):
			return

		if os.path.isfile(util.Constant.like_file):
			with open(util.Constant.like_file, "r") as fd:
				self._like = json.load(fd)
		else:
			self._like = set()

		if os.path.isfile(util.Constant.hate_file):
			with open(util.Constant.hate_file, "r") as fd:
				self._hate = json.load(fd)
		else:
			self._hate = set()

	def like(self, song):
		if song in self._like:
			return
		else:
			self._like.add(song)
			json.dump(self._like, open(util.Constant.like_file, "w"))

	def dislike(self, song):
		if song not in self._like:
			return
		else:
			self._like.remove(song)
			json.dump(self._like, open(util.Constant.like_file, "w"))

	def hate(self, song):
		if song not in self._hate:
			return
		else:
			self._hate.remove(song)
			json.dump(self._hate, open(util.Constant.hate_file, "w"))

	def unhate(self, song):
		if song not in self._hate:
			return
		else:
			self._like.remove(song)
			json.dump(self._hate, open(util.Constant.hate_file, "w"))
