#!/usr/bin/env python
# -*- coding: utf-8 -*-
from singleton import Singleton
from util import Constant
import subprocess
import os
import threading


""": Description of what this file does."""
__author__      = "Kan Yuan"
__copyright__   = "Copyright 2015, Cry Little Kan"
__version__     = "0.1"

class Sound(Singleton):
	laugh_file = os.path.join(Constant.main_dir, "resource/laughter.mp3")
	applause_file = os.path.join(Constant.main_dir, "resource/applause.mp3")
	woo_file = os.path.join(Constant.main_dir, "resource/woo.mp3")

	def __init__(self):
		if hasattr(self, '_init'):
			return
		self._t = None

	def laugh(self):
		self._start_thread(self.t_laugh)

	def t_laugh(self):
		# os.spawnl(os.P_NOWAIT, "afplay " + Sound.laugh_file)
		return_code = subprocess.call(["afplay", Sound.laugh_file])
		# return return_code

	def woo(self):
		self._start_thread(self.t_woo)

	def t_woo(self):
		return_code = subprocess.call(["afplay", Sound.woo_file])

	def applause(self):
		self._start_thread(self.t_applause)

	def t_applause(self):
		return_code = subprocess.call(["afplay", Sound.applause_file])

	def _start_thread(self, fun):
		self._t = threading.Thread(target=fun)
		self._t.start()
