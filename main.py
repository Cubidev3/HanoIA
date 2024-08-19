from agents import Agent, Environment
from hanoi_game import HanoiProblem, default, HanoiMove, HanoiAgentDepthLimitedProgram, HanoiEnvironment, \
    HanoiAgentAstarProgram, HanoiGame

# Victor Neony da Silva - 202200014570

def run_environment(environment: Environment, agent: Agent):
    for i in range(50):
        print('\n')
        print("Desempenho: {}".format(agent.performance))
        print(f"hanoi:  {environment.hanoi}")

        environment.step()

def agent_uninformed():
    game = HanoiGame([[3, 2, 1], [], []])
    environment = HanoiEnvironment(game)

    program = HanoiAgentDepthLimitedProgram()
    agent = Agent(program)

    environment.add_thing(agent)
    run_environment(environment, agent)


def agent_informed():
    game = default() # [[5, 4, 3, 2, 1], [], []]
    environment = HanoiEnvironment(game)

    program = HanoiAgentAstarProgram()
    agent = Agent(program)

    environment.add_thing(agent)
    run_environment(environment, agent)


print("Uninformed Agent Test:")
agent_uninformed()

print("\n")
print("Informed Agent Test:")
agent_informed()