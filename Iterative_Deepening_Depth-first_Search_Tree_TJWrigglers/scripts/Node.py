"""
Author: Bryan A. Asher
Date: 01/30/2019
"""

import Wrigglers
from Configurer import Configurer
from Segment import Segment
from Board import Board
from Logger import Logger


def my_segment_copy(segment_list):

    new_segment_list = []
    for i in range(len(segment_list)):
        location_copy = (segment_list[i].location[0], segment_list[i].location[1])
        symbol_copy = segment_list[i].symbol
        segment_id = Segment.id_counter
        Segment.id_counter += 1
        head_copy = segment_list[i].head
        tail_copy = segment_list[i].tail
        new_segment = Segment(location_copy, symbol_copy, segment_id, head_copy, tail_copy)
        new_segment_list.append(new_segment)

    return new_segment_list


def my_wriggler_copy(wriggler_list):

    new_wrigglers = []
    for i in range(len(wriggler_list)):
        new_wriggler = Wrigglers.Wrigglers()
        new_wriggler.segments = my_segment_copy(wriggler_list[i].segments)
        new_wrigglers.append(new_wriggler)
    return new_wrigglers


def my_copy(board):

    new_board = []
    for i in range(len(board.board)):
        temp = []
        for j in range(len(board.board[0])):
            temp.append(board.board[i][j])
        new_board.append(temp)
    new_obj = Board()
    new_obj.board = new_board
    new_obj.height = len(new_board)
    new_obj.width = len(new_board[0])
    new_wrigglers = my_wriggler_copy(board.wrigglers)
    new_obj.wrigglers = new_wrigglers

    return new_obj


class Node:
    """ A class to model nodes in a BFST. """

    # A class variable for differentiating Nodes
    id_counter = 1

    def __init__(self, board, parent_id, parent_cost, parent_move, parent_depth):

        self.board = board
        self.node_id = Node.id_counter
        self.parent_id = parent_id
        self.parent_move = [parent_move]  # [wriggler id, head(0)/tail(1) indicator, [x, y]]
        self.path_cost = parent_cost + 1
        self.depth = parent_depth + 1
        Node.id_counter += 1

    def is_goal(self):
        """ A function to check if board is in the desired configuration. """

        terminating_symbols = ['U', 'D', 'L', 'R']
        if self.board.board[-1][-1] == '0':
            return True
        elif self.board.board[-1][-1] in terminating_symbols:
            wriggler = Wrigglers.Wrigglers()
            wriggler.transmute([-1, -1, '.'], self.board.board)
            tail_location = wriggler.get_tail_location()

            if self.board.board[tail_location[0]][tail_location[1]] == '0':
                return True

        return False

    def children(self):
        """ A function to expand a state into it's subsequent available states."""
        children = []

        # find starting location of all Wrigglers
        head_locations = Wrigglers.find_wrigglers(self.board)

        # give control of wriggler board symbols to wriggler objects
        for j in range(len(head_locations)):
            self.board.wrigglers[j].transmute(head_locations[j], self.board.board)

        # expand current nodes action
        available_actions = self.board.get_actions(self.board.wrigglers)

        # take all available actions on copied boards
        for i in range(len(available_actions)):

            working_board = my_copy(self.board)
            working_wrigglers = working_board.wrigglers

            # find appropriate wriggler to preform action
            wriggler_id_from_action = available_actions[i][0]
            wriggler_index = Wrigglers.find_appropriate_wriggler(working_wrigglers, wriggler_id_from_action)

            # preform action
            working_wrigglers[wriggler_index].move(available_actions[i], working_board)

            # add new state to frontier; # Node(board, parent_id, parent_cost, parent_move, depth)
            new_node = Node(working_board, self.node_id, self.path_cost, available_actions[i], self.depth)
            children.append(new_node)

        return children

    def solution(self):

        # create logger
        logger = Logger(Configurer.solution_file)
        logger.solution(self)

