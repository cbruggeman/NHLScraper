import re
import pandas as pd
import numpy as np

# Takes in the TOI html for a game, outputs the TOI dataframe for each game
def parse_TOI(text):
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
        shiftNumber=[]
        shiftPeriod=[]
        shiftStart=[]
        shiftEnd=[]
        for shiftText in shifts[2:]:
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
        
        playerDf=pd.DataFrame({ 'firstName': firstName,
          'lastName': lastName,
          'playerNumber': playerNumber,
          'team': teamName,
          'shiftNumber': shiftNumber,
          'shiftPeriod': shiftPeriod,
          'shiftStart': shiftStart,
          'shiftEnd': shiftEnd,
          'gameNumber': gameNumber,
          'gameDate':gameDate})
        if not is_goalie(playerDf):
            dfList.append(playerDf)
    return pd.concat(dfList)

def is_goalie(shift_df):
  shift_lengths = shift_df['shiftEnd']-shift_df['shiftStart']
  mean_length = np.mean(shift_lengths)
  total_length = sum(shift_lengths)
  if total_length > 2400 or mean_length > 200:
    return True

  return False


def convertTime(timeString,period):
    timeString=timeString.strip()
    time=60*int(timeString.split(":")[0])+int(timeString.split(":")[1])
    return time + 20*60*max(0,period-1)



