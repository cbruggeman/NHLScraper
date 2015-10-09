from .shift_class import Shift

def convert_shift_df_to_list(shift_df, home):
    if home:
        home_away = 'home_players'
    else:
        home_away = 'away_players'


    shift_df['playerName'] = shift_df['firstName']+' '+shift_df['lastName']
    grouped = shift_df.groupby('playerName')
    final_list = []
    for player, shifts in grouped:
        player_list = []
        for start, end in zip(shifts['shiftStart'],shifts['shiftEnd']):
            entry = Shift()
            entry.start = start
            entry.end = end
            setattr(entry,home_away,[player])
            player_list.append(entry)
        final_list.append(player_list)

    return final_list