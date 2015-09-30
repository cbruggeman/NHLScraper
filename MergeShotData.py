import copy

def merge_shot_data(shift_list, home_shots, away_shots):
    return shot_data_helper(shot_data_helper(copy.deepcopy(shift_list),home_shots),away_shots)



def shot_data_helper(shift_list, shots):
    shift_list = [shift+[0] for shift in shift_list]

    shift_iter = iter(shift)
    shift = shift_iter.next()
    for shot in shots:
        while shot > shift[3]:
            try:
                shift = shift_iter.next()
            except StopIteration:
                break
        shift[-1] += 1

    return shift_list
