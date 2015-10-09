import copy

def time_since_faceoff(shift_data, faceoff_times):
    """
    Takes in a list of shifts in the form:
    [list_of_home_players, list_of_away_players, shift_start, shift_end]
    and a list of faceoff_times and adds an additional value representing
    the time of the last faceoff.

    If a faceoff occurs during a shift without any players changing, then
    the shift is split into two at the time of the faceoff.
    """

    shift_num = 0
    total_shifts = len(shift_data)
    new_shift_list = []
    shift = copy.deepcopy(shift_data[0])
    faceoff_num = 0
    faceoff = faceoff_times[0]
    next_faceoff = faceoff_times[1]

    while True:
        if faceoff > shift[2]:
            # Something bad has happened?
            continue

        elif faceoff <= shift[2]:

            # If this is the last faceoff, add remaining shifts with this faceoff time
            if faceoff_num == (len(faceoff_times) - 1):
                shift.append(faceoff)
                new_shift_list.append(shift)
                new_shift_list.extend([shift+[faceoff] for shift in copy.deepcopy(shift_data[shift_num+1:])])
                break

            

             # Check if the next faceoff also happens before the shift starts
            elif next_faceoff <= shift[2]:
                faceoff = next_faceoff
                faceoff_num += 1
                if faceoff_num < (len(faceoff_times) - 1):
                    next_faceoff = faceoff_times[faceoff_num + 1]

            # Check if the next faceoff happens before the end of the shift
            elif next_faceoff < shift[3]:
                new_shift = copy.deepcopy(shift)
                new_shift.append(faceoff)
                new_shift[3] = next_faceoff
                new_shift_list.append(new_shift)
                shift[2] = next_faceoff

            # If this is the last shift
            elif shift_num == (total_shifts - 1):
                shift.append(faceoff)
                new_shift_list.append(shift)
                break
             
            else:
                shift.append(faceoff)
                new_shift_list.append(shift)
                shift_num += 1
                shift = copy.deepcopy(shift_data[shift_num])

    return new_shift_list


