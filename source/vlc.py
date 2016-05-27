#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import telnetlib
import os
import socket
import util
from singleton import Singleton
from subprocess import Popen


""": Description of what this file does."""
__author__      = "Kan Yuan"
__copyright__   = "Copyright 2015, Cry Little Kan"
__version__     = "0.1"


NL = '\n'

class VLC(Singleton):
	def __init__(self, mode=util.Constant.M_KARAOKE):
		if hasattr(self, '_init'):
			return
		self._init = True
		self._conn = None
		self._mode = mode

	@staticmethod
	def create_player(mode):
		with open(os.devnull, "w") as nullfile:
			if mode == util.Constant.M_KARAOKE:
				Popen("/Applications/VLC.app/Contents/MacOS/VLC --audio-track 1".split(), stderr=nullfile, stdout=nullfile)
			elif mode == util.Constant.M_PLAYER:
				Popen("/Applications/VLC.app/Contents/MacOS/VLC".split(), stderr=nullfile, stdout=nullfile)
		# os.system("/Applications/VLC.app/Contents/MacOS/VLC")
		# Popen(["open", "-g", "-W", "/Applications/Utilities/Terminal.app", "/Applications/VLC.app/Contents/MacOS/VLC"])
		# Popen(["open", "-g", "-W", "/Applications/VLC.app/Contents/MacOS/VLC"])

	def connect(self):
		hostserver = '127.0.0.1'
		hostport = '9221'
		password = 'monsteroke'

		try:
			self._conn = telnetlib.Telnet(hostserver, hostport)
			msg = self._conn.read_until('Password: ')
			util.debug_print("[Kanraoke] rec: " + msg)
			self._send_cmd(password)
			return True
		except socket.error:
			retry = 3
			VLC.create_player(self._mode)
			while retry > 0:
				time.sleep(.5)
				retry -= 1
				try:
					self._conn = telnetlib.Telnet(hostserver, hostport)
					msg = self._conn.read_until('Password: ')
					util.debug_print("[Kanraoke] rec: " + msg)
					self._send_cmd(password)
					return True
				except socket.error:
					pass
			return False

	def initial_player(self):
		msg = self._send_cmd("is_playing").strip()
		if msg == "0":
			# self.clear()
			pass
		# self.fullscn()

	def _send_cmd(self, cmd):
		self._conn.write(cmd + NL)
		util.debug_print("[Kanraoke] send: " + cmd)
		msg = self._conn.read_until('> ')
		util.debug_print("[Kanraoke] rec: " + msg)
		return msg[:-3]

	def _disconnect(self):
		if self._conn:
			self._send_cmd("shutdown")
			self._conn.close()
			self._conn = None

	def enqueue(self, f):
		self._send_cmd("enqueue " + f)

	def clear(self):
		self._send_cmd("clear")

	def play(self):
		self._send_cmd("play")

	def replay(self):
		self._send_cmd("seek 0")

	def next(self):
		self._send_cmd('next')

	def pause(self):
		self._send_cmd('pause')

	def _get_list(self):
		self._send_cmd('pause')

	def change_atrack(self, track):
		if track is not None:
			self._send_cmd('atrack ' + str(track))
		else:
			res = self._send_cmd('atrack')
			lines = [l.strip() for l in res.split("\n")]
			for line in lines:
				if line.endswith("*"):
					curr = line[2]
					if curr == '1':
						self._send_cmd('atrack 2')
					else:
						self._send_cmd('atrack 1')

	def fullscn(self, mode=True):
		if mode:
			self._send_cmd('f on')
		else:
			self._send_cmd('f off')