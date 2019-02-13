"""
Author: Bryan A. Asher
Date: 01/27/2019
"""
# todo deal with anterior and posterior updates

from Segment import Segment
from Board import is_adjacent


def find_wrigglers(board):
    """ A function for locating initial head locations of all Wrigglers. """

    head_locations = []

    for i in range(board.get_num_rows()):
        for j in range(board.get_num_columns()):
            symbol = board.get_symbol([i, j])
            if symbol in ['U', 'D', 'L', 'R']:
                head_locations.append([i, j, symbol])

    return head_locations


def find_appropriate_wriggler(wrigglers, wriggler_id):
    """ A function that returns the index of a Wriggler in an list given it's id"""

    for i in range(len(wrigglers)):
        if wrigglers[i].get_id() == wriggler_id:
            return i


def form_wrigglers(board):
    """ A function for associating segments of a Wriggler with each other. """

    wrigglers = []

    for i in range(len(Wrigglers.initial_wrigglers_head_locations)):
        # create wriggler object
        wrigg = Wrigglers()

        # grab relevant info
        segment_location = Wrigglers.initial_wrigglers_head_locations[i][:2]
        head_symbol = Wrigglers.initial_wrigglers_head_locations[i][2]

        # create a segment object
        head_segment = Segment(segment_location, head_symbol, Segment.id_counter, True)
        Segment.id_counter += 1

        # add to wriggler's 'body'
        wrigg.segments.append(head_segment)

        # complete the rest of the links
        wrigg.fill_segment_list(board.get_board())

        wrigg.connect_segments()

        wrigglers.append(wrigg)

    return wrigglers


def fix_directions(segment_list, board):

    direction = None
    for i in range(len(segment_list)):

        first_seg = segment_list[i].get_location()
        if i != len(segment_list) - 1:
            second_seg = segment_list[i+1].get_location()
        else:
            break

        if first_seg[0] > second_seg[0]:
            if segment_list[i].is_head():
                direction = 'U'
            else:
                direction = '^'
        elif first_seg[0] < second_seg[0]:
            if segment_list[i].is_head():
                direction = 'D'
            else:
                direction = 'v'
        elif first_seg[1] > second_seg[1]:
            if segment_list[i].is_head():
                direction = 'L'
            else:
                direction = '<'
        elif first_seg[1] < second_seg[1]:
            if segment_list[i].is_head():
                direction = 'R'
            else:
                direction = '>'

        board.board[first_seg[0]][first_seg[1]] = direction


class Wrigglers:
    """ A class to model the Wrigglers from the TJ Wrigglers game. """

    # A class variable for differentiating Wrigglers
    id_counter = 1

    # A class variable for tracking individual Wrigglers
    initial_wrigglers_head_locations = []

    def __init__(self):
        self.length = None
        self.wriggler_id = None
        self.segments = []

    def get_head_location(self):
        """ A function for locating the head a specific Wriggler. """
        body = self.get_segments()
        head_location = None
        for i in range(len(body)):
            if body[i].is_head():
                head_location = body[i].get_location()

        return head_location

    def get_tail_location(self):
        """ A function for locating the tail a specific Wriggler. """
        body = self.get_segments()
        tail_location = None
        for i in range(len(body)):
            if body[i].is_tail():
                tail_location = body[i].get_location()

        return tail_location

    def get_id(self):
        """ A function for locating the id a specific Wriggler. """
        body = self.get_segments()
        wriggler_id = None
        for i in range(len(body)):
            if body[i].is_tail():
                wriggler_id = body[i].get_symbol()

        return wriggler_id

    def get_segments(self):
        return self.segments

    def get_len(self):
        return self.length

    def transmute(self, head_location, board):
        """ A function that allows a Wriggler object to take control of Wriggler board symbols. """

        # Segment(location, symbol, segment_id, head=False, tail=False)
        head = Segment(head_location[:2], head_location[2], Segment.id_counter, True)

        self.segments = [head]
        self.fill_segment_list(board)

    def fill_segment_list(self, board):
        """ A function to define and record the location of Wriggler segments on a board. """

        # check if Wriggler present
        if not self.segments:
            print('Error: no Wriggler present!')
            exit(1)

        # get location of all Wriggler segments
        additional_segments = True
        while additional_segments:
            next_segment_location = self.segments[-1].get_next_segment_location(board)
            next_symbol = board[next_segment_location[0]][next_segment_location[1]]

            # create segment object
            seg = Segment(next_segment_location, next_symbol, Segment.id_counter)

            # add segment to 'body'
            self.segments.append(seg)

            # check if were done
            if next_symbol.isdigit():
                additional_segments = False
                seg.set_tail()

        # set other parameters for later use
        self.length = len(self.segments)
        self.wriggler_id = self.segments[-1].get_symbol()

    def connect_segments(self):
        """ A function to set neighbors as an internal state for each segment. """

        for i in range(self.get_len()):
            if i == self.get_len() - 1:
                self.segments[i].set_anterior_segment(self.segments[i - 1].get_location())
            elif i == 0:
                self.segments[i].set_posterior_segment(self.segments[i + 1].get_location())
            else:
                self.segments[i].set_anterior_segment(self.segments[i - 1].get_location())
                self.segments[i].set_posterior_segment(self.segments[i + 1].get_location())

    def print_wriggler(self):
        for i in range(len(self.segments)):
            print(self.segments[i].get_symbol(), end='')
        print()

    def move(self, new_location, board):
        """A function to move a Wriggler to a new location on the board. """

        # find if the new_location is next to the head or tail
        wriggler_body = self.get_segments()
        head_position = self.get_head_location()
        tail_position = self.get_tail_location()

        # determine which end of Wriggler is going to move
        move_head, move_tail = False, False
        if is_adjacent(head_position, new_location):
            if board.is_symbol(new_location, 'e'):
                move_head = True
        elif is_adjacent(tail_position, new_location):
            if board.is_symbol(new_location, 'e'):
                move_tail = True
        else:
            print('Error: invalid move', new_location)
            exit(1)

        # do move and associated resets
        old_location = None
        if move_head:
            for i in range(len(wriggler_body)):
                old_location = wriggler_body[i].get_location()
                wriggler_body[i].set_location(new_location)
                board.board[new_location[0]][new_location[1]] = board.board[old_location[0]][old_location[1]]
                new_location = old_location
            board.board[old_location[0]][old_location[1]] = 'e'

        elif move_tail:
            for i in range(len(wriggler_body)-1, -1, -1):
                old_location = wriggler_body[i].get_location()
                wriggler_body[i].set_location(new_location)
                board.board[new_location[0]][new_location[1]] = board.board[old_location[0]][old_location[1]]
                new_location = old_location
            board.board[old_location[0]][old_location[1]] = 'e'

        # format Wriggler segments correctly
        fix_directions(self.get_segments(), board)


