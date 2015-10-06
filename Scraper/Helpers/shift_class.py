import pandas as pd

class Shift():
    def __init__(self):
        pass

def shift_list_to_class(shift_as_list):
    shift = Shift()
    [shift.home_players, 
     shift.away_players, 
     shift.start,
     shift.end,
     shift.last_faceoff,
     shift.home_shots,
     shift.away_shots] = shift_as_list
    shift.home_number, shift.away_number = [len(shift.home_players), len(shift.away_players)]
    return shift

def create_final_shift_df(shift_list):
    player_list = reduce(lambda a,b: a.union(b), map(lambda x: set(x.away_players+x.home_players),shift_list))
    num_shifts = len(shift_list)
    dict_of_shifts = {}
    
    for player_name in player_list:
        dict_of_shifts[player_name] = [0]*num_shifts
    
    for k,shift in enumerate(shift_list):
        for player in shift.home_players:
            dict_of_shifts[player][k] = 1
        for player in shift.away_players:
            dict_of_shifts[player][k] = -1

    df = pd.DataFrame(dict_of_shifts)
    df['home_on_ice'] = [shift.home_number for shift in shift_list]
    df['away_on_ice'] = [shift.away_number for shift in shift_list]
    df['home_shots'] = [shift.home_shots for shift in shift_list]
    df['away_shots'] = [shift.away_shots for shift in shift_list]
    df['faceoff_adjusted_start'] = [shift.start for shift in shift_list]
    df['end'] = [shift.end for shift in shift_list]
    
    return df