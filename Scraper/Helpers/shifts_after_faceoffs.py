import copy

def shifts_after_faceoff_delay(shift_list, cutoff = 10):
    """shift_list has form [home_players, away_players, shift_start, shift_end, time_of_last_faceoff]
    """
    filtered_list = []
    for shift in shift_list:
        if shift.end-shift.last_faceoff <= cutoff:
            continue
        elif shift.start > shift.last_faceoff + cutoff:
            filtered_list.append(copy.deepcopy(shift))
        else:
            new_shift = copy.deepcopy(shift)
            new_shift.start = new_shift.last_faceoff + cutoff
            filtered_list.append(new_shift)
    
    return filtered_list
        