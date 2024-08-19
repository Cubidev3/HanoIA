from agents import Agent
from hanoi_game import HanoiProblem, default, HanoiMove, HanoiAgentProgram, HanoiEnvironment
from search import breadth_first_tree_search, Node, depth_limited_search

def print_node(node):
    if node in (None, 'cutoff', 'failure'):
        return

    print_node(node.parent)
    print(node.state)

environment = HanoiEnvironment(default())

program = HanoiAgentProgram()
agent = Agent(program)

environment.add_thing(agent)

for i in range(20):
    print('\n')
    print("Desempenho: {}".format(agent.performance))
    print(f"hanoi:  {environment.hanoi}")

    environment.step()