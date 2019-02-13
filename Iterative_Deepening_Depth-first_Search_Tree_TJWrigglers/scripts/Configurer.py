"""
Author: Bryan A. Asher
Date: 01/27/2019
"""
import os

class Configurer:
    """ A class for reading input files and configuring
        the appropriate objects accordingly. """

    solution_file = None

    def __init__(self, arg_list):
        self.width = None
        self.height = None
        self.number_wrigglers = None
        self.board_data = []
        self.solution_file = None
        self.puzzle_file = None

        if len(arg_list) == 1:
            print('Error: specify puzzle file and/or solution file.')
            exit(1)
        elif len(arg_list) == 2:
            # if there is only one argument it will be assumed to be a puzzle file
            self.puzzle_file = '/home/ash/Dropbox/university/spring2019/ai/2019-sp-1a-puzzle2-baa522/puzzles/' + arg_list[1]
            self.solution_file = '/home/ash/Dropbox/university/spring2019/ai/2019-sp-1a-puzzle2-baa522/logs/solution{0}.txt'.format(arg_list[1][6])
            # self.puzzle_file = './puzzles/' + arg_list[1]
            # self.solution_file = './logs/solution{0}.txt'.format(arg_list[1][6])
        elif len(arg_list) == 3:
            self.puzzle_file = './puzzles/' + arg_list[1]
            self.solution_file = './logs/' + arg_list[2]
        else:
            print('Error: invalid command line arguments.')
            exit(1)

        Configurer.solution_file = self.solution_file

    def check_board_header(self):
        """An error checking function."""

        if int(self.height) < 1 or int(self.width) < 1 or self.height is None or self.width is None:
            print('Error: invalid board dimensions.')
            exit(1)
        if int(self.number_wrigglers) < 1 or self.number_wrigglers is None:
            print('Error: invalid Wrigglers assignment.')
            exit(1)

    def check_board_specs(self):
        """An error checking function."""

        number_rows = len(self.board_data)
        if number_rows != int(self.height):
            print('Error: inconsistent board specifications')
            exit(1)

        for i in range(number_rows):
            if len(self.board_data[i]) != int(self.width):
                print('Error: inconsistent board specifications')
                exit(1)

        wriggler_counter = 0
        for i in range(int(self.height)):
            for j in range(int(self.width)):
                if self.board_data[i][j].isdigit():
                    wriggler_counter += 1

        if wriggler_counter != int(self.number_wrigglers):
            print('Error: inconsistent Wriggler specifications')
            exit(1)

    def read_file(self):
        """ A function for reading configuration files. """

        file = self.puzzle_file

        with open(file, 'r') as in_file:
            self.width, self.height, self.number_wrigglers = in_file.readline().split()
            self.check_board_header()

            for line in in_file:
                self.board_data.append(line.split())
            self.check_board_specs()

    def setup(self, board):
        """ A function for configuring board and wriggler objects. """

        board.set_board(self.board_data, self.number_wrigglers)

    def print_configs(self):
        """ A function for printing configurable data. """

        print('Width: ', self.width)
        print('Height:', self.height)
        print('#Wrigglers:', self.number_wrigglers)

        for i in range(int(self.height)):
            print(self.board_data[i])
