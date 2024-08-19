from hanoi_game import HanoiProblem, default, HanoiMove
from search import breadth_first_tree_search, Node, depth_limited_search

def print_node(node):
    if node in (None, 'cutoff', 'failure'):
        return

    print_node(node.parent)
    print(node.state)

problem = HanoiProblem()
node = depth_limited_search(problem, 50)
print_node(node)