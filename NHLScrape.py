import re
import urllib
import pandas as pd
import numpy as np

# Takes in the TOI html for a game, outputs the TOI dataframe for each game

def convertTime(timeString,period):
	timeString=timeString.strip()
	time=60*int(timeString.split(":")[0])+int(timeString.split(":")[1])
	return time + 20*60*max(0,period-1)
	

def parseTOI(text):

	playersText=text.split("playerHeading")

	# Game meta-data
	top=playersText[1]
	gameNumber=re.search(r':bold">Game (\d+)',top).group(1)
	gameDate=re.search(r'bold">(\w+, \w+ \d+, \d+)</td>',top).group(1)
	teamName=re.search(r'class="teamHeading \+ border" align="center">([\w \.-]+)</td',top).group(1)

	# Process shift-by-shift data
	dfList=[]
	for playerText in playersText[2:]:
		shifts=playerText.split("</tr>")
		nameNum=re.search('colspan="8">(\d+) ([\w \.\'-]+), ([\w \.\'-]+)',shifts[0])
		playerNumber, lastName, firstName=nameNum.groups()
		# Text to find name/number
		shifts=playerText.split("<tr")
		for shiftText in shifts[2:]:
			shiftNumber=[]
			shiftPeriod=[]
			shiftStart=[]
			shiftEnd=[]
			shiftData=re.findall(r'border">([\w :]+)',shiftText)
			
			# Break when hitting summaries
			if not shiftData or shiftData[0]=="Per": break

			# Convert to Numeric
			period=shiftData[1]
			if period=="OT": period=4
			else: period=int(period)
			shiftNumber.append(int(shiftData[0]))
			shiftPeriod.append(period)

			# Convert to TimeData
			shiftStart.append(convertTime(shiftData[2],period))
			shiftEnd.append(convertTime(shiftData[3],period))

			playerDf=pd.DataFrame({	'firstName': firstName,
									'lastName': lastName,
									'playerNumber': playerNumber,
									'team': teamName,
									'shiftNumber': shiftNumber,
									'shiftPeriod': shiftPeriod,
									'shiftStart': shiftStart,
									'shiftEnd': shiftEnd,
									'gameNumber': gameNumber,
									'gameDate':gameDate})
			dfList.append(playerDf)
	return pd.concat(dfList)

def parsePlayByPlay(text):
	textChunks=text.split("Copyright")

	shotTimeLst=[]
	shooterLst=[]
	shootingTeamLst=[]
	faceTimeLst=[]
	faceWinnerLst=[]
	faceLocLst=[]
	goalTimeLst=[]
	goalScorerLst=[]
	goalTeamLst=[]



	for textChunk in textChunks:
		if not re.search(r'>([\w \.]+)<br>Game \d+ Away Game',textChunk): break
		awayTeam=re.search(r'>([\w \.]+)<br>Game \d+ Away Game',textChunk).group(1)
		homeTeam=re.search(r'>([\w \.]+)<br>Game \d+ Home Game',textChunk).group(1)
		[awayShort,homeShort]=re.findall(r'([\w \.]+) On Ice',textChunk)
		for eventChunk in textChunk.split('<td align="center" class="')[1:]:
			#eventData=re.findall(r'">([\w @:\.@#@&@;@-@,@-@)@(]+)<',eventChunk)
			eventData=re.findall(r'">([^<]+)<',eventChunk) # Learned about ^ in regular expressions. Life is much easier now
			period=eventData[1]
			if period=="OT": period=4
			else: period=int(period)

			time=convertTime(eventData[3],period)
			eventType=eventData[4]
			eventText=eventData[5]
			#print eventType,eventText
			if eventType=="SHOT":
				shotTimeLst.append(time)
				shootingTeamLst.append(eventText.split()[0])
				shooterLst.append(eventText.split()[3].strip("#"))

			if eventType=="FAC":
				faceTimeLst.append(time)
				faceWinnerLst.append(eventText.split()[0])
				faceLocLst.append(eventText.split()[2])

			if eventType=="GOAL":
				goalTimeLst.append(time)
				goalTeamLst.append(eventText.split()[0])
				goalScorerLst.append(eventText.split()[1].strip('#'))

	shotDf=pd.DataFrame({	'time': shotTimeLst,
							'team': shootingTeamLst,
							'shooter': shooterLst})
	faceoffDf=pd.DataFrame({'time': faceTimeLst,
							'winner': faceWinnerLst,
							'location': faceLocLst})

	goalDf=pd.DataFrame({	'time': goalTimeLst,
							'team': goalTeamLst,
							'shooter': goalScorerLst})

	return (shotDf,faceoffDf,goalDf,awayTeam,homeTeam)




# Retrieves all necessary data for a given game
def processGame(season,gameNumber):
	#Sanitize Season Input
	#print 'http://www.nhl.com/scores/htmlreports/%d/TH02%04d.HTM'%(season,gameNumber)
	homeTeamTOI=parseTOI(urllib.urlopen('http://www.nhl.com/scores/htmlreports/%d/TH02%04d.HTM'%(season,gameNumber)).read())
	awayTeamTOI=parseTOI(urllib.urlopen('http://www.nhl.com/scores/htmlreports/%d/TH02%04d.HTM'%(season,gameNumber)).read())
	shotPP,faceoffPP,goalPP,awayTeam,homeTeam=parsePlayByPlay(urllib.urlopen("http://www.nhl.com/scores/htmlreports/%d/PL02%04d.HTM"%(season,gameNumber)).read())
	#gameNumber=int(homeTeamTOI['gameNumber'].values[0])
	gameDate=homeTeamTOI['gameDate'].values[0]

	#Figure out how to remove goalies

	homePlayers=homeTeamTOI['playerNumber'].unique()
	awayPlayers=awayTeamTOI['playerNumber'].unique()

	shiftDataList=[]
	for pNum in homePlayers:
		tempdf=homeTeamTOI[homeTeamTOI['playerNumber'==pNum]][['shiftStart','shiftEnd']]
		





# To be filled in: retrieves all necessary data for a single season
def processSeason(season):
	pass








print processGame(20142015,1053)
			
#print parsePlayByPlay(urllib.urlopen("http://www.nhl.com/scores/htmlreports/20142015/PL021053.HTM").read())[2]
#print parseTOI(urllib.urlopen('http://www.nhl.com/scores/htmlreports/20142015/TV021051.HTM').read())
###

