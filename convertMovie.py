#! /usr/bin/env python
import libmovies2hdd
import sys
import shutil
movie = sys.argv[0]
shutil.move(movie, "/tmp/")
libmovies2hdd.convertMovie(movie.strip(".ts"))
shutil.move("/tmp/"+movie+".mpg" + ".")
