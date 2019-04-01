import time
import heapq
import os
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
from PIL import Image
import numpy as np
np.set_printoptions(threshold='nan')

class Node(object):
    def __init__(self, pairs, frequency):
        # print pairs
        self.pairs = pairs
        self.frequency = frequency

    def __repr__(self):
        return repr(self.pairs) + ", " + repr(self.frequency)

    def merge(self, other):
        total_frequency = self.frequency + other.frequency
        for p in self.pairs:
            p[1] = "1" + p[1]
        for p in other.pairs:
            p[1] = "0" + p[1]
        new_pairs = self.pairs + other.pairs
        return Node(new_pairs, total_frequency)

    def __lt__(self, other):
        return self.frequency < other.frequency

def imread(imageFile):
		#read image
		currentImage = Image.open(imageFile)
		image = currentImage.load()
		[rows,columns] = currentImage.size
		redFile = open("redFile.txt","w")
		greenFile = open("greenFile.txt","w")
		blueFile = open("blueFile.txt","w")
		for i in range(0,rows):
			redFile.write("\n")
			greenFile.write("\n")
			blueFile.write("\n")
			for j in range(0, columns):
				redFile.write(str(image[i,j][0])+" ")
				greenFile.write(str(image[i,j][1])+" ")
				blueFile.write(str(image[i,j][2])+" ")

def getImageSize(imageFile):
		currentImage = Image.open(imageFile)
		return currentImage.size

def redPixelClustering(rows, columns, numberOfClusters):
	red = []
	with open("redFile.txt") as redFile:
		y = redFile.read()
		for m in y.split():
			red.append(int(m))
	redarray  = np.asarray(red);
	redCluster = open("redCluster.txt","w")
	centroids,_ = kmeans(redarray,numberOfClusters)
	k = 0;
	with open("redClusterTable.txt","w") as redClusterTable:
		for identifier in centroids:
			redClusterTable.write(str(k))
			redClusterTable.write(" "+str(identifier)+"\n");
			k = k+1
	idx,_ = vq(redarray,centroids)
	c = 1
	for cid in idx:
		redCluster.write(str(cid)+" ")
		c = c+1
		if(c==columns+1):
			redCluster.write("\n")
			c = 1;

def greenPixelClustering(rows, columns, numberOfClusters):
	green = []
	with open("greenFile.txt") as greenFile:
		y = greenFile.read()
		for m in y.split():
			green.append(int(m))
	greenarray  = np.asarray(green);
	greenCluster = open("greenCluster.txt","w")
	centroids,_ = kmeans(greenarray,numberOfClusters)
	k = 0
	with open("greenClusterTable.txt","w") as greenClusterTable:
		for identifier in centroids:
			greenClusterTable.write(str(k))
			greenClusterTable.write(" "+str(identifier)+"\n");
			k = k+1
	idx,_ = vq(greenarray,centroids)
	c = 1
	for cid in idx:
		greenCluster.write(str(cid)+" ")
		c = c+1
		if(c==columns+1):
			greenCluster.write("\n")
			c = 1;

def bluePixelClustering(rows, columns, numberOfClusters):
	blue = []
	with open("blueFile.txt") as blueFile:
		y = blueFile.read()
		for m in y.split():
			blue.append(int(m))
	bluearray  = np.asarray(blue);
	blueCluster = open("blueCluster.txt","w")
	centroids,_ = kmeans(bluearray,numberOfClusters)
	k = 0;
	with open("blueClusterTable.txt","w") as blueClusterTable:
		for identifier in centroids:
			# print identifier
			blueClusterTable.write(str(k))
			blueClusterTable.write(" "+str(identifier)+"\n");
			k = k+1
	c = 1
	idx,_ = vq(bluearray,centroids)
	for cid in idx:
		blueCluster.write(str(cid)+" ")
		c = c+1
		if(c==columns+1):
			blueCluster.write("\n")
			c = 1;

def doClustering(rows, columns, noOfClusters):
	redPixelClustering(rows, columns, noOfClusters)
	greenPixelClustering(rows, columns, noOfClusters)
	bluePixelClustering(rows, columns, noOfClusters)
	os.remove('redFile.txt')
	os.remove('blueFile.txt')
	os.remove('greenFile.txt')

def miner(rows, columns, noOfClusters, minimumSupport):
	redFile = []
	with open("redCluster.txt", "r") as r:
		for line in r:
			line = line.replace("\n","")
			redFile.append(" "+line+" ")
	# print redFile
	#Find all one length sequences
	frequentPatterns = {}
	currentLength = 1
	frequentPatterns[currentLength] = {}
	for i in range(0,noOfClusters):
		cKey = " "+str(i)+" "
		for eachLine in redFile:
			if(cKey in eachLine):
				if(cKey in frequentPatterns[currentLength].keys()):
					frequentPatterns[currentLength][cKey] = frequentPatterns[currentLength][cKey] + 1
				else:
					frequentPatterns[currentLength][cKey] = 1
	# print frequentPatterns
	#Enumerate length 2 frequent sequences
	currentLength = 2
	frequentPatterns[currentLength] = {}
	for key1 in frequentPatterns[currentLength-1].keys():
		for key2 in frequentPatterns[currentLength-1].keys():
			newKey = key1.rstrip()+key2
			frequentPatterns[currentLength][newKey] = 0
	for eachKey in frequentPatterns[currentLength].keys():
		for line in redFile:
			if(eachKey in line):
				frequentPatterns[currentLength][eachKey] = frequentPatterns[currentLength][eachKey] + 1
	for key in frequentPatterns[currentLength].keys():
		if(frequentPatterns[currentLength][key]<minimumSupport):
			frequentPatterns[currentLength].pop(key, None)
	currentLength = currentLength + 1
	# print frequentPatterns
	#Enumerate all frequent sequences
	for i in range(currentLength, columns+1):
		# print i
		# if(len(frequentPatterns[i].keys())!=0):
		frequentPatterns[i] = {}
		#Generate the i-length keys
		for key1 in frequentPatterns[i-1].keys():
			for key2 in frequentPatterns[i-1].keys():
				mkey1 = key1.lstrip().rstrip().split(" ")
				mkey2 = key2.lstrip().rstrip().split(" ")
				if(mkey1[1:len(mkey1)]==mkey2[0:len(mkey2)-1]):
					key2Split = key2.lstrip().rstrip().split(" ")
					newKey = key1+key2Split[len(key2Split)-1]+" "
					frequentPatterns[i][newKey] = 0;
		# print "Loop"
		#Find the support of each i-length key
		for line in redFile:
			for eachKey in frequentPatterns[i].keys():
				if(eachKey in line):
					frequentPatterns[i][eachKey] = frequentPatterns[i][eachKey] + 1

		#Pop all sequences that don't satisfy the minimum support threshold
		for key in frequentPatterns[i].keys():
			if(frequentPatterns[i][key]<minimumSupport):
				frequentPatterns[i].pop(key, None)

		#Pop all non closed sequences
		for key1 in frequentPatterns[i].keys():
			for key2 in frequentPatterns[i-1].keys():
				if((key2 in key1) and (frequentPatterns[i][key1] == frequentPatterns[i-1][key2])):
					frequentPatterns[i-1].pop(key2, None)

	allKeys = []
	allFrequentPatterns = {}
	for i in range(1, columns+1):
		for key in frequentPatterns[i].keys():
			allKeys.insert(0,key.lstrip().rstrip())
			allFrequentPatterns[key.lstrip().rstrip()] = 0
			# print key+"---"+str(frequentPatterns[i][key])

	#By this time all frequent sequences are generated
	'''*********************************************'''
	#Find the modified frequency of each sequence
	for line in redFile:
		# print "x"
		for key in allKeys:
			# print key
			if(len(key.split(" ")) == 1):
				# print key
				key = " "+key+" "
				if(key in line):
					allFrequentPatterns[key.lstrip().rstrip()] = allFrequentPatterns[key.lstrip().rstrip()] + line.count(key)
					while(key in line):
						line = line.replace(key,' ')
					# print line
			else:
				key = " "+key+" "
				if(key in line):
					# key = key.lstrip().rstrip()
					allFrequentPatterns[key.lstrip().rstrip()] = allFrequentPatterns[key.lstrip().rstrip()] + line.count(key)
					while(key in line):
						line = line.replace(key,' ')
		# print line
	finalKeys = open("redPatterns.txt","w")
	finalLength = 0
	for eachKey in allKeys:
		if(allFrequentPatterns[eachKey]!=0):
			finalKeys.write(eachKey.lstrip().rstrip()+"-"+str(allFrequentPatterns[eachKey])+"\n")
			finalLength = finalLength + (len(eachKey.lstrip().rstrip().split(" "))*allFrequentPatterns[eachKey])


	greenFile = []
	with open("greenCluster.txt", "r") as r:
		for line in r:
			line = line.replace("\n","")
			greenFile.append(" "+line+" ")

	#Find all one length sequences
	frequentPatterns = {}
	currentLength = 1
	frequentPatterns[currentLength] = {}
	for i in range(0,noOfClusters):
		cKey = " "+str(i)+" "
		for eachLine in greenFile:
			if(cKey in eachLine):
				if(cKey in frequentPatterns[currentLength].keys()):
					frequentPatterns[currentLength][cKey] = frequentPatterns[currentLength][cKey] + 1
				else:
					frequentPatterns[currentLength][cKey] = 1

	#Enumerate length 2 frequent sequences
	currentLength = 2
	frequentPatterns[currentLength] = {}
	for key1 in frequentPatterns[currentLength-1].keys():
		for key2 in frequentPatterns[currentLength-1].keys():
			newKey = key1.rstrip()+key2
			frequentPatterns[currentLength][newKey] = 0
	for eachKey in frequentPatterns[currentLength].keys():
		for line in redFile:
			if(eachKey in line):
				frequentPatterns[currentLength][eachKey] = frequentPatterns[currentLength][eachKey] + 1
	for key in frequentPatterns[currentLength].keys():
		if(frequentPatterns[currentLength][key]<minimumSupport):
			frequentPatterns[currentLength].pop(key, None)
	currentLength = currentLength + 1

	#Enumerate all frequent sequences
	for i in range(currentLength, columns+1):
		# if(len(frequentPatterns[i].keys())!=0):
		frequentPatterns[i] = {}
		#Generate the i-length keys
		for key1 in frequentPatterns[i-1].keys():
			for key2 in frequentPatterns[i-1].keys():
				mkey1 = key1.lstrip().rstrip().split(" ")
				mkey2 = key2.lstrip().rstrip().split(" ")
				if(mkey1[1:len(mkey1)]==mkey2[0:len(mkey2)-1]):
					key2Split = key2.lstrip().rstrip().split(" ")
					newKey = key1+key2Split[len(key2Split)-1]+" "
					frequentPatterns[i][newKey] = 0;

		#Find the support of each i-length key
		for line in greenFile:
			for eachKey in frequentPatterns[i].keys():
				if(eachKey in line):
					frequentPatterns[i][eachKey] = frequentPatterns[i][eachKey] + 1

		#Pop all sequences that don't satisfy the minimum support threshold
		for key in frequentPatterns[i].keys():
			if(frequentPatterns[i][key]<minimumSupport):
				frequentPatterns[i].pop(key, None)

		#Pop all non closed sequences
		for key1 in frequentPatterns[i].keys():
			for key2 in frequentPatterns[i-1].keys():
				if((key2 in key1) and (frequentPatterns[i][key1] == frequentPatterns[i-1][key2])):
					frequentPatterns[i-1].pop(key2, None)

	allKeys = []
	allFrequentPatterns = {}
	for i in range(1, columns+1):
		for key in frequentPatterns[i].keys():
			allKeys.insert(0,key.lstrip().rstrip())
			allFrequentPatterns[key.lstrip().rstrip()] = 0
			# print key+"---"+str(frequentPatterns[i][key])

	#By this time all frequent sequences are generated
	'''*********************************************'''
	#Find the modified frequency of each sequence
	for line in greenFile:
		for key in allKeys:
			if(len(key.split(" ")) == 1):
				# print key
				key = " "+key+" "
				if(key in line):
					allFrequentPatterns[key.lstrip().rstrip()] = allFrequentPatterns[key.lstrip().rstrip()] + line.count(key)
					while(key in line):
						line = line.replace(key,' ')
					# print line
			else:
				key = " "+key+" "
				if(key in line):
					# key = key.lstrip().rstrip()
					allFrequentPatterns[key.lstrip().rstrip()] = allFrequentPatterns[key.lstrip().rstrip()] + line.count(key)
					while(key in line):
						line = line.replace(key,' ')
	finalKeys = open("greenPatterns.txt","w")
	finalLength = 0
	for eachKey in allKeys:
		if(allFrequentPatterns[eachKey]!=0):
			finalKeys.write(eachKey.lstrip().rstrip()+"-"+str(allFrequentPatterns[eachKey])+"\n")
			finalLength = finalLength + (len(eachKey.lstrip().rstrip().split(" "))*allFrequentPatterns[eachKey])

	blueFile = []
	with open("blueCluster.txt", "r") as r:
		for line in r:
			line = line.replace("\n","")
			blueFile.append(" "+line+" ")

	#Find all one length sequences
	frequentPatterns = {}
	currentLength = 1
	frequentPatterns[currentLength] = {}
	for i in range(0,noOfClusters):
		cKey = " "+str(i)+" "
		for eachLine in blueFile:
			if(cKey in eachLine):
				if(cKey in frequentPatterns[currentLength].keys()):
					frequentPatterns[currentLength][cKey] = frequentPatterns[currentLength][cKey] + 1
				else:
					frequentPatterns[currentLength][cKey] = 1

	#Enumerate length 2 frequent sequences
	currentLength = 2
	frequentPatterns[currentLength] = {}
	for key1 in frequentPatterns[currentLength-1].keys():
		for key2 in frequentPatterns[currentLength-1].keys():
			newKey = key1.rstrip()+key2
			frequentPatterns[currentLength][newKey] = 0
	for eachKey in frequentPatterns[currentLength].keys():
		for line in redFile:
			if(eachKey in line):
				frequentPatterns[currentLength][eachKey] = frequentPatterns[currentLength][eachKey] + 1
	for key in frequentPatterns[currentLength].keys():
		if(frequentPatterns[currentLength][key]<minimumSupport):
			frequentPatterns[currentLength].pop(key, None)
	currentLength = currentLength + 1

	#Enumerate all frequent sequences
	for i in range(currentLength, columns+1):
		# if(len(frequentPatterns[i].keys())!=0):
		frequentPatterns[i] = {}
		#Generate the i-length keys
		for key1 in frequentPatterns[i-1].keys():
			for key2 in frequentPatterns[i-1].keys():
				mkey1 = key1.lstrip().rstrip().split(" ")
				mkey2 = key2.lstrip().rstrip().split(" ")
				if(mkey1[1:len(mkey1)]==mkey2[0:len(mkey2)-1]):
					key2Split = key2.lstrip().rstrip().split(" ")
					newKey = key1+key2Split[len(key2Split)-1]+" "
					frequentPatterns[i][newKey] = 0;

		#Find the support of each i-length key
		for line in blueFile:
			for eachKey in frequentPatterns[i].keys():
				if(eachKey in line):
					frequentPatterns[i][eachKey] = frequentPatterns[i][eachKey] + 1

		#Pop all sequences that don't satisfy the minimum support threshold
		for key in frequentPatterns[i].keys():
			if(frequentPatterns[i][key]<minimumSupport):
				frequentPatterns[i].pop(key, None)

		#Pop all non closed sequences
		for key1 in frequentPatterns[i].keys():
			for key2 in frequentPatterns[i-1].keys():
				if((key2 in key1) and (frequentPatterns[i][key1] == frequentPatterns[i-1][key2])):
					frequentPatterns[i-1].pop(key2, None)

	allKeys = []
	allFrequentPatterns = {}
	for i in range(1, columns+1):
		for key in frequentPatterns[i].keys():
			allKeys.insert(0,key.lstrip().rstrip())
			allFrequentPatterns[key.lstrip().rstrip()] = 0
			# print key+"---"+str(frequentPatterns[i][key])

	#By this time all frequent sequences are generated
	'''*********************************************'''
	#Find the modified frequency of each sequence
	for line in blueFile:
		for key in allKeys:
			if(len(key.split(" ")) == 1):
				# print key
				key = " "+key+" "
				if(key in line):
					allFrequentPatterns[key.lstrip().rstrip()] = allFrequentPatterns[key.lstrip().rstrip()] + line.count(key)
					while(key in line):
						line = line.replace(key,' ')
					# print line
			else:
				key = " "+key+" "
				if(key in line):
					# key = key.lstrip().rstrip()
					allFrequentPatterns[key.lstrip().rstrip()] = allFrequentPatterns[key.lstrip().rstrip()] + line.count(key)
					while(key in line):
						line = line.replace(key,' ')
	finalKeys = open("bluePatterns.txt","w")
	finalLength = 0
	for eachKey in allKeys:
		if(allFrequentPatterns[eachKey]!=0):
			finalKeys.write(eachKey.lstrip().rstrip()+"-"+str(allFrequentPatterns[eachKey])+"\n")
			finalLength = finalLength + (len(eachKey.lstrip().rstrip().split(" "))*allFrequentPatterns[eachKey])

def huffman_codes(s):
    freq = []
    i = 0
    table = []
    with open(s,"r") as s:
        for line in s:
            x = line.replace("\n",'').rstrip().split('-')
            table.append(Node([[x[0], '']], int(x[1])))
    heapq.heapify(table)
    while len(table) > 1:
        first_node = heapq.heappop(table)
        second_node = heapq.heappop(table)
        new_node = first_node.merge(second_node)
        heapq.heappush(table, new_node)
    return dict(table[0].pairs)

def huffEncode():
    s = open("rcodetable.txt","w")
    x = huffman_codes("redPatterns.txt")
    for i in x.keys():
        s.write(i+"-"+x[i]+"\n")

    s = open("gcodetable.txt","w")
    x = huffman_codes("greenPatterns.txt")
    for i in x.keys():
        s.write(i+"-"+x[i]+"\n")

    s = open("bcodetable.txt","w")
    x = huffman_codes("bluePatterns.txt")
    for i in x.keys():
        s.write(i+"-"+x[i]+"\n")

def redComponentCompressor():
	codetable = {}
	with open("rcodetable.txt","r") as ct:
		for line in ct:
			(pattern, code) = line.replace("\n","").split("-")
			codetable[pattern] = code

	codeTableItems = codetable.items()
	sortedCodeTable = sorted(codeTableItems,key = lambda s: len(s[0]))
	reversedSortedCodeTable = list(reversed(sortedCodeTable))
	# print reversedSortedCodeTable[0][0]
	codes = []
	for item in reversedSortedCodeTable:
		codes.append(item[0])

	# print codetable

	redEncoding = open("redCompressed.txt","w")
	with open("redCluster.txt","r") as rc:
		for line in rc:
			line = " " + line + " "
			currentLine = line
			for key in codes:
				# print codetable[key]
				if(len(key.split(" "))==1):
					# print "yes"
					k1 = " "+key+" "
					k2 = " "+key+" "
					if((k1 in currentLine)):
						while(k1 in currentLine):
							currentLine = currentLine.replace(k1, " -"+codetable[key]+"- ")
						# redEncoding.write("no-"+k1+"$$"+currentLine+"\n")
					elif(k2 in currentLine):
						while(k2 in currentLine):
							currentLine = currentLine.replace(k2, " -"+codetable[key]+"- ")
						# redEncoding.write("no-"+k2+"$$"+currentLine+"\n")
				else:
					# print "no"
					if(" "+key+" " in currentLine):
						while(" "+key+" " in currentLine):
							currentLine = currentLine.replace(" "+key+" ", " -"+codetable[key]+"- ")
						# redEncoding.write("ues "+currentLine+"\n")
						# print currentLprint currentLineine
			
			
			currentLine = currentLine.replace(" ","").replace("-","")
			redEncoding.write(currentLine+"\n")

def greenComponentCompressor():
	#FOR GREEN COMPONENT
	codetable = {}
	with open("gcodetable.txt","r") as ct:
		for line in ct:
			(pattern, code) = line.replace("\n","").split("-")
			codetable[pattern] = code

	codeTableItems = codetable.items()
	sortedCodeTable = sorted(codeTableItems,key = lambda s: len(s[0]))
	reversedSortedCodeTable = list(reversed(sortedCodeTable))
	# print reversedSortedCodeTable[0][0]
	codes = []
	for item in reversedSortedCodeTable:
		codes.append(item[0])

	# print codetable

	redEncoding = open("greenCompressed.txt","w")
	with open("greenCluster.txt","r") as rc:
		for line in rc:
			line = " " + line + " "
			currentLine = line
			for key in codes:
				# print codetable[key]
				if(len(key.split(" "))==1):
					# print "yes"
					k1 = " "+key+" "
					k2 = " "+key+" "
					if((k1 in currentLine)):
						while(k1 in currentLine):
							currentLine = currentLine.replace(k1, " -"+codetable[key]+"- ")
						# redEncoding.write("no-"+k1+"$$"+currentLine+"\n")
					elif(k2 in currentLine):
						while(k2 in currentLine):
							currentLine = currentLine.replace(k2, " -"+codetable[key]+"- ")
						# redEncoding.write("no-"+k2+"$$"+currentLine+"\n")
				else:
					# print "no"
					if(" "+key+" " in currentLine):
						while(" "+key+" " in currentLine):
							currentLine = currentLine.replace(" "+key+" ", " -"+codetable[key]+"- ")
						# redEncoding.write("ues "+currentLine+"\n")
						# print currentLprint currentLineine
			
			
			currentLine = currentLine.replace(" ","").replace("-","")
			redEncoding.write(currentLine+"\n")

def blueComponentCompressor():

	#FOR BLUE COMPONENT
	codetable = {}
	with open("bcodetable.txt","r") as ct:
		for line in ct:
			(pattern, code) = line.replace("\n","").split("-")
			codetable[pattern] = code

	codeTableItems = codetable.items()
	sortedCodeTable = sorted(codeTableItems,key = lambda s: len(s[0]))
	reversedSortedCodeTable = list(reversed(sortedCodeTable))
	# print reversedSortedCodeTable[0][0]
	codes = []
	for item in reversedSortedCodeTable:
		codes.append(item[0])

	# print codetable

	redEncoding = open("blueCompressed.txt","w")
	with open("blueCluster.txt","r") as rc:
		for line in rc:
			line = " " + line + " "
			currentLine = line
			for key in codes:
				# print codetable[key]
				if(len(key.split(" "))==1):
					# print "yes"
					k1 = " "+key+" "
					k2 = " "+key+" "
					if((k1 in currentLine)):
						while(k1 in currentLine):
							currentLine = currentLine.replace(k1, " -"+codetable[key]+"- ")
						# redEncoding.write("no-"+k1+"$$"+currentLine+"\n")
					elif(k2 in currentLine):
						while(k2 in currentLine):
							currentLine = currentLine.replace(k2, " -"+codetable[key]+"- ")
						# redEncoding.write("no-"+k2+"$$"+currentLine+"\n")
				else:
					# print "no"
					if(" "+key+" " in currentLine):
						while(" "+key+" " in currentLine):
							currentLine = currentLine.replace(" "+key+" ", " -"+codetable[key]+"- ")
						# redEncoding.write("ues "+currentLine+"\n")
						# print currentLprint currentLineine
			
			
			currentLine = currentLine.replace(" ","").replace("-","")
			redEncoding.write(currentLine+"\n")

def Compressor():
	redComponentCompressor()
	greenComponentCompressor()
	blueComponentCompressor()

def redComponentDecoder():
	codeTable = {}
	with open("rcodetable.txt","r") as ct:
		for line in ct:
			(pattern, code) = line.replace("\n","").split("-")
			codeTable[code] = pattern

	redDecomp = open("redDecomp.txt","w")
	with open("redCompressed.txt","r") as rc:
		for line in rc:
			# print line
			currentLine = ""
			cString = ""
			count = 0
			for i in line:
				# print i
				cString = cString + i
				count = 0
				for key in codeTable.keys():
					if(cString == key):
						count = 1
						break
				if(count == 1):
					# redDecomp.write(cString+"---"+codeTable[cString]+"\n")
					# currentLine = currentLine.replace(cString,"-"+codeTable[cString]+"-")
					currentLine= currentLine+" "+codeTable[cString]
					# redDecomp.write(currentLine+"\n")
					cString = ""
			redDecomp.write(currentLine.rstrip().lstrip()+"\n")
			# print currentLine
			# break

def greenComponentDecoder():
	#FOR GREEN COMPONENT
	codeTable = {}
	with open("gcodetable.txt","r") as ct:
		for line in ct:
			(pattern, code) = line.replace("\n","").split("-")
			codeTable[code] = pattern

	greenDecomp = open("greenDecomp.txt","w")
	with open("greenCompressed.txt","r") as rc:
		for line in rc:
			# print line
			currentLine = ""
			cString = ""
			count = 0
			for i in line:
				# print i
				cString = cString + i
				count = 0
				for key in codeTable.keys():
					if(cString == key):
						count = 1
						break
				if(count == 1):
					# redDecomp.write(cString+"---"+codeTable[cString]+"\n")
					# currentLine = currentLine.replace(cString,"-"+codeTable[cString]+"-")
					currentLine= currentLine+" "+codeTable[cString]
					# redDecomp.write(currentLine+"\n")
					cString = ""
			greenDecomp.write(currentLine.rstrip().lstrip()+"\n")
			# print currentLine
			# break

def blueComponentDecoder():

	#FOR BLUE COMPONENT
	codeTable = {}
	with open("bcodetable.txt","r") as ct:
		for line in ct:
			(pattern, code) = line.replace("\n","").split("-")
			codeTable[code] = pattern

	blueDecomp = open("blueDecomp.txt","w")
	with open("blueCompressed.txt","r") as rc:
		for line in rc:
			# print line
			currentLine = ""
			cString = ""
			count = 0
			for i in line:
				# print i
				cString = cString + i
				count = 0
				for key in codeTable.keys():
					if(cString == key):
						count = 1
						break
				if(count == 1):
					# redDecomp.write(cString+"---"+codeTable[cString]+"\n")
					# currentLine = currentLine.replace(cString,"-"+codeTable[cString]+"-")
					currentLine= currentLine+" "+codeTable[cString]
					# redDecomp.write(currentLine+"\n")
					cString = ""
			blueDecomp.write(currentLine.rstrip().lstrip()+"\n")
			# print currentLine
			# break

def Decoder():
	redComponentDecoder()
	greenComponentDecoder()
	blueComponentDecoder()

def reconstruct(rows, columns, fileName):
	data = np.zeros( (rows,columns,3), dtype=np.uint8)

	redClusters = {}
	with open("redClusterTable.txt","r") as redC:
		for line in redC:
			(x,y) = line.split(" ")
			(x,y) = (int(x), int(y))
			redClusters[x] = y
			
	i = 0;
	j = 0;
	with open("redDecomp.txt","r") as rc, open("dummy.txt","w") as d:
		r = rc.read()
		for character in r.split():
			if(j==columns):
				i = i+1
				j = 0
			# d.write(str(redClusters[int(character)])+" ")
			data[j,i,0] = redClusters[int(character)]
			d.write(str(data[i,j,0])+" ")
			j = j+1;



	greenClusters = {}
	with open("greenClusterTable.txt","r") as greenC:
		for line in greenC:
			(x,y) = line.split(" ")
			(x,y) = (int(x), int(y))
			greenClusters[x] = y
	i = 0;
	j = 0;
	with open("greenDecomp.txt","r") as rc, open("dummy.txt","w") as d:
		r = rc.read()
		for character in r.split():
				if(j==columns):
					i = i+1
					j = 0
				# d.write(str(redClusters[int(character)])+" ")
				data[j,i,1] = greenClusters[int(character)]
				d.write(str(data[i,j,1])+" ")
				j = j+1;



	blueClusters = {}
	with open("blueClusterTable.txt","r") as blueC:
		for line in blueC:
			(x,y) = line.split(" ")
			(x,y) = (int(x), int(y))
			blueClusters[x] = y

	# print blueClusters
	i = 0;
	j = 0;
	with open("blueDecomp.txt","r") as rc, open("dummy.txt","w") as d:
		r = rc.read()
		for character in r.split():
				if(j==columns):
					i = i+1
					j = 0
				# d.write(str(redClusters[int(character)])+" ")
				data[j,i,2] = blueClusters[int(character)]
				d.write(str(data[i,j,2])+" ")
				j = j+1;

	img = Image.fromarray(data, 'RGB')
	img.save(fileName+'.tiff')


results = open("results.txt","w")

imageFile ="4.2.02.tiff"
for k in range(8, 25):
	for alpha in range(10, 105, 12):
		results = open("results.txt", "a")
		noOfClusters = k
		[imageRows, imageColumns] = getImageSize(imageFile)
		minimumSupport = (alpha/(100*1.0))
		ms = int(minimumSupport*imageRows)
		wStart = time.clock()
		imread(imageFile)
		print "Read Image Done"
		clusterStart = time.clock()
		doClustering(imageRows, imageColumns, noOfClusters)
		clusterEnd = time.clock()
		print "Clustering Done"
		minerStart = time.clock()
		miner(imageRows, imageColumns, noOfClusters, ms)
		minerEnd = time.clock()
		print "Mining Done"
		encodeStart = time.clock()
		huffEncode()
		encodeEnd = time.clock()
		print "Encoding Done"
		compressStart = time.clock()
		Compressor()
		compressEnd = time.clock()
		print "Compressing Done"
		decodeStart = time.clock()
		Decoder()
		decodeEnd = time.clock()
		print "Decomressing Done"
		reconstruct(imageRows, imageColumns, str(noOfClusters)+"-"+str(alpha))
		print "Reconstructing Done"
		wEnd = time.clock()
		cTableSize = os.stat("redClusterTable.txt").st_size+os.stat("blueClusterTable.txt").st_size+os.stat("greenClusterTable.txt").st_size
		cTableSize = (cTableSize/(1000*1.0))
		coTableSize = os.stat("rcodetable.txt").st_size+os.stat("gcodetable.txt").st_size+os.stat("bcodetable.txt").st_size
		coTableSize = (coTableSize/(2*1.0))
		compressedImageSize = os.stat("redCompressed.txt").st_size+os.stat("greenCompressed.txt").st_size+os.stat("blueCompressed.txt").st_size
		compressedImageSize = (compressedImageSize / 8*1.0)

		totalSize = cTableSize + coTableSize + compressedImageSize
		results.write("k-"+str(k)+"-su-"+str(alpha)+"-clustertime-"+str(clusterEnd-clusterStart)+"-mineTime-"+str(minerEnd-minerStart)+"-encodeTime-"+str(encodeEnd-encodeStart)+"-compressTime-"+str(compressEnd-compressStart)+"-Decode time-"+str(decodeEnd-decodeStart)+"-ClusterTableSize-"+str(cTableSize)+"-codeTableSize-"+str(coTableSize)+"-CompressedImageSize-"+str(compressedImageSize)+"-Total Size-"+str(totalSize)+"-TotalTime-"+str(wEnd-wStart)+"\n")
		results.close()

		#Remove Unwanted Files
		os.remove("bcodetable.txt")
		os.remove("rcodetable.txt")
		os.remove("gcodetable.txt")
		os.remove("blueCompressed.txt")
		os.remove("greenCompressed.txt")
		os.remove("redCompressed.txt")
		os.remove("blueDecomp.txt")
		os.remove("greenDecomp.txt")
		os.remove("redDecomp.txt")
		os.remove("bluePatterns.txt")
		os.remove("redPatterns.txt")
		os.remove("greenPatterns.txt")
		os.remove("greenCluster.txt")
		os.remove("redCluster.txt")
		os.remove("blueCluster.txt")
		os.remove("greenClusterTable.txt")
		os.remove("blueClusterTable.txt")
		os.remove("redClusterTable.txt")
		os.remove("dummy.txt")










