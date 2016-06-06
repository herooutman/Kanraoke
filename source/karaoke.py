#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import signal
import vlc
import argparse
from util import Constant
from lib import Library
from menu import Menu
# from menu_curses import Menu
# from util import Constant, search_cache

""": Description of what this file does."""
__author__      = "Kan Yuan"
__copyright__   = "Copyright 2015, Cry Little Kan"
__version__     = "0.1"


work_dir, program_name = os.path.split(sys.argv[0])
if '.' in program_name:
	program_name = '.'.join(program_name.split('.')[:-1])
logfile = os.path.join(work_dir, program_name + ".log")


def main():
	opt = argparse.ArgumentParser(description="Kan's Karaoke system.")
	opt.add_argument("-p", "--player", action="store_true", help="Music Player Mode")
	options = opt.parse_args()

	if options.player:
		player = vlc.VLC(Constant.M_PLAYER)
	else:
		player = vlc.VLC()
	print "Connecting to the player."
	connected = player.connect()
	if connected:
		print "Player connected."
		player.initial_player()
		print "Loading library."
		Library()
		signal.signal(signal.SIGINT, send_kill)
		menu = Menu()
		menu.start()
	else:
		print "Cannot connect to the player..."
		return

def send_kill(signum, fram):
	print
	print "exit."
	sys.exit()

if __name__ == '__main__':
	main()
