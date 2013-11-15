#!/usr/bin/env python3
"""A CLI to Movies2HDD"""

#	Copyright (C) 2013 Niklas Sombert

#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
