from copy import deepcopy

from agents import Environment
from search import Problem, SimpleProblemSolvingAgentProgram, depth_limited_search


class HanoiMove:
    def __init__(self, from_tower, to_tower):
        self.from_tower = from_tower
        self.to_tower = to_tower

    def __str__(self):
        return "{} -> {}".format(self.from_tower, self.to_tower)


def default():
    return HanoiGame([[3, 2, 1], [], []])

def finished():
    return HanoiGame([[], [], [3, 2, 1]])

class HanoiGame:
    def __init__(self, towers):
        self.towers = towers

    def push_disk(self, tower_index, disk):
        tower = self.get_tower(tower_index)
        if len(tower) == 0 or tower[-1] > disk:
            tower.append(disk)

    def pop_disk(self, tower_index):
        tower = self.get_tower(tower_index)
        if len(tower) > 0:
            return tower.pop()
        return None

    def apply_move(self, move):
        disk = self.pop_disk(move.from_tower)
        self.push_disk(move.to_tower, disk)

    def get_possible_moves(self):
        moves = []
        top_disks = self.get_top_disks()

        for i in range(len(top_disks)):
            for j in range(len(top_disks)):
                if top_disks[i] is not None and (top_disks[j] is None or top_disks[i] < top_disks[j]):
                    moves.append(HanoiMove(i, j))

        return moves

    def get_top_disk(self, tower_index):
        tower = self.get_tower(tower_index)
        if len(tower) > 0:
            return tower[-1]
        return None

    def get_top_disks(self):
        return [self.get_top_disk(i) for i in range(len(self.towers))]

    def get_tower(self, index):
        return self.towers[index]

    def is_complete(self):
        empty_towers = 0
        for tower in self.towers:
            if len(tower) == 0:
                empty_towers = empty_towers + 1
                continue

            break

        return len(self.towers) - empty_towers <= 1


    def __str__(self):
        return "{}".format(self.towers)


class HanoiProblem(Problem):
    def actions(self, state):
        return state.get_possible_moves()

    def result(self, state, action):
        copy = deepcopy(state)
        copy.apply_move(action)
        return copy

    def goal_test(self, state):
        return state.is_complete()


class HanoiAgentProgram(SimpleProblemSolvingAgentProgram):
    def update_state(self, state, percept):
        return percept

    def formulate_goal(self, state):
        return finished()

    def formulate_problem(self, state, goal):
        return HanoiProblem(state, goal)

    def search(self, problem):
        node = depth_limited_search(problem, 15)
        if node in ("failure", "cutoff", None):
            return None

        return node.solution()


class HanoiEnvironment(Environment):
    def __init__(self, initial):
        super().__init__()
        self.hanoi: HanoiGame = initial

    def percept(self, agent):
        return self.hanoi

    def execute_action(self, agent, action):
        if action is None:
            return

        self.hanoi.apply_move(action)
        if self.hanoi.is_complete():
            agent.performance += 10
            return

        agent.performance -= 1