#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import pypinyin
import re
from copy import copy
from copy import deepcopy
from singleton import Singleton
from util import Constant
# from snownlp import SnowNLP
# from pypinyin import pinyin, load_phrases_dict
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Library(Singleton):

	def __init__(self):
		if hasattr(self, '_init'):
			return
		self._init = True
		self.lib = None
		self.load_lib()

	def load_lib(self):
		if os.path.isfile(Constant.lib_file):
			with open(Constant.lib_file, 'r') as fd:
				self.lib = json.load(fd)
		else:
			self.lib = self._build_lib(self)

	def _build_lib(self):
		raw_input("press any key")
		return None

	def search(self, query):
		pass

	def browse(self):
		res = []
		for idx, song in enumerate(self.lib["songs"]):
			res.append((copy(song), idx))
		return res

	def search_song(self, query):
		res = []
		start = Library.binary_search(query, self.lib["songs_idx"])
		for idx_entry in self.lib["songs_idx"][start:]:
			name, init, idx = idx_entry
			if init.startswith(query):
				res.append((copy(self.lib["songs"][idx]), idx))
			else:
				break
		return res

	def search_artist(self, query):
		res = []
		start = Library.binary_search(query, self.lib["artists_idx"])
		for idx_entry in self.lib["artists_idx"][start:]:
			if idx_entry[1].startswith(query):
				res.append(self.lib["artists_dict"][idx_entry[0]])
			else:
				break
		return res

	@staticmethod
	def binary_search(query, l):
		n = len(l)
		start = 0
		end = n - 1
		while end >= start:
			mid = (end + start) / 2
			m = l[mid][1]
			if m > query:
				end = mid - 1
				continue
			elif m < query:
				start = mid + 1
				continue
			else:
				while l[mid-1][1] == query:
					mid -= 1
				return mid
		return mid


	def build_index(self):
		self.lib["artists_idx"] = []
		for a in self.lib["artists"]:
			if a["index"]:
				self.lib["artists_idx"].append((a["name"], a["index"]))
		self.lib["artists_idx"].sort(key=lambda x: x[1])
		# for a in self.lib["artists_idx"]:
			# print a[0], a[1]

		self.lib["songs_idx"] = []
		for idx, a in enumerate(self.lib["songs"]):
			if a["index"]:
				self.lib["songs_idx"].append((a["name"], a["index"], idx))
		self.lib["songs_idx"].sort(key=lambda x: x[1])
		json.dump(self.lib, open(Constant.lib_file, "w"))


	@staticmethod
	def get_artist_score(artist):
		black = [u"群星", u"佚名", u"no name", u"影视金曲", u"恰恰舞曲", u"歌唱舞曲", u"舞曲"]
		if artist["name"] in black:
			return 0
		else:
			return len(artist["songs"])

	def rank_artists(self):
		self.lib["artists"].sort(key=lambda x: Library.get_artist_score(x))
		self.lib["artists"].reverse()
		# json.dump(self.lib, open(Constant.lib_file, "w"))

	def get_song_by_artist(self, artist):
		a = self.lib["artists_dict"].get(artist, None)
		if a:
			return [(self.get_song_by_idx(song), song) for song in a["songs"]]
		else:
			return None

	@staticmethod
	def display_song(song, prefix=None):
		if prefix is not None:
			print str(prefix) + ". " + "\t".join((song["name"], '/'.join(song["artist"]), song["lang"], song["time"]))
		else:
			print "\t".join((song["name"], '/'.join(song["artist"]), song["lang"], song["time"]))

	@staticmethod
	def display_artist(artist, prefix=None):
		if prefix is not None:
			print str(prefix) + ". " + "\t".join((artist["name"], "%d songs" % len(artist["songs"])))
		else:
			print "\t".join((artist["name"], "%d songs" % len(artist["songs"])))

	def get_artist(self, artist):
		artist = unicode(artist)
		return self.lib["artists_dict"].get(artist, None)

	def get_song_by_idx(self, idx):
		return self.lib["songs"][idx]

	@staticmethod
	def search_new_songs():
		songs = []
		for root, directories, filenames in os.walk(Constant.new_mkv_src):
			for filename in filenames:
				if filename.lower().endswith(".ksc"):
					song = {}
					try:
						with open(os.path.join(root, filename), 'r') as fd:
							for idx, line in enumerate(fd):
								line = line.strip()
								if line.startswith("karaoke.tag"):
									line = line.decode('gbk').encode('utf-8')
									pair = line.split("', '")
									k = pair[0][13:]
									v = pair[1][:-3]
									if k == '歌名':
										song["name"] = v
									elif k == '歌手':
										song["artist"] = v
									elif k == '语种':
										song["lang"] = v
									elif k == '时间':
										song["time"] = v
								elif line.startswith("karaoke.CommonVideo"):
									song["loc"] = line.split(":= '")[1][:-2].decode('gbk').encode('utf-8')
									song["loc"] = os.path.join(root, song["loc"])
						if song and os.path.isfile(song["loc"]):
							songs.append(song)
						else:
							print song["name"] + "\t" + song["loc"] + " missing"
					except Exception, e:
						pass
		with open("/Users/Xiaokang/Documents/karaoke/new_songs.json", "w") as fd:
			json.dump(songs, fd)


	@staticmethod
	def get_index(line):
		line = unicode(line)
		line = line.replace('0', ' 0 ')
		line = line.replace('1', ' 1 ')
		line = line.replace('2', ' 2 ')
		line = line.replace('3', ' 3 ')
		line = line.replace('4', ' 4 ')
		line = line.replace('5', ' 5 ')
		line = line.replace('6', ' 6 ')
		line = line.replace('7', ' 7 ')
		line = line.replace('8', ' 8 ')
		line = line.replace('9', ' 9 ')

		line = line.replace('-', ' ')
		line = line.replace('.', ' ')
		line = line.replace('!', ' ')
		line = re.sub(r"\s+", r" ", line)
		parts = line.split(" ")
		initials = []
		index = ""

		for part in parts:
			if part:
				part = SnowNLP(part).words
				i = pinyin(part, heteronym=False, style=pypinyin.FIRST_LETTER)
				initials += i
		for i in initials:
			if re.match(r"[a-zA-z0-9]", i[0][0]):
				i[0] = i[0][0]
		for i in initials:
			if re.match(r'^[a-zA-Z0-9]$', i[0]):
				index += i[0]
		return index

	@staticmethod
	def search_old_songs():
		with open("/Users/Xiaokang/Documents/karaoke/SONG.txt", 'r') as fd:
			songs = []
			for idx, line in enumerate(fd):
				song = {}
				line = line.strip()
				if line:
					fields = line.split('||')
					name = fields[0]
					artist = fields[1]
					lang = fields[2]

					words = fields[5]
					time = fields[11]
					filename = os.path.join(Constant.mkv_src, fields[12])
					if os.path.isfile(filename):
						song["name"] = name
						song["artist"] = artist
						song["lang"] = lang
						song["words"] = words
						song["time"] = time
						song["loc"] = filename
					else:
						print name + "\t" + filename + " missing"
				if song:
					song["rank"] = len(songs)
					songs.append(song)
		with open("/Users/Xiaokang/Documents/karaoke/old_songs.json", "w") as fd:
			json.dump(songs, fd)

	@staticmethod
	def build_artists(lib):
		with open("/Users/Xiaokang/Documents/karaoke/artists") as fd:
			for idx, line in enumerate(fd):
				artist = {}
				line = line.strip()
				if line:
					line = unicode(line)
					artist['songs'] = []
					artist['name'] = line
					line = line.replace('0', ' 0 ')
					line = line.replace('1', ' 1 ')
					line = line.replace('2', ' 2 ')
					line = line.replace('3', ' 3 ')
					line = line.replace('4', ' 4 ')
					line = line.replace('5', ' 5 ')
					line = line.replace('6', ' 6 ')
					line = line.replace('7', ' 7 ')
					line = line.replace('8', ' 8 ')
					line = line.replace('9', ' 9 ')

					line = line.replace('-', ' ')
					line = line.replace('.', ' ')
					line = line.replace('!', ' ')
					# line = line.replace('`', "'")
					line = re.sub(r"\s+", r" ", line)
					parts = line.split(" ")
					initials = []
					index = ""

					load_phrases_dict({u'乐队': [[u'yúe'], [u'dui']]})
					for part in parts:
						if part:
							part = SnowNLP(part).words
							i = pinyin(part, heteronym=False, style=pypinyin.FIRST_LETTER)
							initials += i
					for i in initials:
						# if len(i) > 1:
						# 	print initials, artist
						# if re.match(r"^[a-zA-Z][a-zA-Z'`]+$", i[0]):
							# i[0] = i[0][0]
						if re.match(r"[a-zA-z0-9]", i[0][0]):
							i[0] = i[0][0]
					# product = reduce(lambda x,y: x*y, [len(i) for i in initials])
					# # print product
					# if product > 1:
					# 	print artist, initials
					for i in initials:

						if re.match(r'^[a-zA-Z0-9]$', i[0]):
							index += i[0]
						# else:
							# print line, i
					if index:
						artist["index"] = index
					elif artist:
						artist["index"] = ''
				if artist:
					lib['artists'].append(artist)
					lib['artists_dict'][artist["name"]] = artist
		# with open("/Users/Xiaokang/Documents/karaoke/artists.json", "w") as fd:
		# 	json.dump(artists, fd)

	@staticmethod
	def parse_new_songs(lib):
		with open("/Users/Xiaokang/Documents/karaoke/artists.json", "r") as fd:
			artists = json.load(fd)
			artist_set = [a["name"].strip() for a in artists]
			artist_set = set(artist_set)

		with open("/Users/Xiaokang/Documents/karaoke/new_songs.json", "r") as fd:
			songs = json.load(fd)
			for song in songs:
				song_idx = len(lib["songs"])
				lib["songs"].append(song)
				lang = song["lang"]
				if lang == "其他" or lang == "法语":
					song["lang"] = "其它"
				elif lang == "台语":
					song["lang"] = "闽南语"
				elif lang == "台语":
					song["lang"] = "闽南语"

				song["name"] = song["name"].split("-")[0]
				song["words"] = len(song["name"])

				########  get artists
				artist = song["artist"].lower()
				artist = re.sub(r"\([^\)\(]+\)", "", artist)
				parsed_artists = []
				if artist in artist_set:
					parsed_artists.append(artist)
				else:
					parts = re.split(r"[_&^]", artist)
					for part in parts:
						if part:
							if part in artist_set:
								parsed_artists.append(part)
								continue

							else:
								parts2 = part.split(" ")
								for part2 in parts2:
									if part2 and part2 in artist_set:
										parsed_artists.append(part2)

				parsed_artists = [unicode(x) for x in parsed_artists]
				for a in parsed_artists:
					# print lib['artists_dict'].keys()
					# raw_input("press any key")
					art_entry = lib['artists_dict'].get(a, None)
					if art_entry:
						art_entry["songs"].append(song_idx)
					else:
						print a
						print type(a)
						print [a]
						raw_input("press any key")

				song["artist"] = parsed_artists

				song["index"] = Library.get_index(song["name"]).lower()

				song["rank"] = 20000

	@staticmethod
	def parse_old_songs(lib):
		with open("/Users/Xiaokang/Documents/karaoke/artists.json", "r") as fd:
			artists = json.load(fd)
			artist_set = [a["name"].strip() for a in artists]
			artist_set = set(artist_set)
		with open("/Users/Xiaokang/Documents/karaoke/artists_small", "r") as fd:
			small_artists = []
			for idx, line in enumerate(fd):
				line = line.strip()
				small_artists.append(line)
		with open("/Users/Xiaokang/Documents/karaoke/old_songs.json", "r") as fd:
			songs = json.load(fd)
			for song in songs:
				song_idx = len(lib["songs"])
				lib["songs"].append(song)
				# song["name"] = song["name"].split("-")[0]
				song["words"] = int(song["words"])

				lang = song["lang"]
				if lang == "0":
					song["lang"] = u"国语"
				elif lang == "1":
					song["lang"] = u"粤语"
				elif lang == "2":
					song["lang"] = u"闽南语"
				elif lang == "3":
					song["lang"] = u"英语"
				elif lang == "4":
					song["lang"] = u"日语"
				elif lang == "5":
					song["lang"] = u"韩语"
				else:
					song["lang"] = u"其它"

				#### get artists
				artist = song["artist"].lower()
				artist = re.sub(r"\([^\)\(]+\)", "", artist)
				parsed_artists = []

				if artist in artist_set:
					parsed_artists.append(artist)
				else:
					remains = artist
					for sa in small_artists:
						if sa in remains:
							parsed_artists.append(sa)
							remains = remains.replace(sa, "")
							remains = remains.strip()

					if remains:
						parts = re.split(r"[_&^+]|vs", remains)
						for part in parts:
							if part:
								if part in artist_set:
									parsed_artists.append(part)
									continue
								if remains in artist_set:
									parsed_artists.append(remains)
								else:
									parts = remains.split(" ")
									for part in parts:
										if part and part in artist_set:
											parsed_artists.append(part)
				parsed_artists = [unicode(x) for x in parsed_artists]
				for a in parsed_artists:
					art_entry = lib['artists_dict'].get(a, None)
					if art_entry:
						art_entry["songs"].append(song_idx)
					else:
						print a
						print type(a)
						print [a]
						raw_input("press any key")
				song["artist"] = parsed_artists

				song["index"] = Library.get_index(song["name"]).lower()

	# @staticmethod
	# def parse_songs():

# Library.search_new_songs()


# lib = {}
# lib["songs"] = []
# lib["artists"] = []
# lib['artists_dict'] = {}
# Library.build_artists(lib)
# Library.parse_old_songs(lib)
# Library.parse_new_songs(lib)
# json.dump(lib, open(Constant.lib_file, "w"))

# l = Library()
# l.rank_artists()
# l.build_index()
