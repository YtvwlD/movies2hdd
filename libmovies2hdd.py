#!/usr/bin/env python
import ftplib
import urllib
from xml.dom.minidom import parseString
import subprocess
import os

def connect(host, user, pwd):
	conn = ftplib.FTP()
	print(conn.connect(host))
	print(conn.login(user, pwd))
	print(conn.cwd("/media/hdd/movie"))
	return conn

def disconnect(conn):
	print(conn.quit())
	return

def getAviableMovies(conn,search):
	allfiles = conn.nlst()
	newlist = list()
	for each in allfiles:
		if each.find(search) != -1:
			newlist.append(each)
	movies = list()
	for each in newlist:
		if each.endswith(".ts"):
			movies.append(each.rstrip(".ts"))
	return movies

def getTitleOfEpisode(conn, movie):
	meta = list()
	conn.retrlines("RETR "+movie+".ts.meta", meta.append)
	if meta[1] == meta[2]:
		return False #Titel wurde nicht bei der Aufnahme gespeichert
	else:
		return meta[2]

def getPositionOfEpisode(series, episode):
	lang = "de" #german
	#search doesn't always work
	sid = parseString(urllib.urlopen("http://thetvdb.com/api/GetSeries.php?seriesname="+series).read()).getElementsByTagName("Data")[0].getElementsByTagName("Series")[0].getElementsByTagName("seriesid")[0].firstChild.data #seriesid
	if series == "Castle":
		sid = 83462
#	txt = urllib.urlopen("http://thetvdb.com/api/FE84E205C6E3D916/series/"+str(sid)+"/all/"+lang+".xml").read()
#	dom = parseString(txt)
#	dom = dom.getElementsByTagName("Data")[0]
	dom = parseString(urllib.urlopen("http://thetvdb.com/api/FE84E205C6E3D916/series/"+str(sid)+"/all/"+lang+".xml").read()).getElementsByTagName("Data")[0]
	episodes = dom.getElementsByTagName("Episode")
	for x in episodes:
		if x.getElementsByTagName("EpisodeName")[0].firstChild.data == episode:
			episode = x.getElementsByTagName("Combined_episodenumber")[0].firstChild.data
			season = x.getElementsByTagName("Combined_season")[0].firstChild.data
			if episode.find(".") != -1:
				episode = episode[0:episode.find(".")]
	return [int(season), int(episode)]

def downloadMovie(conn, movie):
	file = open("/tmp/"+movie+".ts", "wb")
	conn.retrbinary("RETR "+movie+".ts", file.write, 8*1024) #perhaps implement threading ;-)
	file.close()

def convertMovie(movie, path):
	subprocess.Popen(["projectx", "/tmp/"+movie+".ts"]).wait() #threading?
	files = os.listdir("/tmp")
	contents = list()
	for x in files:
		if x.find(movie) != -1:
			contents.append(x[x.index("."):x.count("")-1])
	if contents.count(".m2v") != 0:
		if contents.count(".ac3") != 0:
			subprocess.Popen(["mplex","-f","3","-o",path+".mpg",movie+".ac3",movie+".m2v"]).wait() #threading?
		elif contents.count(".mp2") != 0:
			subprocess.Popen(["mplex","-f","3","-o",path+".mpg",movie+".mp2",movie+".m2v"]).wait() #threading?
		else:
			print "No audio in here."
			return False
	else:
		print "No video in here."
		return False
	os.remove("/tmp/"+movie+".ts")
	for x in contents:
		os.remove("/tmp/"+movie+x)
