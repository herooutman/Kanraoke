#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import sys
import os
import json
from util import Constant
reload(sys)
sys.setdefaultencoding('utf8')

def connect(dbfile):
	if os.path.isfile(Constant.db_lib_file):
		return sqlite3.connect(dbfile)
	else:
		db = sqlite3.connect(Constant.db_lib_file)
		init_lib(db)
		return db

def close(conn):
	conn.close()

def commit(conn, sql, para=None):
	c = conn.cursor()
	if para:
		c.execute(sql, para)
	else:
		c.execute(sql)
	conn.commit()
	return c

def commit_many(conn, sql, para=None):
	c = conn.cursor()
	if para:
		c.executemany(sql, para)
	else:
		c.execute(sql)
	conn.commit()


def query(conn, sql, para=None):
	c = conn.cursor()
	if para:
		c.execute(sql, para)
	else:
		c.execute(sql)
	return c

def init_lib(conn):
	# create song table
	sql = """CREATE TABLE song (id INTEGER PRIMARY KEY, name TEXT, loc TEXT NOT NULL UNIQUE, artists TEXT, initials TEXT, rank INTEGER, words INTEGER, lang TEXT, time TEXT)"""
	commit(conn, sql)
	sql = """CREATE TABLE artist (id INTEGER PRIMARY KEY, name TEXT, initials TEXT, song_number INTEGER)"""
	commit(conn, sql)
	sql = """CREATE TABLE sing (id INTEGER PRIMARY KEY, sid INTEGER NOT NULL, aid INTEGER NOT NULL, UNIQUE(sid, aid) ON CONFLICT IGNORE)"""
	commit(conn, sql)
	with open(Constant.lib_file, "r") as fd:
		old_lib = json.load(fd)
		artists = old_lib["artists"]
		songs = old_lib["songs"]
		insert_songs(conn, songs)
		insert_artists(conn, artists, songs)


def wrap_song(song):
	lang = song.get('lang', '')
	loc = song.get('loc', None)
	name = song.get('name', '')
	artists = song.get('artist', '')
	artists = "###".join(artists)
	initials = song.get('index', '')
	rank = song.get('rank', 9999999)
	words = song.get('words', len(name))
	time = song.get('time', '')
	if not loc:
		raw_input("what the heck")
	else:
		return (name, loc, artists, initials, rank, words, lang, time)

def wrap_songs(songs):
	return [wrap_song(song) for song in songs]

def wrap_artist(artist):
	initials = artist.get('index', '')
	name = artist.get('name', '')
	songs = artist.get('songs', None)
	if not songs:
		# raw_input("empty artist: " + name)
		return None
	else:
		return initials, name, songs

def unwrap_songs(songs):
	return [unwrap_song(song) for song in songs]

def unwrap_song(song):
	sid, name, loc, artists, initials, rank, words, lang, time = song
	ret = dict()
	ret['id'] = sid
	ret['lang'] = lang
	ret['loc'] = loc
	ret['name'] = name
	ret['artists'] = artists.split("###")
	ret['initials'] = initials
	ret['rank'] = rank
	ret['words'] = words
	ret['time'] = time
	return ret

def unwrap_artists(artists):
	return [unwrap_artist(artist) for artist in artists]

def unwrap_artist(artist):
	aid, name, initials, song_number = artist
	ret = dict()
	ret['id'] = aid
	ret['name'] = name
	ret['initials'] = initials
	ret['song_number'] = song_number
	return ret

def insert_song(conn, song):
	para = wrap_song(song)
	sql = """INSERT OR IGNORE INTO song(name, loc, artists, initials, rank, words, lang, time) VALUES (?,?,?,?,?,?,?,?)"""
	commit(conn, sql, para)

def insert_songs(conn, songs):
	para = wrap_songs(songs)
	sql = """INSERT OR IGNORE INTO song(name, loc, artists, initials, rank, words, lang, time) VALUES (?,?,?,?,?,?,?,?)"""
	commit_many(conn, sql, para)

def insert_artist(conn, artist, songs):
	t = wrap_artist(artist)
	if not t:
		return
	initials, name, artist_songs = t
	sql = """INSERT OR IGNORE INTO artist(name, initials, song_number) VALUES (?,?,?)"""
	c = commit(conn, sql, (name, initials, len(artist_songs)))
	aid = c.lastrowid
	for s_idx in artist_songs:
		song = songs[s_idx]
		loc = song['loc']
		sql = """SELECT id FROM song WHERE loc = ?"""
		res = commit(conn, sql, (loc,)).fetchall()
		if not res:
			raw_input("SONG not found at location: %s" % loc)
		else:
			for sid in res:
				insert_sing(conn, sid[0], aid)

def insert_artists(conn, artists, songs):
	for artist in artists:
		insert_artist(conn, artist, songs)

def insert_sing(conn, sid, aid):
	sql = """INSERT INTO sing(sid, aid) VALUES (?,?)"""
	commit(conn, sql, (sid, aid))

def list_table(conn):
	sql = """SELECT * FROM sqlite_master WHERE type='table'"""
	return query(conn, sql)

def table_info(conn):
	sql = """PRAGMA table_info(song)"""
	return query(conn, sql)

def list_songs(conn):
	sql = """SELECT * FROM song ORDER BY initials"""
	return query(conn, sql)

def browse(conn):
	sql = """SELECT * FROM song ORDER BY initials"""
	c = query(conn, sql)
	songs = c.fetchall()
	return unwrap_songs(songs)

def search_artist(conn, q):
	sql = """SELECT * FROM artist WHERE initials LIKE '""" + q + """%'"""
	c = query(conn, sql)
	artists = c.fetchall()
	return unwrap_artists(artists)

def search_song(conn, q):
	sql = """SELECT * FROM song WHERE song.initials LIKE '""" + q + """%'  ORDER BY song.words, song.rank"""
	c = query(conn, sql)
	songs = c.fetchall()
	return unwrap_songs(songs)

def get_song_by_artist(conn, aid):
	sql = """SELECT song.* FROM sing, song WHERE aid = ? AND sing.sid = song.id ORDER BY song.words, song.rank"""

	c = query(conn, sql, (str(aid), ))
	songs = c.fetchall()
	return unwrap_songs(songs)

def test(conn):
	sql = "SELECT song.* FROM artist, sing, song WHERE artist.initials LIKE '%s' AND artist.id = sing.aid and sing.sid = song.id" % 'ldh%'
	print sql
	c = query(conn, sql)
	songs = c.fetchall()
	for song in songs:
		print song
