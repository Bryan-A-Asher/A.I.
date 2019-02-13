"""
Author: Bryan A. Asher
Date: 01/27/2019
"""
# todo deal with anterior and posterior updates

from Segment import Segment


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


def find_wrigglers(board):
    """ A function for locating initial head locations of all Wrigglers. """

    head_locations = []

    for i in range(board.height):
        for j in range(board.width):
            symbol = board.board[i][j]
            if symbol in ['U', 'D', 'L', 'R']:
                head_locations.append([i, j, symbol])

    return head_locations


def find_appropriate_wriggler(wrigglers, wriggler_id):
    """ A function that returns the index of a Wriggler in an list given it's id"""

    for i in range(len(wrigglers)):
        if wrigglers[i].get_id() == wriggler_id:
            return i


def fix_directions(segment_list, board):
    """ A function to realign the direction characters to reference the appropriate segment in the Wriggler. """

    direction = None
    for i in range(len(segment_list)):

        first_seg = segment_list[i].location
        if i != len(segment_list) - 1:
            second_seg = segment_list[i+1].location
        else:
            break

        if first_seg[0] > second_seg[0]:
            if segment_list[i].head:
                direction = 'U'
            else:
                direction = '^'
        elif first_seg[0] < second_seg[0]:
            if segment_list[i].head:
                direction = 'D'
            else:
                direction = 'v'
        elif first_seg[1] > second_seg[1]:
            if segment_list[i].head:
                direction = 'L'
            else:
                direction = '<'
        elif first_seg[1] < second_seg[1]:
            if segment_list[i].head:
                direction = 'R'
            else:
                direction = '>'

        board.board[first_seg[0]][first_seg[1]] = direction


def get_wriggler_ids(board):
    wriggler_ids = []
    for i in range(board.height):
        for j in range(board.width):
            symbol = board.board[i][j]
            if symbol.isdigit():
                wriggler_ids.append(symbol)
    return wriggler_ids


class Wrigglers:
    """ A class to model the Wrigglers from the TJ Wrigglers game. """

    # A class variable for differentiating Wrigglers
    id_counter = 1

    def __init__(self):
        self.wriggler_id = None
        self.segments = []

    def get_head_location(self):
        """ A function for locating the head a specific Wriggler. """

        body = self.segments
        head_location = None
        for i in range(len(body)):
            if body[i].head:
                head_location = body[i].location

        return head_location

    def get_tail_location(self):
        """ A function for locating the tail a specific Wriggler. """

        body = self.segments
        tail_location = None
        for i in range(len(body)):
            if body[i].tail:
                tail_location = body[i].location

        return tail_location

    def get_id(self):
        """ A function for locating the id a specific Wriggler. """

        body = self.segments
        wriggler_id = None
        for i in range(len(body)):
            if body[i].tail:
                wriggler_id = body[i].symbol

        return wriggler_id

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
                seg.tail = True

        # set id
        self.wriggler_id = self.segments[-1].symbol

    def print_wriggler(self):
        for i in range(len(self.segments)):
            print(self.segments[i].symbol, end='')
        print()
        for i in range(len(self.segments)):
            print(self.segments[i].location, end='')
        print()

    def move(self, action_info, board):
        """A function to move a Wriggler to a new location on the board. """

        new_location = action_info[-1]

        # find if the new_location is next to the head or tail
        wriggler_body = self.segments
        head_position = self.get_head_location()
        tail_position = self.get_tail_location()

        # validate which end of Wriggler is going to move
        move_head, move_tail = False, False

        if action_info[1] == 0:  # 0 indicates action came from a head reading
            if is_adjacent(head_position, new_location) and board.is_symbol(new_location, 'e'):
                move_head = True
        elif action_info[1] == 1:  # 1 indicates action came from a tail reading
            if is_adjacent(tail_position, new_location) and board.is_symbol(new_location, 'e'):
                move_tail = True
        else:
            print('Error: invalid move', new_location)
            exit(1)

        # do move and associated resets
        old_location = None
        if move_head:
            for i in range(len(wriggler_body)):
                old_location = wriggler_body[i].location
                wriggler_body[i].location = new_location
                board.board[new_location[0]][new_location[1]] = board.board[old_location[0]][old_location[1]]
                new_location = old_location
            board.board[old_location[0]][old_location[1]] = 'e'

        elif move_tail:
            for i in range(len(wriggler_body)-1, -1, -1):
                old_location = wriggler_body[i].location
                wriggler_body[i].location = new_location
                board.board[new_location[0]][new_location[1]] = board.board[old_location[0]][old_location[1]]
                new_location = old_location
            board.board[old_location[0]][old_location[1]] = 'e'

        # format Wriggler segments correctly
        fix_directions(self.segments, board)


