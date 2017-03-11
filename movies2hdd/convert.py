"""A simple script to convert a movie. It uses the movies2hdd library."""

print ("Movies2HDD's convertMovie tool Copyright (C) 2013-2017 Niklas Sombert")
print ("This program comes with ABSOLUTELY NO WARRANTY.")
print ("This is free software, and you are welcome to redistribute it")
print ("under certain conditions.")

print ("")

print ("This is _deprecated_! It will be removed when other components are ready to be used...")

print ("")

print("Loading libraries...")
from movies2hdd import Movies2HDD
import shutil

def run(args):
	movie = args.movie
	print("Moving "+movie+" to /tmp ...")
	shutil.move(movie, "/tmp/")
	print("Converting it...")
	movie = movie.replace(".ts", "")
	Movies2HDD.convertMovie(Movies2HDD(), movie)
	print("Moving "+movie+".mpg back...")
	shutil.move("/tmp/"+movie+".mpg", ".")
