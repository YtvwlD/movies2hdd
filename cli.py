#!/usr/bin/env python3
"""A CLI to Movies2HDD"""
print("Loading libraries...")
from movies2hdd import Movies2HDD
movies2hdd = Movies2HDD()
#implement a command line parser
import argparse


parser = argparse.ArgumentParser(description="A command line interface to Movies2HDD.")
parser.add_argument("command", metavar="command", type=str, help="The command to execute.")
args = parser.parse_args()
#print (args.command)

if args.command == "help":
	print("The aviable commands are:")
	print(" * convert [path to movie]	Converts the movie from .ts to .mpg. It removes additional audio tracks!")
	print(" * ")

if args.command == "convert":
	import sys
	import shutil
	movie = sys.argv[1]
	print("Moving "+movie+" to /tmp ...")
	shutil.move(movie, "/tmp/")
	print("Converting it...")
	movie = movie.replace(".ts", "")
	Movies2HDD.convertMovie(Movies2HDD(), movie)
	print("Moving "+movie+".mpg back...")
	shutil.move("/tmp/"+movie+".mpg", ".")

