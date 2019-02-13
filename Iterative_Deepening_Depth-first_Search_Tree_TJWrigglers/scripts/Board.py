"""
Author: Bryan A. Asher
Date: 01/27/2019
"""

from numpy import matrix  # for pretty print
import Wrigglers


class Board:
    """ A class for modeling TJ Wrigglers game board. """

    def __init__(self):
        """ A function to initialize a basic Board object. """

        self.width = None
        self.height = None
        self.board = []
        self.wrigglers = []

    def is_symbol(self, new_location, symbol):
        """ A function that returns true if a specific cell on the game board is a specified symbol. """

        if self.board[new_location[0]][new_location[1]] == symbol:
            return True
        else:
            return False

    def set_board(self, board_info, number_wrigglers):
        """ A function to do the initial configuration of a game board. """

        self.board = board_info
        self.height = len(board_info)
        self.width = len(board_info[0])

        for _ in range(int(number_wrigglers)):
            self.wrigglers.append(Wrigglers.Wrigglers())

    def print_board(self):
        """ A function to pretty print a game board. """

        print(matrix(self.board))

    def get_valid_locations(self, reference_location, wriggler_id, indicator):
        """ A function for testing move viability on adjacent board locations. """

        up, down, left, right = None, None, None, None

        if reference_location[0] - 1 > -1:
            up = [reference_location[0] - 1, reference_location[1]]

        if reference_location[0] + 1 < self.height:
            down = [reference_location[0] + 1, reference_location[1]]

        if reference_location[1] - 1 > - 1:
            left = [reference_location[0], reference_location[1] - 1]

        if reference_location[1] + 1 < self.width:
            right = [reference_location[0], reference_location[1] + 1]

        locations = []
        directions = [up, down, left, right]

        for direction in directions:
            valid_location = False
            if direction is not None:
                valid_location = self.is_symbol(direction, 'e')
            if valid_location:
                locations.append([wriggler_id, indicator, direction])

        return locations

    def get_actions(self, wrigglers):
        """ A function to find available board moves for given Wrigglers. """

        available_actions = []  # [[id, head(0)/tail(1) body_indicator [x, y]], ...]
        for i in range(len(wrigglers)):
            head_location = wrigglers[i].get_head_location()
            tail_location = wrigglers[i].get_tail_location()
            wriggler_id = wrigglers[i].get_id()

            available_actions += self.get_valid_locations(head_location, wriggler_id, 0)
            available_actions += self.get_valid_locations(tail_location, wriggler_id, 1)

        return available_actions
