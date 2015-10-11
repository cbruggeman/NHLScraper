import copy
from .shift_class import Shift

def merge_shift_data(list_a,list_b):
    """
    Take in two lists of lists of the form:
    [list_of_home_players, list_of_away_players, shift_start, shift_end]
    and merges them into one list
    """

    if not list_a:
        return list_b
    if not list_b:
        return list_a

    # Should already by sorted, but resort just in case
    # Since shift data is a list of lists of lists, we take
    # a deep copy to avoid unexpected behaviour
    list_a = sorted(list_a, key = lambda x: x.start)
    list_b = sorted(list_b, key = lambda x: x.start)

    a = 0
    b = 0

    La = len(list_a)
    Lb = len(list_b)
    
    current_a = list_a[0]
    current_b = list_b[0]

    shift_list = []
    while a<La or b<Lb:
        

        a_end = current_a.end
        b_end = current_b.end
        a_start = current_a.start
        b_start = current_b.start

        # a starts earlier
        if a_start < b_start:
            # a ends before b starts
            if a_end <= b_start:
                shift_list.append(current_a)
                a += 1
                if a == La:
                    shift_list.append(current_b)
                    shift_list.extend(list_b[b+1:])
                    break
                current_a = list_a[a]

            else:
                new_shift = copy.deepcopy(current_a)
                new_shift.end = b_start
                current_a.start = b_start
                shift_list.append(new_shift)

        # b starts earlier
        elif b_start < a_start:

            if b_end <= a_start:
                shift_list.append(current_b)
                b += 1
                if b == Lb:
                    shift_list.append(current_b)
                    shift_list.extend(list_a[a+1:])
                    break
                current_b = list_b[b]

            else:
                new_shift = copy.deepcopy(current_b)
                new_shift.end = a_start
                current_b.start = a_start
                shift_list.append(new_shift)

        # Starting at the same time
        else:
            if a_end < b_end:
                combined_shift = Shift()
                combined_shift.home_players = current_a.home_players + copy.deepcopy(current_b.home_players)
                combined_shift.away_players = current_a.away_players + copy.deepcopy(current_b.away_players)
                combined_shift.start = a_start
                combined_shift.end = a_end
                a +=1
                current_b.start = a_end

                shift_list.append(combined_shift)
                
                if a == La:
                    shift_list.append(current_b)
                    shift_list.extend(list_b[b+1:])
                    break

                current_a = list_a[a]

            elif b_end < a_end:
                combined_shift = Shift()
                combined_shift.home_players = copy.deepcopy(current_a.home_players) + copy.deepcopy(current_b.home_players)
                combined_shift.away_players = copy.deepcopy(current_a.away_players) + copy.deepcopy(current_b.away_players)
                combined_shift.start = a_start
                combined_shift.end = b_end
                b +=1
                current_a.start = b_end

                shift_list.append(combined_shift)

                if b == Lb:
                    shift_list.append(current_a)
                    shift_list.extend(list_a[a+1:])
                    break

                current_b = list_b[b]

            else:
                a += 1
                b += 1
                combined_shift = Shift()
                combined_shift.home_players = current_a.home_players + copy.deepcopy(current_b.home_players)
                combined_shift.away_players = current_a.away_players + copy.deepcopy(current_b.away_players)
                combined_shift.start = a_start
                combined_shift.end = a_end

                shift_list.append(combined_shift)

                if a == La:
                    shift_list.extend(list_b[b+1:])
                    break

                if b == Lb:
                    shift_list.extend(list_a[a+1:])
                    break

                current_b = list_b[b]
                current_a = list_a[a]


    return shift_list


# s1 = Shift()
# s1.home_players=['bob','fred']
# s1.start = 1
# s1.end = 5
# s2 = Shift()
# s2.home_players = ['bob','sue']
# s2.away_players = ['al']
# s2.start = 5
# s2.end = 10
# s3 = Shift()
# s3.home_players = ['sally','igor']
# s3.start = 1
# s3.end = 2
# s4 = Shift()
# s4.home_players = ['alex']
# s4.start = 4
# s4.end = 10

# sa = [s1,s2]
# sb = [s3,s4]
