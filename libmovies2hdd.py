#!/usr/bin/env python
def load():
	import ftplib
	return

def connect(host, user, pass):
	conn = ftplib.FTP()
	print(conn.connect(host))
	print(conn.login(user, pass))
	print(conn.cwd("/media/hdd/movie"))
	return conn

def disconnect(conn):
	print(conn.quit())
	return

