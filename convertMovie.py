#! /usr/bin/env python
print "Loading libraries..."
import libmovies2hdd
import sys
import shutil
movie = sys.argv[1]
print "Moving "+movie+" to /tmp ..."
shutil.move(movie, "/tmp/")
print "Converting it..."
movie = movie.replace(".ts", "")
libmovies2hdd.convertMovie(movie)
print "Moving "+movie+".mpg back..."
shutil.move("/tmp/"+movie+".mpg", ".")
