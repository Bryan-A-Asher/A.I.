"""
Author: Bryan A. Asher
Date: 01/28/2019
"""


def validate_next_symbol(board, segment_location):
    """ A function for checking location pointed to by current symbol. """

    directions = ['^', '>', 'v', '<', 'U', 'R', 'D', 'L']

    row, column = segment_location
    next_symbol = board[row][column]

    if next_symbol in directions or next_symbol.isdigit():
        return True
    else:
        print('Error: invalid segment ', next_symbol)
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

    def get_next_segment_location(self, board):
        """ A function for locating next associated segment of a Wriggler. """

        row, column = self.location
        segment_symbol = board[row][column]
        valid_segment = False

        if segment_symbol == 'U' or segment_symbol == '^':
            row -= 1
            if validate_next_symbol(board, [row, column]):
                valid_segment = True

        elif segment_symbol == 'D' or segment_symbol == 'v':
            row += 1
            if validate_next_symbol(board, [row, column]):
                valid_segment = True

        elif segment_symbol == 'L' or segment_symbol == '<':
            column -= 1
            if validate_next_symbol(board, [row, column]):
                valid_segment = True

        elif segment_symbol == 'R' or segment_symbol == '>':
            column += 1
            if validate_next_symbol(board, [row, column]):
                valid_segment = True

        elif segment_symbol.isdigit():
            valid_segment = True

        else:
            print('Error: invalid segment type', segment_symbol)
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
