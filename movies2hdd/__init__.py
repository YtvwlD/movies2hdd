#!/usr/bin/env python3
"""A library to work with movies on a DreamBox."""

#	Copyright (C) 2013 Niklas Sombert

#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Lesser General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Lesser General Public License for more details.
#
#	You should have received a copy of the GNU Lesser General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ftplib
import urllib
try:
	import urllib.request #Python 3
except ImportError:
	pass
from xml.dom.minidom import parseString
import subprocess
import os

class Movies2HDD:
	"""A simple set of python scripts and libraries to work with movies. I use it with my DreamBox."""

	def __init__(self):
		"""The __init__. What else?"""
		pass

	def connect(self, host, user, pwd):
		"""Connect to a DreamBox using the given host and credentials."""
		self.conn = ftplib.FTP()
		print((self.conn.connect(host)))
		print((self.conn.login(user, pwd)))
		print((self.conn.cwd("/media/hdd/movie")))
		#return conn

	def disconnect(self):
		"""Close the connection."""
		print((self.conn.quit()))
		return

	def getAviableMovies(self,search):
		"""List movies aviable on your DreamBox."""
		allfiles = self.conn.nlst()
		newlist = list()
		for each in allfiles:
			if each.find(search) != -1:
				newlist.append(each)
		movies = list()
		for each in newlist:
			if each.endswith(".ts"):
				movies.append(each.replace(".ts", ""))
		return movies
	
	def getTitleOfEpisode(self, movie):
		"""Get the title of an episode. It uses the .ts.meta file that are automatically stored with your recordings."""
		meta = list()
		self.conn.retrlines("RETR "+movie+".ts.meta", meta.append)
		if meta[1] == meta[2]:
			return False #Titel wurde nicht bei der Aufnahme gespeichert
		else:
			return meta[2]

	def getSeries(self, series):
		"""Get the id of the series."""
		try:
			api = urllib.urlopen("http://thetvdb.com/api/GetSeries.php?seriesname="+series)
		except AttributeError:
			api = urllib.request.urlopen("http://thetvdb.com/api/GetSeries.php?seriesname="+series)
		apianswer = api.read()
		api.close()

		series = []
		seriesdom = parseString(apianswer).getElementsByTagName("Data")[0].getElementsByTagName("Series")
		for x in seriesdom:
			seriesid = x.getElementsByTagName("seriesid")[0].firstChild.data
			seriesname = x.getElementsByTagName("SeriesName")[0].firstChild.data
			try:
				overview = x.getElementsByTagName("Overview")[0].firstChild.data
			except IndexError:
				overview = ""
			series.append({
				'seriesid': seriesid,
				'SeriesName': seriesname,
				'Overview': overview
			})
		
		return(series)
	
	def getPositionOfEpisode(self, series, episode):
		"""Get the season and episode number of an episode."""
		lang = "de" #german #or perhaps as a parameter
		#search doesn't always work
		try:
			apianswer = urllib.urlopen("http://thetvdb.com/api/GetSeries.php?seriesname="+series).read()
		except AttributeError:
			apianswer = urllib.request.urlopen("http://thetvdb.com/api/GetSeries.php?seriesname="+series).read()

		sid = parseString(apianswer).getElementsByTagName("Data")[0].getElementsByTagName("Series")[0].getElementsByTagName("seriesid")[0].firstChild.data #seriesid
		if series == "Castle":
			sid = 83462
		try:
			apianswer = urllib.urlopen("http://thetvdb.com/api/FE84E205C6E3D916/series/"+str(sid)+"/all/"+lang+".xml").read()
		except AttributeError:
			apianswer = urllib.request.urlopen("http://thetvdb.com/api/FE84E205C6E3D916/series/"+str(sid)+"/all/"+lang+".xml").read()
	#	dom = parseString(txt)
	#	dom = dom.getElementsByTagName("Data")[0]
		dom = parseString(apianswer).getElementsByTagName("Data")[0]
		episodes = dom.getElementsByTagName("Episode")
		season = 0
		for x in episodes:
			if x.getElementsByTagName("EpisodeName")[0].firstChild.data == episode:
				episode = x.getElementsByTagName("Combined_episodenumber")[0].firstChild.data
				season = x.getElementsByTagName("Combined_season")[0].firstChild.data
				if episode.find(".") != -1:
					episode = episode[0:episode.find(".")]
		if (episode.isdigit()):
			return [int(season), int(episode)]
		else:
			return False

	def downloadMovie(self, movie):
		"""Download a video from your DreamBox."""
		file = open("/tmp/"+movie+".ts", "wb")
		result = self.conn.retrbinary("RETR "+movie+".ts", file.write, 8*1024) #perhaps implement threading ;-)
		print(result)
		file.close()
		if result.startswith("2") == False:
			raise BaseException
		else:
			print("TODO")
			#print(self.conn.delete(movie)) #TODO

	def convertMovie(self, movie):
		"""Convert a movie. It will remove additional audio tracks!"""
		if subprocess.Popen(["projectx", "/tmp/"+movie+".ts"]).wait() != 0: #threading?
			raise BaseException
		files = os.listdir("/tmp")
		contents = list()
		for x in files:
			print("There is "+x+".")
			if x.startswith(movie):
				print("It belongs to us! "+x)
				#if x.find("[") == -1 and x.find("_log") == -1 and x.find(".ts") == -1:
					#contents.append(x[x.index("."):x.count("")-1])
				if x.endswith(".ac3"):
					contents.append(".ac3")
					print(x+" is in.")
				elif x.endswith(".mp2") and x.find("[") == -1:
					contents.append(".mp2")
					print(x+" is in.")
				elif x.endswith(".m2v"):
					contents.append(".m2v")
					print(x+" is in.")
				elif x.endswith(".ts"):
					contents.append(".ts")
					print(x+" will not be deleted for now.")
				else:
					os.remove("/tmp/"+x)
					print(x+" removed.")
		print("We have got the following files:")
		print(contents)
		if contents.count(".m2v") != 0:
			if contents.count(".ac3") != 0:
				if subprocess.Popen(["mplex","-f","3","-o","/tmp/"+movie+".mpg","/tmp/"+movie+".ac3","/tmp/"+movie+".m2v"]).wait() != 0: #threading?
					raise BaseException
			elif contents.count(".mp2") != 0:
				if subprocess.Popen(["mplex","-f","3","-o","/tmp/"+movie+".mpg","/tmp/"+movie+".mp2","/tmp/"+movie+".m2v"]).wait() != 0: #threading?
					raise BaseException
			else:
				print("No audio in here.")
				#return False
				raise BaseException
		else:
			print("No video in here.")
			#return False
			raise BaseException
		for x in contents:
			print("deleting "+movie+x+"...")
			os.remove("/tmp/"+movie+x)
