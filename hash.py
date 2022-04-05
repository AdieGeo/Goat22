# !/usr/bin/python3

import os
import hashlib
import datetime 

#print("Adie")

#This program must have a current log file to run as of rn. Maybe try adding try and except blocks. 

#This is for saving the the information into a file. I open the file and write to it.

#First open current file log and read all the hashes out
oldhashes=[]
oldfiles = []
try:
	f = open("filelog.txt", "r")
	oldlogs = f.readlines()
	for line in oldlogs:
		#print(line)
		line=line.split("   ")
		oldfilename = line [0]
		oldhash = line[1]
		#print(oldhash)
		oldfiles.append("oldfilename")
		oldhashes.append("oldhash")
	#Now rename the file log to old file log so that new filelog can be generated. 
	os.rename("filelog.txt", "oldfilelog.txt")
except:
	print("No current log exists, so we're generating a starting one")	

#Set up the summary return info
newfilelist = []
missingfilelist = []
modifiedfilelist = []


f = open("filelog.txt", "a+")

Unhashables = ["dev", "proc", "run", "sys", "tmp", "var/lib", "var/run"]    #This is a list of the unhashables that I will check against 

#The following section of code does some of Part 1 of the lab, and was taken from Python documentation on Os.Walk. This snippiet of code was taken specfically from tuorials point. 
#Cite: https://www.tutorialspoint.com/python/os_walk.htm
#I then modified the code snippet to take out the unhashables and actually do the hashes. 

for (root, dirs, files) in os.walk("/"):
	for name in files:
		for unhashable in Unhashables:
			if unhashable in os.path.join(root, name): 	#Skippig the files who contain an unhashablein it.
				#print("I've been skipped")				#How I verified everything worked. 
				continue
			else:
				#The following section of code was taken from the python documentation on hashlib
				#Cite: https://docs.python.org/3/library/hashlib.html
				stringtohash=str(os.path.join(root, name))
				if stringtohash not in oldfiles:
					newfilelist.append(stringtohash)  	#Seeing if this is a new file or not 
				bytestohash = bytes(stringtohash, 'utf-8')
				h=hashlib.new('sha256')
				h.update(bytestohash)
				#print (h.hexdigest())
				f.write(stringtohash + "    " + str(h.hexdigest()) + "   " + str(datetime.datetime.now()) + "\n")
	for name in dirs:
		for unhashable in Unhashables:
			if unhashable in os.path.join(root, name):
				continue
			else:
				stringtohash=str(os.path.join(root, name))
				if stringtohash not in oldfiles:
					newfilelist.append(stringtohash)
				bytestohash = bytes(stringtohash, 'utf-8')
				h=hashlib.new('sha256')
				h.update(bytestohash)
				#print (h.hexdigest())
				f.write(stringtohash + "    " + str(h.hexdigest()) + "   " + str(datetime.datetime.now()) + "\n")
				
#f.close()
try:
	currentlogsfile = []
	currenthashes = []
	#Doing this to find any missing files				
	#f = open("filelog.txt", "r")
	logs = f.readlines()
	for line in logs:
		#print(line)
		line=line.split("   ")
		logname = line [0]
		loghash = line[1]
		#print(oldhash)
		currentlogsfile.append("logname")
		currenthashes.append("loghash")
	for filename in oldfiles:			#if a file used to exist and no longer does add it to missing list. 
		if filename not in currenlogsfile:
			missingfilelist.append(filename)
		
	hashestocheck = []
	#Gotta figure out modified files still. Probs gonna do this via hashes.
	for eachhash in currenthashes:
		if eachhash not in oldhashes:
			#This means either a newfile or a modifed one
			hashestocheck.append(eachhash)
	for eachfile in currentlogfiles:
		if eachfile in newfilelist:	#if it's a new file  then it's not modified. 
			continue
		else:				#file either modifed or not
			bytestohash = bytes(eachfile, 'utf-8')
			h=hashlib.new('sha256')
			h.update(bytestohash)
			computedhash = h.hexdigest()
			if computedhash not in oldhashes: 	#if the computed has is in the oldhashes file then file is not modified
				modifiedfilelist.append(eachfile)

	print("Summary")
	print("New files added since last time we checked: " + str(newfilelist))
	print("Missing files that are no longer on the system: " + str(missingfilelist))
	print("These files have been modified since last time we checked: " + str(modifiedfilelist))
		
except:
	print("Summary")
	print("All files are new")
	print("No files are missing")
	print("Nothing has been modified")
			
f.close()

#Now I have a list with the path for everything. I need to skip the unhashashables, so I went back through and added that to the code. 
#I added the unhashable dictionary and checking to skip printing them out. 
#Now I move on to adding the hashing. 
#Now I move on to storing evertything into a file
#Now to open the hash file read it and see what's different when I run the program again








