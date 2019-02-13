"""
Author: Bryan A. Asher
Date: 02/08/2019
"""


def failure():
    print('Fail: No solution found!')
    exit(0)


def cutoff_termination(limit):
    print('Cutoff: no solution within current depth of {0}.'.format(limit))


def run_indicator(counter):

    if counter % 4 == 0:
        print('|', end='\r')
    elif counter % 4 == 1:
        print('/', end='\r')
    elif counter % 4 == 2:
        print('-', end='\r')
    elif counter % 4 == 3:
        print("\\", end='\r')
