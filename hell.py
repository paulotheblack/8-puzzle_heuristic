# Michal Paulovic
# STU FIIT 2020
# UI zadanie_2

# copy.deepcopy(list)
import copy
import time
from queue import PriorityQueue
from itertools import count

# Class Node (vrchol grafu)
from puzzle_node import Node


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
def get_heuristic_one(current_puzzle, final_puzzle):
    count = 0
    for m in range(len(current_puzzle)):
        for n in range(len(current_puzzle[m])):
            if current_puzzle[m][n] != final_puzzle[m][n]:
                count += 1
    return count


# Heuristika 2: Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície
def get_heuristic_two(current_puzzle, final_puzzle):
    distance_sum = 0
    for m in range(len(current_puzzle)):
        for n in range(len(current_puzzle[m])):
            if current_puzzle[m][n] != 0:
                searched_element = get_position(final_puzzle, current_puzzle[m][n])
                # rozdiel indexov prvku v absolutnej hodnote == vzdialenost od cielovej pozicie
                distance_element = (abs(m - searched_element[0])) + abs((n - searched_element[1]))
                distance_sum += distance_element
    return distance_sum


# Heuristika 3: Kombinácia predchádzajúcich odhadov
def get_heuristic_three(current_puzzle, final_puzzle):
    one = get_heuristic_one(current_puzzle, final_puzzle)
    two = get_heuristic_two(current_puzzle, final_puzzle)
    return one + two

# pomocna funckia pre greedy_algo
def heuristic(type, current_puzzle, final_puzzle):
    if type == 1:
        heuristic_value = get_heuristic_one(current_puzzle, final_puzzle)
    elif type == 2:
        heuristic_value = get_heuristic_two(current_puzzle, final_puzzle)
    elif type == 3:
        heuristic_value = get_heuristic_three(current_puzzle, final_puzzle)

    return heuristic_value


#-----------------------------------------#
# Operands section: UP, DOWN, LEFT, RIGHT #
#-----------------------------------------#
# position[0] = m_index
# position[1] = n_index
def move_up(puzzle, position):
    if position[0] == 0:
        return 0 # -> Illegal move
    else:
        new_puzzle = copy.deepcopy(puzzle)
        new_puzzle[position[0]][position[1]] = new_puzzle[position[0] - 1][position[1]]
        new_puzzle[position[0] - 1][position[1]] = 0
        # TEST PRINT
        # print("\nLegal move:")
        # for i in new_puzzle:
        #     print(i)
        return new_puzzle


def move_down(puzzle, position):
    if position[0] == (len(puzzle) - 1):
        return 0 # -> Illegal move
    else:
        new_puzzle = copy.deepcopy(puzzle)
        new_puzzle[position[0]][position[1]] = new_puzzle[position[0] + 1][position[1]]
        new_puzzle[position[0] + 1][position[1]] = 0
        return new_puzzle


def move_left(puzzle, position):
    if position[1] == 0:
        return 0 # -> Illegal move
    else:
        new_puzzle = copy.deepcopy(puzzle)
        new_puzzle[position[0]][position[1]] = new_puzzle[position[0]][position[1] - 1]
        new_puzzle[position[0]][position[1] - 1] = 0
        return new_puzzle


def move_right(puzzle, position):
    if position[1] == (len(puzzle[0]) - 1):
        return 0 # -> Illegal move
    else:
        new_puzzle = copy.deepcopy(puzzle)
        new_puzzle[position[0]][position[1]] = new_puzzle[position[0]][position[1] + 1]
        new_puzzle[position[0]][position[1] + 1] = 0
        return new_puzzle


def greedy_algo(start_puzzle, final_puzzle, heuristic_type = None):
    pq = PriorityQueue()
    counter = count() # counts all generated Nodes
    visited_nodes = {}  # dict, key == value
    route = [] # poradie operandov

    current_node = Node(start_puzzle, None, "S")

    # define heuristic in use
    h_type = 1
    # h_type = 2
    # h_type = 3

    # heuristic_value for start_puzzle
    heuristic_value = heuristic(h_type, current_node.puzzle, final_puzzle)

    # -> Tuple(Tuple(heuristic_value, counter_visited), current_puzzle)
    # PQ now contains start_puzzle
    pq.put(((heuristic_value, next(counter)), current_node))

    # POPIS
    # hashable_puzzle = tuple([tuple(row) for row in current_node.puzzle])
    # if hashable_puzzle not in visited_nodes:
    #     visited_nodes[hashable_puzzle] = hashable_puzzle

    # actual algo:
    while True:
        if pq.empty(): # return 0 if PQ is empty
            print("Visited: " + str(next(counter)) + " nodes")
            print("There's no solution, you are looking for :(")

        current_node = pq.get()[1]
        route.append(current_node.last_operand)


        if current_node.puzzle == final_puzzle:
            print("Visited: " + str(next(counter)) + " nodes")
            print("Operands order: " + str(route))
            break

        hashable_puzzle = tuple([tuple(x) for x in current_node.puzzle])

        if hashable_puzzle not in visited_nodes:
            visited_nodes[hashable_puzzle] = hashable_puzzle
            zero_position = get_position(current_node.puzzle, 0)
            next_puzzle = []

            if current_node.last_operand != "U": # ked bol UP nechcem ist dole <- cyklicke tahy
                next_puzzle = move_down(current_node.puzzle, zero_position)
                if next_puzzle:
                    heuristic_value = heuristic(h_type, next_puzzle, final_puzzle)
                    next_node = Node(next_puzzle, current_node, "D")
                    pq.put(((heuristic_value, next(counter)), next_node))

            if current_node.last_operand != "D":
                next_puzzle = move_up(current_node.puzzle, zero_position)
                if next_puzzle:
                    heuristic_value = heuristic(h_type, next_puzzle, final_puzzle)
                    next_node = Node(next_puzzle, current_node, "U")
                    pq.put(((heuristic_value, next(counter)), next_node))

            if current_node.last_operand != "L":
                next_puzzle = move_right(current_node.puzzle, zero_position)
                if next_puzzle:
                    heuristic_value = heuristic(h_type, next_puzzle, final_puzzle)
                    next_node = Node(next_puzzle, current_node, "R")
                    pq.put(((heuristic_value, next(counter)), next_node))

            if current_node.last_operand != "R":
                next_puzzle = move_left(current_node.puzzle, zero_position)
                if next_puzzle:
                    heuristic_value = heuristic(h_type, next_puzzle, final_puzzle)
                    next_node = Node(next_puzzle, zero_position, "L")
                    pq.put(((heuristic_value, next(counter)), next_node))








def main():
    start_time = time.time()

    start_puzzle, final_puzzle = get_start_final_puzzle()
    greedy_algo(start_puzzle,final_puzzle)

    end_time = time.time()
    time_exec = end_time - start_time
    print("Exection time: " + str(time_exec) + " [s]")


if __name__ == '__main__':
    main()
