"""
Author: Bryan A. Asher
Date: 01/27/2019
Brief: A Breadth-First Tree Search pathfinder program for the Wrigglers game.
"""

from Configurer import Configurer
from Board import Board
from Logger import Logger
from Node import Node
import Wrigglers
import sys
import time
import copy

# todo code optimization and clean up

if __name__ == '__main__':

    # start program timer
    start_time = time.time()

    # read in configuration data
    config = Configurer()
    config.read_file(sys.argv[1])

    # create board
    board = Board()
    config.setup(board)
    board.print_board()

    # create logger
    logger = Logger('./logs/phase_one_solution.txt')

    # create Wrigglers
    number_wrigglers = int(config.get_num_wrigglers())

    wrigglers = []
    for _ in range(number_wrigglers):
        wrigglers.append(Wrigglers.Wrigglers())

    # used as que
    frontier = []

    # used for tracking
    visited = {}

    # used to determine if goal is found:)
    goal_found = False

    # initialize the frontier
    root = Node(board, None, 0, None)  # Node(board, parent_id, parent_cost, parent_move)
    frontier.append(root)

    while frontier:

        # choose leaf node and remove from frontier
        current_node = frontier.pop(0)
        visited[current_node.node_id] = current_node

        # if node contains goal state return corresponding solution
        goal_found = current_node.board.is_goal_state()
        logger.check_goal(goal_found, current_node, visited, start_time)

        # find starting location of all Wrigglers
        head_locations = Wrigglers.find_wrigglers(current_node.board)

        # give control of wriggler board symbols to wriggler objects
        for j in range(len(head_locations)):
            wrigglers[j].transmute(head_locations[j], current_node.board.get_board())

        # expand current nodes action
        available_actions = current_node.board.get_actions(wrigglers)

        # take all available actions on copied boards
        for i in range(len(available_actions)):
            working_board = copy.deepcopy(current_node.board)
            working_wrigglers = copy.deepcopy(wrigglers)

            # find appropriate wriggler to preform action
            wriggler_id_from_action = available_actions[i][0]
            wriggler_move_from_action = available_actions[i][-1]
            wriggler_index = Wrigglers.find_appropriate_wriggler(working_wrigglers, wriggler_id_from_action)

            # preform action
            working_wrigglers[wriggler_index].move(available_actions[i][-1], working_board)

            # add new state to frontier; # Node(board, parent_id, parent_cost, parent_move)
            new_node = Node(working_board, current_node.get_id(), current_node.get_cost(), available_actions[i])
            frontier.append(new_node)

    # if frontier is empty and goal not found return fail
    if not goal_found:
        logger.fail()

