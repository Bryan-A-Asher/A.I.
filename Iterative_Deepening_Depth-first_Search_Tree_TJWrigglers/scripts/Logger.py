"""
Author: Bryan A. Asher
Date: 01/27/2019
"""

import time
import os


class Logger:
    """ A class used for logging information. """
    start_time = None

    def __init__(self, solution_file):
        """ A function to initialize a logger object. """

        self.write_file = solution_file

    def solution(self, current_node):
        """ A function to gather appropriate solution info and write it to the solution file. """

        moves = current_node.parent_move

        if moves[-1] is None:
            del moves[-1]
            
        if not os.path.exists('./logs'):
            os.makedirs('./logs')

        new_solution_counter = 1
        while os.path.exists(self.write_file):

            if self.write_file[-5] != ')':
                self.write_file = self.write_file[:-4] + '(' + str(new_solution_counter) + ').txt'
            else:
                self.write_file = self.write_file[:-6] + str(new_solution_counter)  + ').txt'
            new_solution_counter += 1

        with open(self.write_file, 'w+') as write_file:
            for i in range(len(moves) - 1, -1, -1):
                info = '{0} {1} {2} {3} \n'.format(str(moves[i][0]), str(moves[i][1]), str(moves[i][2][1]),
                                                   str(moves[i][2][0]))
                write_file.write(info)

            board = current_node.board.board
            for j in range(len(board)):
                row = ' '.join(str(element) for element in board[j])
                row += '\n'
                write_file.write(row)

            # end program timer
            end_time = time.time()
            elapsed_time = end_time - Logger.start_time

            final_time = '{0} \n'.format(elapsed_time)
            write_file.write(final_time)

            number_moves = '{0} \n'.format(len(moves))
            write_file.write(number_moves)
            print('\n'*5)
            exit(0)
