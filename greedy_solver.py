# Michal Paulovic
# STU FIIT 2020
# AI assigment_2
# Python 3.7

import copy
import time
from queue import PriorityQueue
from itertools import count

from node import Node
from informant import Informant

#-----------------------------------------#
#           Getters section               #
#-----------------------------------------#
def get_conf():

    config_files = ['start.conf', 'final.conf']
    puzzles_list = []

    for file in config_files:
        puzzle = []
        file = open(file, 'r')

        if file.name == config_files[0]:
            print("Start puzzle:")
        else:
            print("Final Puzzle")

        for line in file:
            parsed_line = line.split()
            formated_line = []
            # type conversion 'str' -> 'int' if needed
            for character in parsed_line:
                if character.isdigit():
                    character = int(character)
                    formated_line.append(character)
                else:
                    formated_line.append(character)

            print(str(formated_line))
            puzzle.append(formated_line)

        puzzles_list.append(puzzle)
        file.close()
        print()

    return puzzles_list[0], puzzles_list[1]


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
                # Index difference in absolute value == distance to final position
                distance_element = (abs(m - searched_element[0])) + abs((n - searched_element[1]))
                distance_sum += distance_element
    return distance_sum


# Heuristika 3: Kombinácia predchádzajúcich odhadov
def get_heuristic_three(current_puzzle, final_puzzle):
    one = get_heuristic_one(current_puzzle, final_puzzle)
    two = get_heuristic_two(current_puzzle, final_puzzle)
    return one + two


# Heuristic function used by greedy algorithm
def heuristic(type, current_puzzle, final_puzzle):
    if type == 1:
        return get_heuristic_one(current_puzzle, final_puzzle)
    elif type == 2:
        return get_heuristic_two(current_puzzle, final_puzzle)
    elif type == 3:
        return get_heuristic_three(current_puzzle, final_puzzle)
    else:
        return get_heuristic_one(current_puzzle, final_puzzle) # DEFAULT heuristic, if not set

#-----------------------------------------#
# Operands section: UP, DOWN, LEFT, RIGHT #
#-----------------------------------------#
def move_up(puzzle, position):
    if position[0] == 0:
        return 0 # -> Illegal move
    else:
        new_puzzle = copy.deepcopy(puzzle)
        new_puzzle[position[0]][position[1]] = new_puzzle[position[0] - 1][position[1]]
        new_puzzle[position[0] - 1][position[1]] = 0
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

#------------------------------------------------#
#         Greedy algorithm implementation        #
#------------------------------------------------#
def greedy_algo(start_puzzle, final_puzzle, h_type):
    """
    :param start_puzzle: puzzle from .begin.conf
    :param final_puzzle:  puzzle from .final.conf
    :param h_type: type of heurisitic function
    :return: void function
    """
    start_time = time.time()
    pq = PriorityQueue()

    # Counts all generated Nodes
    counter = count()

    # Dicitonary of all visited nodes (key == value)
    # Used becuase of optimalization (can be list also)
    visited_nodes = {}

    # First node with special operand Start
    current_node = Node(start_puzzle, None, "S")

    # heuristic_value for start_puzzle
    heuristic_value = heuristic(h_type, current_node.puzzle, final_puzzle)

    # PriorityQueue now contains start_puzzle
    # data types --> tuple(tuple(heuristic_value, counter_visited), current_node)
    pq.put(((heuristic_value, next(counter)), current_node))

    # actual greedy algorithm implementation
    while True:
        if pq.empty(): # Unable to solve puzzle
            execution_time = time.time() - start_time
            return counter, -1, execution_time

        # Get Node with the lowest heuristic value
        current_node = pq.get()[1]

        if current_node.puzzle == final_puzzle: # Puzzle is solved
            execution_time = time.time() - start_time
            return counter, current_node, execution_time

        # list(list) -> tuple(tuple) <= because of optimalization
        hashable_puzzle = tuple([tuple(x) for x in current_node.puzzle])

        if hashable_puzzle not in visited_nodes:
            visited_nodes[hashable_puzzle] = hashable_puzzle
            zero_position = get_position(current_node.puzzle, 0)
            next_puzzle = []

            # avoiding repeating moves (last move was not UP, can go down)
            if current_node.last_operand != "U":
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
                    next_node = Node(next_puzzle, current_node, "L")
                    pq.put(((heuristic_value, next(counter)), next_node))


def main():
    screamer = Informant()
    start_puzzle, final_puzzle = get_conf()

    for heuristic_type in range(1,4):
        visited_nodes, final_node, execution_time = greedy_algo(start_puzzle, final_puzzle, heuristic_type)
        screamer.give_info(visited_nodes, final_node, execution_time, heuristic_type)

if __name__ == '__main__':
    main()
