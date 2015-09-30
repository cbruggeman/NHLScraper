import copy

def mergeShiftData(shift_a,shift_b):
    """
    Take in two lists of lists of the form:
    [list_of_home_players, list_of_away_players, shift_start, shift_end]
    and merges them into one list
    """

    if not shift_a:
        return shift_b
    if not shift_b:
        return shift_a

    # Should already by sorted, but resort just in case
    # Since shift data is a list of lists of lists, we take
    # a deep copy to avoid unexpected behaviour
    shift_a = copy.deepcopy(sorted(shift_a, key = lambda x: x[2]))
    shift_b = copy.deepcopy(sorted(shift_b, key = lambda x: x[2]))

    a=0
    b=0

    La = len(shift_a)
    Lb = len(shift_b)
    
    current_a = shift_a[0]
    current_b = shift_b[0]

    shift_list = []

    while a<La or b<Lb:
        if a == La:
            shift_list.extend
        

        a_end = current_a[3]
        b_end = current_b[3]

        if a_end < b_end:
            combined_shift = [current_a[0]+current_b[0],
                                current_a[1] + current_b[1],
                                current_a[2],
                                a_end]
            a +=1
            current_b[2] = a_end

            shift_list.append(combined_shift)
            
            if a == La:
                shift_list.append(current_b)
                shift_list.extend(shift_b[b+1:])
                break

            current_a = shift_a[a]

        elif b_end < a_end:
            combined_shift = [current_a[0]+current_b[0],
                                current_a[1] + current_b[1],
                                current_a[2],
                                b_end]
            b +=1
            current_a[2] = b_end

            shift_list.append(combined_shift)

            if b == Lb:
                shift_list.append(current_a)
                shift_list.extend(shift_a[a+1:])
                break

            current_b = shift_b[b]

        else:
            a+=1
            b+=1
            combined_shift = [current_a[0]+current_b[0],
                                current_a[1] + current_b[1],
                                current_a[2],
                                a_end]

            shift_list.append(combined_shift)

            if a == La:
                shift_list.extend(shift_b[b+1:])
                break

            if b == Lb:
                shift_list.extend(shift_a[a+1:])
                break

            current_b = shift_b[b]
            current_a = shift_a[a]

        

    return shift_list


# sa=[[['bob','fred'],[],1,5],[['bob','sue'],['al'],5,10]]
# sb=[[['sally','igor'],[],1,2],[['alex'],[],2,10]]

# mergeShiftData(sa,sb)