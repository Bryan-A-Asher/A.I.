"""
Author: Bryan A. Asher
Date: 01/28/2019
"""

import copy


def validate_next_symbol(board, segment_location):
    """ A function for checking location pointed to by current symbol. """

    directions = ['^', '>', 'v', '<', 'U', 'R', 'D', 'L']
    row, column = segment_location

    next_symbol = board[row][column]

    if next_symbol in directions or next_symbol.isdigit():
        return True
    else:
        print('Error: invalid segment ')
        exit(1)


class Segment:
    """ A class to model segments of a Wriggler. """

    # A class variable for differentiating segments
    id_counter = 1

    def __init__(self, location, symbol, segment_id, head=False, tail=False):
        self.head = head
        self.tail = tail
        self.anterior = None
        self.posterior = None
        self.symbol = symbol
        self.segment_id = segment_id
        Segment.id_counter += 1
        self.location = location

    def is_head(self):
        return self.head

    def is_tail(self):
        return self.tail

    def set_location(self, location):
        self.location = location

    def set_tail(self):
        self.tail = True

    def set_anterior_segment(self, neighbor):
        self.anterior = neighbor

    def set_posterior_segment(self, neighbor):
        self.posterior = neighbor

    def set_symbol(self, value):
        self.symbol = value

    def get_location(self):
        return self.location

    def get_symbol(self):
        return self.symbol

    def get_next_segment_location(self, board):
        """ A function for locating next associated segment of a Wriggler. """

        segment_location = copy.copy(self.location)
        row, column = segment_location

        segment_symbol = board[row][column]

        valid_segment = False

        if segment_symbol in ['U', '^']:
            row -= 1
            if validate_next_symbol(board, segment_location):
                valid_segment = True
        elif segment_symbol in ['D', 'v']:
            row += 1
            if validate_next_symbol(board, segment_location):
                valid_segment = True
        elif segment_symbol in ['L', '<']:
            column -= 1
            if validate_next_symbol(board, segment_location):
                valid_segment = True
        elif segment_symbol in ['R', '>']:
            column += 1
            if validate_next_symbol(board, segment_location):
                valid_segment = True
        elif segment_symbol.isdigit():
            valid_segment = True

        else:
            print('Error: invalid segment type')
            exit(1)

        if valid_segment:
            return [row, column]

    def print_segment_info(self):
        """ A function for printing all segment information. """

        print('Head:', self.head, '\t',
              'Tail:', self.tail, '\t',
              'Symbol:', self.symbol, '\t',
              'Anterior', self.anterior, '\t',
              'Posterior', self.posterior, '\t',
              'ID:', self.segment_id, '\t',
              'Location:', self.location, '\n\n')
