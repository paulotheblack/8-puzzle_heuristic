import copy

# Vrchol grafu
class Node:
    def __init__(self, puzzle, parent = None, last_operand = ""):
        self.puzzle = copy.deepcopy(puzzle)
        self.parent = parent
        self.last_operand = last_operand