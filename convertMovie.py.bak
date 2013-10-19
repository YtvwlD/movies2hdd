#! /usr/bin/env python
print "Loading libraries..."
from movies2hdd import Movies2HDD
import sys
import shutil
movie = sys.argv[1]
print "Moving "+movie+" to /tmp ..."
shutil.move(movie, "/tmp/")
print "Converting it..."
movie = movie.replace(".ts", "")
Movies2HDD.convertMovie(Movies2HDD(), movie)
print "Moving "+movie+".mpg back..."
shutil.move("/tmp/"+movie+".mpg", ".")
