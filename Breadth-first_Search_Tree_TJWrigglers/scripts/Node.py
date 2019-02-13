"""
Author: Bryan A. Asher
Date: 01/30/2019
"""


class Node:
    """ A class to model nodes in a BFST. """

    # A class variable for differentiating Nodes
    id_counter = 1

    def __init__(self, board, parent_id, parent_cost, parent_move):
        self.board = board
        self.node_id = Node.id_counter
        self.parent_id = parent_id
        self.parent_move = parent_move  # [wriggler id, head(0)/tail(1) indicator, [x, y]]
        self.avail_actions = None       # [wriggler id, head(0)/tail(1) indicator, [x, y], ...]
        self.path_cost = parent_cost + 1
        Node.id_counter += 1

    def get_id(self):
        return self.node_id

    def get_cost(self):
        return self.path_cost
