#!/usr/bin/env python
import ftplib
import urllib
from xml.dom.minidom import parseString

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
