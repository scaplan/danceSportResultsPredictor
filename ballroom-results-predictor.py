#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata, operator
from unicodedata import normalize

def extractRankingFromFile(inputFilePath):
	rankingDict = {}
	with open(inputFilePath, 'r') as inputFile:
		for currLine in inputFile:
			if '&' in currLine:
				tokens = currLine.split('&')
				rankIndex = tokens[0].rfind(".")
				rank = tokens[0][:rankIndex]
				leaderIndex = tokens[0].rfind("\t")
				leader = tokens[0][leaderIndex+1:].strip().lower()
				follow = tokens[1].strip().lower()
				couple = leader + ' & ' + follow
				rankingDict[couple] = int(rank)
				#print rank + couple
	return rankingDict

def predictResults(rankingDict, eventListFilePath):
	competingDict = {}
	with open(eventListFilePath, 'r') as eventFile:
		for currLine in eventFile:
			currCouple = currLine.split(' of ')[0].strip().lower()
			if currCouple in rankingDict:
				competingDict[currCouple] = rankingDict[currCouple]
			else:
				competingDict[currCouple] = 101
	
	sorted_heatList = sorted(competingDict.items(), key=operator.itemgetter(1))
	counter = 1
	for couple, rank in sorted_heatList:
		print str(counter) + '. ' + couple + ' --- ' + str(rank)
		counter += 1

##
## Main method block
##
if __name__=="__main__":

	if (len(sys.argv) < 2):
		print('incorrect number of arguments ' + str(len(sys.argv)) + ' given')
		exit(0)

	priorRankingFile = sys.argv[1]
	eventListFile = sys.argv[2]

	rankingDict = extractRankingFromFile(priorRankingFile)
	predictResults(rankingDict, eventListFile)