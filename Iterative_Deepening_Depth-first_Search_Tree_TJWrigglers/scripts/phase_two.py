"""
Author: Bryan A. Asher
Date: 01/27/2019
Brief: A Iterative Deepening Depth-First Tree Search pathfinder program for the Wrigglers game.
"""

from Configurer import Configurer
from Board import Board
from Node import Node
from search import iterative_deepening_depth_first_tree_search
from Logger import Logger
import sys
import time

if __name__ == '__main__':

    # start program timer
    Logger.start_time = time.time()
    # print(Logger.start_time)

    # read in configuration data
    config = Configurer(sys.argv)
    config.read_file()

    # create board
    board = Board()
    config.setup(board)
    # board.print_board()

    # initialize problem state
    root = Node(board, None, 0, None, -1)  # Node(board, parent_id, parent_cost, parent_move, parent_depth)

    # perform search
    iterative_deepening_depth_first_tree_search(root)


