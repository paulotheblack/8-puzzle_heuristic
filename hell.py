# Michal Paulovic
# STU FIIT 2020
# UI zadanie_2

# copy.deepcopy(list)
import copy


# reads config file
# return puzzle_list
def get_conf(file):
    puzzle = []
    file = open(file, 'r')

    for line in file:
        parsed_line = line.split()
        formated_line = []

        # type conversion 'str' -> 'int'
        for item in parsed_line:
            if item.isdigit():
                item = int(item)
                formated_line.append(item)
            else:
                formated_line.append(item)
        puzzle.append(formated_line)

    file.close()
    return puzzle


# STDOUT information
# return start_state, final_state
def get_start_final_state():
    start_state = get_conf(".begin.conf")
    # TEST PRINT
    print("START_STATE: " + str(len(start_state)) + "x" + str(len(start_state[0])))
    for i in start_state:
        print(i)

    final_state = get_conf(".final.conf")
    # TEST PRINT
    # print("\nFINAL STATE ")
    # for i in final_state:
    #     print(i)

    return start_state, final_state


# get position of desired element in puzzle
# return array[M_index, N_index]
def get_position(state, element):
    for m in range(len(state)):
        for n in range(len(state[m])):
            if state[m][n] == element:
                return [m, n]


#-----------------------------------------#
#          Heuristics section             #
#-----------------------------------------#
# Heuristika 1: Počet políčok, ktoré nie sú na svojom mieste
def get_heuristic_one(start_state, final_state):
    count = 0
    for m in range(len(start_state)):
        for n in range(len(start_state[m])):
            if start_state[m][n] != final_state[m][n]:
                count += 1
    return count


# Heuristika 2: Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície
def get_heuristic_two(start_state, final_state):
    distance_sum = 0
    for m in range(len(start_state)):
        for n in range(len(start_state[m])):
            if start_state[m][n] != 0:
                searched_element = get_position(final_state, start_state[m][n])
                # rozdiel indexov prvku v absolutnej hodnote == vzdialenost od cielovej pozicie
                distance_element = (abs(m - searched_element[0])) + abs((n - searched_element[1]))
                distance_sum += distance_element
    return distance_sum


#-----------------------------------------#
# Operands section: UP, DOWN, LEFT, RIGHT #
#-----------------------------------------#
# position[0] = m_index
# position[1] = n_index
def move_up(parent_state, position):
    if position[0] == 0:
        return -1 # -> Illegal move
    else:
        new_state = copy.deepcopy(parent_state)
        new_state[position[0]][position[1]] = new_state[position[0] - 1][position[1]]
        new_state[position[0] - 1][position[1]] = 0
        # TEST PRINT
        # print("\nLegal move:")
        # for i in new_state:
        #     print(i)
        return new_state


def move_down(parent_state, position):
    if position[0] == (len(parent_state) - 1):
        return -1 # -> Illegal move
    else:
        new_state = copy.deepcopy(parent_state)
        new_state[position[0]][position[1]] = new_state[position[0] + 1][position[1]]
        new_state[position[0] + 1][position[1]] = 0
        return new_state


def move_left(parent_state, position):
    if position[1] == 0:
        return -1 # -> Illegal move
    else:
        new_state = copy.deepcopy(parent_state)
        new_state[position[0]][position[1]] = new_state[position[0]][position[1] - 1]
        new_state[position[0]][position[1] - 1] = 0
        return new_state


def move_right(parent_state, position):
    if position[1] == (len(parent_state[0]) - 1):
        return -1 # -> Illegal move
    else:
        new_state = copy.deepcopy(parent_state)
        new_state[position[0]][position[1]] = new_state[position[0]][position[1] + 1]
        new_state[position[0]][position[1] + 1] = 0
        return new_state


def main():
    # JUST FOR TESTING PURPOSE
    start_state, final_state = get_start_final_state()
    count = get_heuristic_one(start_state, final_state)
    print("\nHeuristic 1: count_sum = " + str(count))
    distance = get_heuristic_two(start_state, final_state)
    print("\nHeuristic 2: distance_sum = " + str(distance))

    zero_position = get_position(start_state, 0)
    print("Zero position at:" + str(zero_position))

    new_state = move_up(start_state, zero_position)
    print("\n" + str(new_state))
    new_state = move_down(start_state, zero_position)
    print("\n" + str(new_state))
    new_state = move_left(start_state, zero_position)
    print("\n" + str(new_state))
    new_state = move_right(start_state, zero_position)
    print("\n" + str(new_state))



if __name__ == '__main__':
    main()
