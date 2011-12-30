#!/usr/bin/python
#--------------------------------------------------------------------------------------------------------
# Program: 	parseXbmcLibrary
# Function: 	Find missing video files in the Xbmc library. Based on a specified folder and a library
# 		export file (videodb.xml, exported from the "Settings->Video" menu in Xbmc), the program
#		returns a list of the files that are in 
#--------------------------------------------------------------------------------------------------------

import os
import sqlite3
from shutil import copyfile

#Global vars
dbFile 			= "/home/mistercrunch/.xbmc/userdata/Database/MyVideos34.db" 	#location of the library exported file
videoPath 		= "/home/mistercrunch/Videos"		#folder to scan for video files
fileExtention 		= ['avi', 'mpg', 'mkv', 'mov'] 		# only check files with these extensions
excludeFileIfContains 	= ['sample']				#won't consider filename containing these words
excludeDirIfContains	= ['zizik', 'camera video', 'perso']

#List that will contain all full paths to video from the library
videoLibFileList = []  
copyfile(dbFile, dbFile + ".tmp")
conn = sqlite3.connect(dbFile + ".tmp")
cur = conn.cursor() 
sql = 	"""
	select strPath || +  strFilename
	from files  a
	inner join path b on a.idPath = b.idPath;
	"""
videoLibFileList = [f[0] for f in cur.execute(sql) ] 


#Building file system file list from filesystem
fileList = []			
for root, dirs, files in os.walk(videoPath):
    for name in files:
	if name.split('.').pop().lower() in fileExtention:
		if (not any(s in name.lower() for s in excludeFileIfContains)) and (not any(s in root.lower() for s in excludeDirIfContains)):
			fileList.append(unicode(root+"/"+name, 'Latin-1')) 
	
#Finding missing files (in the file system, but not in the library)
missingFiles = [f for f in fileList if f not in videoLibFileList]

def PrintStats():
	print "---------------------------------------"
	print "Stats"
	print "---------------------------------------"
	print "Number of files in folder(s): " + str(len(fileList))
	print "Number of files in library: " + str(len(videoLibFileList))
	print "Number of missing files: " + str(len(missingFiles))
	print ""

def PrintMissingFiles():
	print "---------------------------------------"
	print "List of missing files"
	print "---------------------------------------"
	missingFiles.sort()
	for f in missingFiles:
		print f.encode('Latin-1')

PrintStats()
PrintMissingFiles()

