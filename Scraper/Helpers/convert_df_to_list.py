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
        shift_starts = list(shifts['shiftStart'])
        shift_ends = list(shifts['shiftEnd'])
        for start, end in zip(shift_starts,shift_ends):
            entry = [[],[],start,end]
            entry[home_away].append(player)
            player_list.append(entry)
        final_list.append(player_list)

    return final_list