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
	season = 0
	for x in episodes:
		if x.getElementsByTagName("EpisodeName")[0].firstChild.data == episode:
			episode = x.getElementsByTagName("Combined_episodenumber")[0].firstChild.data
			season = x.getElementsByTagName("Combined_season")[0].firstChild.data
			if episode.find(".") != -1:
				episode = episode[0:episode.find(".")]
	return [int(season), int(episode)]

def downloadMovie(conn, movie):
	file = open("/tmp/"+movie+".ts", "wb")
	result = conn.retrbinary("RETR "+movie+".ts", file.write, 8*1024) #perhaps implement threading ;-)
	print result
	file.close()
	if result.startswith("2") == False:
		raise BaseException
	else:
		print "TODO"
		#print(conn.delete(movie)) #TODO

def convertMovie(movie):
	if subprocess.Popen(["projectx", "/tmp/"+movie+".ts"]).wait() != 0: #threading?
		raise BaseException
	files = os.listdir("/tmp")
	contents = list()
	for x in files:
		print "There is "+x+"."
		if x.startswith(movie):
			print "It belongs to us! "+x
			#if x.find("[") == -1 and x.find("_log") == -1 and x.find(".ts") == -1:
				#contents.append(x[x.index("."):x.count("")-1])
			if x.endswith(".ac3"):
				contents.append(".ac3")
				print x+" is in."
			elif x.endswith(".mp2"):
				contents.append(".mp2")
				print x+" is in."
			elif x.endswith(".m2v"):
				contents.append(".m2v")
				print x+" is in."
			else:
				os.remove("/tmp/"+x)
				print x+" removed."
	print "We have got the following files:"
	print contents
	if contents.count(".m2v") != 0:
		if contents.count(".ac3") != 0:
			if subprocess.Popen(["mplex","-f","3","-o","/tmp/"+movie+".mpg","/tmp/"+movie+".ac3","/tmp/"+movie+".m2v"]).wait() != 0: #threading?
				raise BaseException
		elif contents.count(".mp2") != 0:
			if subprocess.Popen(["mplex","-f","3","-o","/tmp/"+movie+".mpg","/tmp/"+movie+".mp2","/tmp/"+movie+".m2v"]).wait() != 0: #threading?
				raise BaseException
		else:
			print "No audio in here."
			#return False
			raise BaseException
	else:
		print "No video in here."
		#return False
		raise BaseException
	for x in contents:
		print "deleting "+movie+x+"..."
		os.remove("/tmp/"+movie+x)
