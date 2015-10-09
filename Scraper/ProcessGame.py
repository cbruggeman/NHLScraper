

def processGame(season,gameNumber):

    homeTeamTOI=parseTOI(urllib.urlopen('http://www.nhl.com/scores/htmlreports/%d/TH02%04d.HTM'%(season,gameNumber)).read())
    awayTeamTOI=parseTOI(urllib.urlopen('http://www.nhl.com/scores/htmlreports/%d/TH02%04d.HTM'%(season,gameNumber)).read())
    shotPP,faceoffPP,goalPP,awayTeam,homeTeam=parsePlayByPlay(urllib.urlopen("http://www.nhl.com/scores/htmlreports/%d/PL02%04d.HTM"%(season,gameNumber)).read())
    #gameNumber=int(homeTeamTOI['gameNumber'].values[0])
    gameDate=homeTeamTOI['gameDate'].values[0]



    homePlayers=homeTeamTOI['playerNumber'].unique()
    awayPlayers=awayTeamTOI['playerNumber'].unique()

    shift_data_list = reduce(mergeShiftData,convert_shift_df_to_list(home_toi_df,True)+convert_shift_df_to_list(away_toi_df,False))


def convert_shift_df_to_list(shift_df, home):
    if home:
        home_away = 0
    else:
        home_away = 1


    shift_df['playerName'] = shift_df['firstName']+' '+shift_df['lastName']

    grouped = shift_df.groupby('playerName')
    final_list = []
    for player, shifts in grouped:
        player_list = []
        shift_start = list(shifts['shiftStart'])
        shift_end = list(shifts['shiftEnd'])
        for start, end in zip(shift_start,shift_end):
            entry = [[],[],shift_start,shift_end]
            entry[home_away].append(player)
            player_list.append(entry)
        final_list.append(player_list)

    return final_list




