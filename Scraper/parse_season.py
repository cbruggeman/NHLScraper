import os

from Helpers.convert_df_to_list import *
from Helpers.merge_shifts import *
from Helpers.merge_shot_data import *
from Helpers.parse_play_by_play import *
from Helpers.parse_toi import *
from Helpers.shifts_after_faceoffs import *
from Helpers.time_since_faceoff import *
from Helpers.shift_class import *

def make_dir(path):
    if not os.path.isdir('./%s'%(path)):
        os.mkdir('./%s'%(path))


def process_season(season_start, faceoff_cutoff = 10):
    num_games = 3
    season_string = "{0}{1}".format(season_start,season_start+1)
    for game in range(1,num_games+1):
        in_file = open('./../data/html/%s/%04d/play_by_play.html'%(season_string,game), 'r')
        play_by_play_html = in_file.read()
        in_file.close()
        in_file = open('./../data/html/%s/%04d/home_toi.html'%(season_string,game), 'r')
        home_toi_html = in_file.read()
        in_file.close()
        in_file = open('./../data/html/%s/%04d/away_toi.html'%(season_string,game), 'r')
        away_toi_html = in_file.read()
        in_file.close()
        
        make_dir('./../data/raw')
        make_dir('./../data/raw/%s'%season_string)

        make_dir('./../data/filtered')
        make_dir('./../data/filtered/%s'%season_string)

        print 'Processing game: %d'%game
        process_game(play_by_play_html = play_by_play_html,
                        home_toi_html = home_toi_html,
                        away_toi_html = away_toi_html,
                        season_string = season_string,
                        game_num = game,
                        faceoff_cutoff = faceoff_cutoff,
                        save_raw_data = True)


def process_game(play_by_play_html, 
                    home_toi_html, 
                    away_toi_html, 
                    season_string = "20142015", 
                    game_num = 1, 
                    faceoff_cutoff = 10,
                    save_raw_data = True):
    homeTeamTOI = parse_TOI(home_toi_html)
    awayTeamTOI = parse_TOI(away_toi_html)
    shotPP,faceoffPP,goalPP,awayTeam,homeTeam = parse_play_by_play(play_by_play_html)

    make_dir('./../data/raw/%s/%04d'%(season_string,game_num))

    homeTeamTOI.to_csv('./../data/raw/%s/%04d/home_toi.csv'%(season_string,game_num))
    awayTeamTOI.to_csv('./../data/raw/%s/%04d/away_toi.csv'%(season_string,game_num))
    shotPP.to_csv('./../data/raw/%s/%04d/shots.csv'%(season_string,game_num))
    faceoffPP.to_csv('./../data/raw/%s/%04d/faceoffs.csv'%(season_string,game_num))
    goalPP.to_csv('./../data/raw/%s/%04d/goals.csv'%(season_string,game_num))


    gameDate = homeTeamTOI['gameDate'].values[0]

    homePlayers = homeTeamTOI['playerNumber'].unique()
    awayPlayers = awayTeamTOI['playerNumber'].unique()

    shift_data_list = reduce(merge_shift_data,convert_shift_df_to_list(homeTeamTOI,True)+
                                            convert_shift_df_to_list(awayTeamTOI,False))
    
    faceoff_times = list(faceoffPP.time)
    merged_faceoffs = time_since_faceoff(shift_data_list, faceoff_times)
    merged_cutoff = shifts_after_faceoff_delay(merged_faceoffs, faceoff_cutoff)
    
    home_shots = sorted(list(shotPP.time[shotPP.team == homeTeam]) + list(goalPP.time[goalPP.team == homeTeam]))
    away_shots = sorted(list(shotPP.time[shotPP.team == awayTeam]) + list(goalPP.time[goalPP.team == awayTeam]))
    
    merged_shots = merge_shot_data(merged_cutoff, home_shots, away_shots)
    for shift in merged_shots:
        shift.home_number = len(shift.home_players)
        shift.away_number = len(shift.away_players)
    #final_list_class = map(add_number_on_ice, merged_shots)

    df = create_final_shift_df(merged_shots)
    #  print list(df.columns)
    df.to_csv('./../data/filtered/%s/filtered%04d.csv'%(season_string,game_num))



process_season(2014)    