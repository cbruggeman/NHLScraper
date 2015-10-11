import re
import pandas as pd

def parse_play_by_play(text):
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

                shotDf=pd.DataFrame({   'time': shotTimeLst,
                    'team': shootingTeamLst,
                    'shooter': shooterLst})
                faceoffDf=pd.DataFrame({'time': faceTimeLst,
                    'winner': faceWinnerLst,
                    'location': faceLocLst})

                goalDf=pd.DataFrame({   'time': goalTimeLst,
                    'team': goalTeamLst,
                    'shooter': goalScorerLst})

    return (shotDf,faceoffDf,goalDf,awayTeam,homeTeam)

def convertTime(time_string,period):
    """Converts the time from a string of the form MM:SS to a measurement in seconds.
    Removes non-numeric characters to catch typos in the game-log. Adds on 20 minutes
    for each period of play.
    """
    time_string = time_string.strip()
    minutes, seconds = map(lambda x: int(re.sub('[^\d]','',x)), time_string.split(':'))
    time=60*minutes+seconds
    return time + 20*60*max(0,period-1)