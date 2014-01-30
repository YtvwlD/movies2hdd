#!/usr/bin/env python3
'''A line-based interface to Movies2HDD.'''

print ("Movies2HDD's line-based interface Copyright (C) 2013 Niklas Sombert")
print ("This program comes with ABSOLUTELY NO WARRANTY.")
print ("This is free software, and you are welcome to redistribute it")
print ("under certain conditions.")

print ("")

print ("Loading libraries...")
import movies2hdd
Movies2HDD = movies2hdd.Movies2HDD()
from getpass import getpass
import sys
if sys.version_info.major == 2:
	ask = raw_input
elif sys.version_info.major == 3:
	ask = input
else:
	print ("What version of Python are you using?!")
	quit()
print ("")

print ("Movies2HDD")
def connect():
	print ("Connect to your DreamBox")
	host = ask("Host: ")
	user = ask("User: ")
	print ("Your password will be sent unencryptedly!!!")
	print ("Don't do this if you don't trust this network.")
	print ("Otherwise, please tunnel this connection via SSH.")
	pwd = getpass("Password: ")
	print ("Connecting...")
	Movies2HDD.connect(host, user, pwd)
#
def disconnect():
	print ("Disconnecting...")
	Movies2HDD.disconnect()
#
def search():
	print ("Search for movies")
	search = ask("Search for: ")
	print ("")
	result = Movies2HDD.getAviableMovies(search)
	print ("The following movies were found:")
	i = 0
	for x in result:
		i += 1
		print ("	[" + str(i) + "] " + x)
	print ("")
	print ("Which of them do you want to download?")
	print ("Please type in the numbers and seperate them with a ',' (e.g. '1,5,7,42,1234').")
	selection_input = ask("> ")
	movies_to_get = []
	for x in selection_input.split(","):
		x = int(x)-1
		movies_to_get.append(result[x])
	print ("")
	print ("The following movies are selected to be downloaded:")
	for x in movies_to_get:
		print ("	* " + x)
	movies = movies_to_get
#
def select():
	pass
	#filetype = ?
#
def save():
	print ("Where do you want to save the movies?")
	path = ask("> ")
	#do something
#
def download():
	pass
	#filetype = "ts"
#
def rename():
	pass
#
def convert():
	if filetype == "ts":
		for x in movies:
			Movies2HDD.convertMovie(x)
	elif filetype == "mpg":
		print ("The files are already .mpg.")
	else:
		print ("What?!")
		print ("... file type are you using?")
		quit()
#
def quit():
	print ("Exiting...")
	sys.exit()
#
while True:
	print ("")
	print ("What do you want to do next?")
	print ("	[1] Connect to your DreamBox")
	print ("	[2] Disconnect from your DreamBox")
	print ("	[3] Search for movies (needs a connection)")
	print ("	[4] Select movies from your disk (not implemented yet!)")
	print ("	[5] Save movies to your disk (needs a list of movies)")
	print ("	[6] Download movies (needs a connection and a list of movies)")
	print ("	[7] Rename movies (needs a list of movies)")
	print ("	[8] Convert movies (needs a list of movies)")
	print ("	[9] Quit (disconnect first!)")
	print ("")
	answer = int(ask("> "))
	print ("")
	if answer == 1:
		connect()
	if answer == 2:
		disconnect()
	if answer == 3:
		search()
	if answer == 4:
		select()
	if answer == 5:
		save()
	if answer == 6:
		download()
	if answer == 7:
		rename()
	if answer == 8:
		convert()
	if answer == 9:
		quit()
