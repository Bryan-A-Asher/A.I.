"""
Author: Bryan A. Asher
Date: 01/27/2019
"""

from numpy import matrix  # for pretty print


def is_adjacent(reference_location, new_location):
    """ A function for checking if a location is next to another. """

    adjacent = False
    if reference_location[0] - 1 == new_location[0] and reference_location[1] == new_location[1]:
        adjacent = True
    elif reference_location[0] + 1 == new_location[0] and reference_location[1] == new_location[1]:
        adjacent = True
    elif reference_location[0] == new_location[0] and reference_location[1] - 1 == new_location[1]:
        adjacent = True
    elif reference_location[0] == new_location[0] and reference_location[1] + 1 == new_location[1]:
        adjacent = True

    return adjacent


class Board:
    """ A class for modeling TJ Wrigglers game board. """

    def __init__(self):
        """ A function to initialize a basic Board object. """

        self.width = None
        self.height = None
        self.board = []

    def is_symbol(self, new_location, symbol):
        """ A function that returns true if a specific cell on the game board is a specified symbol. """

        if self.board[new_location[0]][new_location[1]] == symbol:
            return True
        else:
            return False

    def get_board(self):
        """ A function to return the 2D array that represents the game board. """

        return self.board

    def get_num_columns(self):
        """ A function to return the number of columns on the game board. """

        return self.width

    def get_num_rows(self):
        """ A function to return the number of rows on the game board. """

        return self.height

    def get_symbol(self, location):
        """ A function to return the symbol on a specific cell of the game board. """

        return self.board[location[0]][location[1]]

    def set_board(self, board_info):
        """ A function to do the initial configuration of a game board. """

        self.board = board_info
        self.height = len(board_info)
        self.width = len(board_info[0])

    def print_board(self):
        """ A function to pretty print a game board. """

        print(matrix(self.board))

    def is_goal_state(self):
        """ A function to check if board is in the desired configuration. """

        if self.board[-1][-1] in ['U', 'D', 'L', 'R']:
            return True

        return False

    def get_valid_locations(self, reference_location, wriggler_id, indicator):
        """ A function for testing move viability on adjacent board locations. """

        up, down, left, right = None, None, None, None

        if reference_location[0] - 1 > -1:
            up = [reference_location[0] - 1, reference_location[1]]

        if reference_location[0] + 1 < self.get_num_rows():
            down = [reference_location[0] + 1, reference_location[1]]

        if reference_location[1] - 1 > - 1:
            left = [reference_location[0], reference_location[1] - 1]

        if reference_location[1] + 1 < self.get_num_columns():
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

        available_actions = []  # [[id, head(0)/tail(1) indicator [x, y]], ...]
        for i in range(len(wrigglers)):
            head_location = wrigglers[i].get_head_location()
            tail_location = wrigglers[i].get_tail_location()
            wriggler_id = wrigglers[i].get_id()

            available_actions += self.get_valid_locations(head_location, wriggler_id, 0)
            available_actions += self.get_valid_locations(tail_location, wriggler_id, 1)

        return available_actions
