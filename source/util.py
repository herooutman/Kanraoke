# encoding: UTF-8
import os
import sys
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
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
	return _getch
getch = find_getch()


def add_to_playlist(player, song):
	song_idx = song[1]
	song = song[0]
	loc = str(song["loc"])
	src_dir, f = os.path.split(loc)
	outname = "%s-%s-[%s]-%d.MKV" % (song["name"], "&".join(song["artist"]), song["lang"], song_idx)

	path = search_cache(f)
	if not path:
		path = copy_to_cache(src_dir, f, outname)
	if path:
		player.enqueue(str(path))
		player.play()
		return True
	else:
		return False
