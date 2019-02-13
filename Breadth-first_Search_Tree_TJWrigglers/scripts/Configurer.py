"""
Author: Bryan A. Asher
Date: 01/27/2019
"""


class Configurer:
    """ A class for reading input files and configuring
        the appropriate objects accordingly. """

    def __init__(self):
        self.width = None
        self.height = None
        self.number_wrigglers = None
        self.board_data = []

    def read_file(self, file):
        """ A function for reading configuration files. """

        file = './puzzles/' + file

        with open(file, 'r') as in_file:
            self.width, self.height, self.number_wrigglers = in_file.readline().split()
            for line in in_file:
                self.board_data.append(line.split())

    def setup(self, board):
        """ A function for configuring board and wriggler objects. """

        board.set_board(self.board_data)

    def get_num_wrigglers(self):
        return self.number_wrigglers

    def print_configs(self):
        """ A function for printing configurable data. """

        print('Width: ', self.width)
        print('Height:', self.height)
        print('#Wrigglers:', self.number_wrigglers)

        for i in range(int(self.height)):
            print(self.board_data[i])
