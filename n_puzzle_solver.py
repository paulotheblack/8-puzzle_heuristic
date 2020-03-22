# Michal Paulovic
# STU FIIT 2020
# AI assigment_2

import copy
import time
from queue import PriorityQueue
from itertools import count

#-----------------------------------------#
#           Getters section               #
#-----------------------------------------#
def get_conf(file):
    puzzle = []
    file = open(file, 'r')

    for line in file:
        parsed_line = line.split()
        formated_line = []

        # type conversion 'str' -> 'int' if needed
        for item in parsed_line:
            if item.isdigit():
                item = int(item)
                formated_line.append(item)
            else:
                formated_line.append(item)
        puzzle.append(formated_line)

    file.close()
    return puzzle


def get_start_final_puzzle():
    start_puzzle = get_conf("start.conf")
    print("START_PUZZLE: " + str(len(start_puzzle)) + "x" + str(len(start_puzzle[0])))
    for i in start_puzzle:
        print(i)

    final_puzzle = get_conf("final.conf")
    print("\nFINAL_PUZZLE")
    for i in final_puzzle:
        print(i)

    return start_puzzle, final_puzzle


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

# Heuristic function used by greedy algorithm
def heuristic(type, current_puzzle, final_puzzle):
    if type == 1:
        heuristic_value = get_heuristic_one(current_puzzle, final_puzzle)
    elif type == 2:
        heuristic_value = get_heuristic_two(current_puzzle, final_puzzle)
    elif type == 3:
        heuristic_value = get_heuristic_three(current_puzzle, final_puzzle)
    else:
        return 1 # DEFAULT heuristic, if not set

    return heuristic_value


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
# Class Node = Graph Node/Vertice representation #
#------------------------------------------------#
class Node:
    def __init__(self, puzzle, parent = None, last_operand = ""):
        self.puzzle = copy.deepcopy(puzzle)
        self.parent = parent
        self.last_operand = last_operand


#-----------------------------------------#
#     Greedy algorithm implementation     #
#-----------------------------------------#
def greedy_algo(start_puzzle, final_puzzle, h_type):
    """
    :param start_puzzle: puzzle from .begin.conf
    :param final_puzzle:  puzzle from .final.conf
    :param h_type: type of heurisitic function
    :return: void function
    """
    pq = PriorityQueue()

    # Counts all generated Nodes
    counter = count()

    # Dicitonary of all visited nodes (key == value)
    # Used becuase of optimalization (can be list also)
    visited_nodes = {}

    # List of operands used to achieve final_puzzle
    route = []

    """
    Class Node
        puzzle::list
        parent::Node
        last_operand::string (U/D/L/R) S = start
    """
    current_node = Node(start_puzzle, None, "S")

    # heuristic_value for start_puzzle
    heuristic_value = heuristic(h_type, current_node.puzzle, final_puzzle)

    # PriorityQueue now contains start_puzzle
    # -> tuple(tuple(heuristic_value, counter_visited), current_puzzle)
    pq.put(((heuristic_value, next(counter)), current_node))

    # actual greedy algorithm implementation
    while True:
        if pq.empty(): # Unable to solve puzzle
            return counter, "There's no solution, you are looking for :("

        # Get Node with the lowest heuristic value
        current_node = pq.get()[1]
        route.append(current_node.last_operand)


        if current_node.puzzle == final_puzzle:
            return counter, route

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
                    next_node = Node(next_puzzle, zero_position, "L")
                    pq.put(((heuristic_value, next(counter)), next_node))


def main():
    start_puzzle, final_puzzle = get_start_final_puzzle()

    # start execution timer
    start_time = time.time()
    # change last paramater of greedy_algo to change heuritics in use (1/2/3)
    visited_nodes, route = greedy_algo(start_puzzle, final_puzzle, 3)
    # stop execution
    execution_time = time.time() - start_time

    print("\nVisited " + str(next(visited_nodes) - 1) + " Nodes")
    print("Route: " + str(route))
    print("Exection time: " + str(execution_time) + " [s]")


if __name__ == '__main__':
    main()
