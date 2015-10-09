import copy

def merge_shot_data(shift_list, home_shots, away_shots):
    return shot_data_helper(shot_data_helper(copy.deepcopy(shift_list),home_shots, home = True),
                            away_shots, home = False)

def shot_data_helper(shift_list, shots, home = True):
    if home:
        home_away = 'home_shots'
    else:
        home_away = 'away_shots'


    shift_iter = iter(shift_list)
    shift = shift_iter.next()
    for shot in shots:
        while shot > shift.end:
            try:
                shift = shift_iter.next()
            except StopIteration:
                break
        if shot >= shift.start:
            setattr(shift, home_away, getattr(shift, home_away)+1)

    return shift_list