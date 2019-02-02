"""
Author: Bryan A. Asher
Date: 01/27/2019
"""

import time


class Logger:
    """ A class used for logging information. """

    def __init__(self, solution_file):
        """ A function to initialize a logger object. """

        self.write_file = solution_file

    def check_goal(self, goal_found, current_node, visited, start_time):
        """ A function to manage flow in a solution state. """
        if goal_found:
            self.solution(current_node, visited, start_time)
            exit(0)

    def solution(self, current_node, visited, start_time):
        """ A function to gather appropriate solution info and write it to the solution file. """

        moves = [current_node.parent_move]
        parent_id = current_node.parent_id

        while parent_id is not None:
            parent_node = visited[parent_id]
            move = parent_node.parent_move
            if move is not None:
                moves.append(move)
            parent_id = parent_node.parent_id

        with open(self.write_file, 'a+') as write_file:
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
            elapsed_time = end_time - start_time

            final_time = '{0} \n'.format(elapsed_time)
            write_file.write(final_time)

            number_moves = '{0} \n'.format(len(moves))
            write_file.write(number_moves)

    def fail(self):
        """ A function to log a failure to solve game. """

        print("Fail: No solution found")
        with open(self.write_file, 'a+') as write_file:
            write_file.write('FAIL\n')
