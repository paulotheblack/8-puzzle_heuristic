# Michal Paulovic
# STU FIIT 2020
# UI zadanie_2

# copy.deepcopy(list)
import copy
from queue import PriorityQueue


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
# return start_puzzle, final_puzzle
def get_start_final_puzzle():
    start_puzzle = get_conf(".begin.conf")
    # TEST PRINT
    print("START_PUZZLE: " + str(len(start_puzzle)) + "x" + str(len(start_puzzle[0])))
    for i in start_puzzle:
        print(i)

    final_puzzle = get_conf(".final.conf")
    # TEST PRINT
    # print("\nFINAL_PUZZLE:")
    # for i in final_puzzle:
    #     print(i)

    return start_puzzle, final_puzzle


# get position of desired element in puzzle
# return array[M_index, N_index]
def get_position(puzzle, element):
    for m in range(len(puzzle)):
        for n in range(len(puzzle[m])):
            if puzzle[m][n] == element:
                return [m, n]


#-----------------------------------------#
#          Heuristics section             #
#-----------------------------------------#
# Heuristika 1: Počet políčok, ktoré nie sú na svojom mieste
def get_heuristic_one(parent_puzzle, new_puzzle):
    count = 0
    for m in range(len(parent_puzzle)):
        for n in range(len(parent_puzzle[m])):
            if parent_puzzle[m][n] != new_puzzle[m][n]:
                count += 1
    return count


# Heuristika 2: Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície
def get_heuristic_two(parent_puzzle, new_puzzle):
    distance_sum = 0
    for m in range(len(parent_puzzle)):
        for n in range(len(parent_puzzle[m])):
            if parent_puzzle[m][n] != 0:
                searched_element = get_position(new_puzzle, parent_puzzle[m][n])
                # rozdiel indexov prvku v absolutnej hodnote == vzdialenost od cielovej pozicie
                distance_element = (abs(m - searched_element[0])) + abs((n - searched_element[1]))
                distance_sum += distance_element
    return distance_sum


# Heuristika 3: Kombinácia predchádzajúcich odhadov
def get_heuristic_three(parent_puzzle, new_puzzle):
    one = get_heuristic_one(parent_puzzle, new_puzzle)
    two = get_heuristic_two(parent_puzzle, new_puzzle)
    return one + two


#-----------------------------------------#
# Operands section: UP, DOWN, LEFT, RIGHT #
#-----------------------------------------#
# position[0] = m_index
# position[1] = n_index
def move_up(parent_puzzle, position):
    if position[0] == 0:
        return 0 # -> Illegal move
    else:
        new_puzzle = copy.deepcopy(parent_puzzle)
        new_puzzle[position[0]][position[1]] = new_puzzle[position[0] - 1][position[1]]
        new_puzzle[position[0] - 1][position[1]] = 0
        # TEST PRINT
        # print("\nLegal move:")
        # for i in new_puzzle:
        #     print(i)
        return new_puzzle


def move_down(parent_puzzle, position):
    if position[0] == (len(parent_puzzle) - 1):
        return 0 # -> Illegal move
    else:
        new_puzzle = copy.deepcopy(parent_puzzle)
        new_puzzle[position[0]][position[1]] = new_puzzle[position[0] + 1][position[1]]
        new_puzzle[position[0] + 1][position[1]] = 0
        return new_puzzle


def move_left(parent_puzzle, position):
    if position[1] == 0:
        return 0 # -> Illegal move
    else:
        new_puzzle = copy.deepcopy(parent_puzzle)
        new_puzzle[position[0]][position[1]] = new_puzzle[position[0]][position[1] - 1]
        new_puzzle[position[0]][position[1] - 1] = 0
        return new_puzzle


def move_right(parent_puzzle, position):
    if position[1] == (len(parent_puzzle[0]) - 1):
        return 0 # -> Illegal move
    else:
        new_puzzle = copy.deepcopy(parent_puzzle)
        new_puzzle[position[0]][position[1]] = new_puzzle[position[0]][position[1] + 1]
        new_puzzle[position[0]][position[1] + 1] = 0
        return new_puzzle


def main():
    # JUST FOR TESTING PURPOSE
    # start_puzzle, final_puzzle = get_start_final_puzzle()
    # count = get_heuristic_one(start_puzzle, final_puzzle)
    # print("\nHeuristic 1: count_sum = " + str(count))
    # distance = get_heuristic_two(start_puzzle, final_puzzle)
    # print("\nHeuristic 2: distance_sum = " + str(distance))
    #
    # zero_position = get_position(start_puzzle, 0)
    # print("Zero position at:" + str(zero_position))
    #
    # new_puzzle = move_up(start_puzzle, zero_position)
    # print("\n" + str(new_puzzle))
    # new_puzzle = move_down(start_puzzle, zero_position)
    # print("\n" + str(new_puzzle))
    # new_puzzle = move_left(start_puzzle, zero_position)
    # print("\n" + str(new_puzzle))
    # new_puzzle = move_right(start_puzzle, zero_position)
    # print("\n" + str(new_puzzle))



if __name__ == '__main__':
    main()
