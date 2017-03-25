#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Spencer Caplan
# Contact: spcaplan@sas.upenn.edu
# Modified: 3/25/2017

import sys, unicodedata, operator
reload(sys)
sys.setdefaultencoding('utf-8')
from unicodedata import normalize

fullCoupleRankingDict = {}
leaderFullnameRankingDict = {}
leaderSurnameRankingDict = {}

def extractRankingFromFile(inputFilePath):
	global fullCoupleRankingDict, leaderFullnameRankingDict, leaderSurnameRankingDict
	doubleEntryLeader = []
	doubleEntryLeaderSurname = []
	with open(inputFilePath, 'r') as inputFile:
		for currLine in inputFile:
			if '&' in currLine:
				tokens = currLine.split('&')
				rankIndex = tokens[0].rfind(".")
				rank = tokens[0][:rankIndex]
				leaderIndex = tokens[0].rfind("\t")
				leader = tokens[0][leaderIndex+1:].strip().lower()
				leaderSurname = leader.split(' ')[1]
				follow = tokens[1].strip().lower()
				couple = leader + ' & ' + follow
				fullCoupleRankingDict[couple] = int(rank)

				# So that double entries are removed at the end rather than overwritten
				if leader in leaderFullnameRankingDict:
					doubleEntryLeader.append(leader)
				if leaderSurname in leaderSurnameRankingDict:
					doubleEntryLeaderSurname.append(leaderSurname)

				leaderFullnameRankingDict[leader] = int(rank)
				leaderSurnameRankingDict[leaderSurname] = int(rank)
				#print rank + couple

	for leader in doubleEntryLeader:
		if leader in leaderFullnameRankingDict:
			del leaderFullnameRankingDict[leader]
	for leaderSurname in doubleEntryLeaderSurname:
		if leaderSurname in leaderSurnameRankingDict:
			del leaderSurnameRankingDict[leaderSurname]

def predictResults(eventListFilePath):
	global fullCoupleRankingDict, leaderFullnameRankingDict, leaderSurnameRankingDict
	competingDict = {}
	with open(eventListFilePath, 'r') as eventFile:
		for currLine in eventFile:
			currCouple = currLine.split(' of ')[0].strip().lower()
			currLeader = currCouple.split(' & ')[0]
			currLeaderSurname = currLeader.split(' ')[1]
			if currCouple in fullCoupleRankingDict:
				competingDict[currCouple] = fullCoupleRankingDict[currCouple]
			elif currLeader in leaderFullnameRankingDict:
				competingDict[currCouple] = leaderFullnameRankingDict[currLeader]
			elif currLeaderSurname in leaderSurnameRankingDict:
				competingDict[currCouple] = leaderSurnameRankingDict[currLeaderSurname]
			else:
				competingDict[currCouple] = 999
	
	sorted_heatList = sorted(competingDict.items(), key=operator.itemgetter(1))
	counter = 1
	printedUnrankBreak = False
	for couple, rank in sorted_heatList:
		if rank == 999 and not printedUnrankBreak:
			print '\n-----UNRANKED-----'
			printedUnrankBreak = True
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

	extractRankingFromFile(priorRankingFile)
	predictResults(eventListFile)