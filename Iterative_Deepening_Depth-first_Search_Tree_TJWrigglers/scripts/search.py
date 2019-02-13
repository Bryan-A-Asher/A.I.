"""
Author: Bryan A. Asher
Date: 02/08/2019
"""

from collections import deque
import utility


def breadth_first_tree_search(root):
    # initialize the frontier using the initial state of problem
    frontier = deque()
    frontier.append(root)

    while True:

        # if the frontier is empty then return failure
        if not frontier:
            utility.failure()

        # choose a leaf node and remove it from the frontier
        current_node = frontier.popleft()

        # if the node contains a goal state then return the corresponding solution
        if current_node.is_goal():
            current_node.solution()

        else:
            # expand the chosen node, adding the resulting nodes to the frontier
            children = current_node.children()

            for child in children:
                child.parent_move = child.parent_move + current_node.parent_move
                frontier.append(child)


def depth_limiting_tree_search(root, limit):

    cutoff = False
    current_node = root
    current_node.depth = 0

    # if the node contains a goal state then return the corresponding solution
    if current_node.is_goal():
        current_node.solution()

    else:
        # expand the chosen node, adding the resulting nodes to the frontier
        children = current_node.children()

        if limit == 0:
            cutoff = True

        if not cutoff:
            for child in children:
                child.parent_move = child.parent_move + current_node.parent_move
                depth_limiting_tree_search(child, limit-1)


def iterative_deepening_depth_first_tree_search(root):
    depth = 0
    max_depth = float('inf')

    while depth <= max_depth:
        depth_limiting_tree_search(root, depth)
        depth += 1
        print('Current search depth:{0}'.format(depth), end='\r')
    print('Fail: No solution within a search depth of {0}'.format(depth))

