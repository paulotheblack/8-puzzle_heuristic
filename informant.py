class Informant:

    @staticmethod
    def give_info(visited_nodes, final_node, execution_time, heuristic_type):
        if final_node == -1:
            print("There is no solution you are looking for :(")
            exit(-1)

        route_operand = []
        route_nodes = [final_node]

        # get route_operand via each parent Node
        while final_node.parent is not None:
            route_operand.append(final_node.last_operand)
            route_nodes.append(final_node.parent)
            final_node = final_node.parent

        route_operand.append("S")  # Start operand <=> node.parent == None
        route_operand.reverse()
        route_nodes.reverse()

        # Solution as file output (in same directory)
        # .txt <= compatibilty reason
        file = open("n_puzzle_" + str(heuristic_type) + str(".txt"), "w")
        for node in route_nodes:
            if node.last_operand == "S":
                file.write("Solved using heuristic "
                           + str(heuristic_type)
                           + ".\nTotal " + str(len(route_nodes))
                           + " nodes on route to final puzzle."
                           + "\nGenerated in total " + str(next(visited_nodes) - 1)
                           + " nodes." + "\nExecution time: " + str(execution_time)
                           + "[s] (RT)\nStarting point:\n")
            else:
                file.write("\n")
                file.write("\nOperand used: " + node.last_operand)
            for i in node.puzzle:
                file.write("\n" + str(i))

        # Terminal info
        print("\nHeuristic " + str(heuristic_type)
              + ":\nIt takes " + str(len(route_nodes)) + " moves to solve puzzle."
              + "\nRead file '" + str(file.name)
              + "' for more information.")
        file.close()
