# encoding: UTF-8
import os
import sys
import termios
import fcntl
from signal import SIGINT
from shutil import copyfile

class Constant:
	DEBUG = False
	M_PLAYER = 0
	M_KARAOKE = 1
	main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
	print main_dir
	lib_dir = os.path.join(main_dir, "library")
	db_lib_file = os.path.join(lib_dir, 'kanraoke.db')
	lib_file = os.path.join(main_dir, 'lib.json')
	like_file = os.path.join(main_dir, 'like.json')
	hate_file = os.path.join(main_dir, 'hate.json')
	cache_dir = os.path.join(main_dir, "cache")
	mkv_src = "/Volumes/Seagate Backup Plus Drive/MKV"
	new_mkv_src = "/Volumes/Seagate Backup Plus Drive/MKV Update"

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

class color:
	def __init__(self, c):
		self._c = c.lower()

	def __enter__(self):
		if self._c == "red":
			sys.stdout.write(bcolors.FAIL)
		elif self._c == "blue":
			sys.stdout.write(bcolors.OKBLUE)
		elif self._c == "green":
			sys.stdout.write(bcolors.OKGREEN)
		elif self._c == "yellow":
			sys.stdout.write(bcolors.WARNING)
		elif self._c == "bold":
			sys.stdout.write(bcolors.BOLD)
		elif self._c == "underline":
			sys.stdout.write(bcolors.UNDERLINE)
		elif self._c == "pink":
			sys.stdout.write(bcolors.HEADER)
		else:
			self._c = None

	def __exit__(self, type, value, traceback):
		if self._c:
			sys.stdout.write(bcolors.ENDC)

def debug_print(*args):
	if Constant.DEBUG:
		print " ".join(map(lambda x: str(x), args))


def search_cache(f):
	for root, directories, filenames in os.walk(Constant.cache_dir):
		for filename in filenames:
			if filename == f:
				return os.path.join(root, filename)
	return None

def copy_to_cache(src_dir, f, outname):
	fsrc = os.path.join(src_dir, f)
	fdst = os.path.join(Constant.cache_dir, outname)
	if os.path.isfile(fsrc):
		copyfile(fsrc, fdst)
		return fdst
	else:
		return None

def find_getch():
	try:
		import termios
	except ImportError:
		# Non-POSIX. Return msvcrt's (Windows') getch.
		import msvcrt
		return msvcrt.getch

	# POSIX system. Create and return a getch that manipulates the tty.
	import sys
	import tty

	def _getch():
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			ret = sys.stdin.read(1)
		except KeyboardInterrupt:
			print "keyborad interrupt"
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ret
	return _getch

def getch(msg=None):
	if msg:
		sys.stdout.write(msg)
	fun = find_getch()
	return fun()


def add_to_playlist(player, song):
	song_idx = song['id']
	loc = str(song["loc"])
	src_dir, f = os.path.split(loc)
	outname = "%s-%s-[%s]-%d.MKV" % (song["name"], "&".join(song["artists"]), song["lang"], song_idx)

	path = search_cache(f)
	if not path:
		path = copy_to_cache(src_dir, f, outname)
	if path:
		player.enqueue(str(path))
		player.play()
		return True
	else:
		return False

def read_single_keypress(msg=None):
	"""Waits for a single keypress on stdin.

	This is a silly function to call if you need to do it a lot because it has
	to store stdin's current setup, setup stdin for reading single keystrokes
	then read the single keystroke then revert stdin back after reading the
	keystroke.

	Returns the character of the key that was pressed (zero on
	KeyboardInterrupt which can happen when a signal gets handled)

	"""
	if msg:
		sys.stdout.write(msg)
	fd = sys.stdin.fileno()
	# save old state
	flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
	attrs_save = termios.tcgetattr(fd)
	# make raw - the way to do this comes from the termios(3) man page.
	attrs = list(attrs_save) # copy the stored version to update
	# iflag
	attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
				  | termios.ISTRIP | termios.INLCR | termios. IGNCR
				  | termios.ICRNL | termios.IXON )
	# oflag
	attrs[1] &= ~termios.OPOST
	# cflag
	attrs[2] &= ~(termios.CSIZE | termios. PARENB)
	attrs[2] |= termios.CS8
	# lflag
	attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
				  | termios.ISIG | termios.IEXTEN)
	termios.tcsetattr(fd, termios.TCSANOW, attrs)
	# turn off non-blocking
	fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
	# read a single keystroke
	try:
		ret = sys.stdin.read(1) # returns a single character
	except KeyboardInterrupt:
		ret = '\x03'
	finally:
		# restore old state
		termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
		fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
	if ret == '\x03':
		os.kill(os.getpid(), SIGINT)
	return ret


def text_width(text):
	import re
	add_len = 0
	patten = u"[\u3000-\u30ff\u4e00-\u9fa5\ufb00-\ufffd]+"
	res = re.findall(patten, text)
	for t in res:
		add_len += len(t)
	return len(text) + add_len

def readline(msg):
	try:
		targ = raw_input(msg)
		return targ
	except KeyboardInterrupt:
		print "Cancelled"
