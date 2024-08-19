from copy import deepcopy

from agents import Environment
from search import Problem, SimpleProblemSolvingAgentProgram, depth_limited_search, astar_search, Node

# Victor Neony da Silva - 202200014570

class HanoiMove:
    def __init__(self, from_tower, to_tower):
        self.from_tower = from_tower
        self.to_tower = to_tower

    def __str__(self):
        return "{} -> {}".format(self.from_tower, self.to_tower)


def default():
    return HanoiGame([[5, 4, 3, 2, 1], [], []])

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

    def get_tower_cost(self, index):
        return (len(self.towers) - index - 1) * 2

    def get_disk_count(self):
        highest = 0
        for tower in self.towers:
            for disk in tower:
                highest = disk if disk > highest else highest

        return highest

    def get_disks(self):
        disks = []
        for tower in self.towers:
            for disk in tower:
                disks.append(disk)

        disks.sort(reverse=True)
        return disks

    def finished(self):
        towers = [[]] * (len(self.towers) - 1)
        towers.append(self.get_disks())
        return towers

    def get_cost(self):
        cost = 0
        for i in range(len(self.towers)):
            tower = self.get_tower(i)
            if len(tower) != 0:
                cost += (i+1) * self.get_tower_cost(i)

        return cost

    def is_complete(self):
        empty_towers = 0
        for tower in self.towers:
            if len(tower) == 0:
                empty_towers = empty_towers + 1
                continue

            break

        return len(self.towers) - empty_towers <= 1

    def as_tuple(self):
        disks = [0] * self.get_disk_count()
        for tower_index in range(len(self.towers)):
            tower = self.get_tower(tower_index)

            for disk in tower:
                disks[disk - 1] = tower_index

        return tuple(disks)


    def __str__(self):
        return "{}".format(self.towers)

    def __lt__(self, other):
        return self.get_cost() < other.get_cost()

    def __eq__(self, other):
        if not isinstance(other, HanoiGame):
            return False

        result = self.as_tuple() == other.as_tuple()
        return result

    def __hash__(self):
        return hash(self.as_tuple())


class HanoiProblem(Problem):
    def actions(self, state):
        return state.get_possible_moves()

    def result(self, state, action):
        copy = deepcopy(state)
        copy.apply_move(action)
        return copy

    def goal_test(self, state):
        return state.is_complete()


class HanoiAgentDepthLimitedProgram(SimpleProblemSolvingAgentProgram):
    def update_state(self, state, percept):
        return percept

    def formulate_goal(self, state):
        return state.finished()

    def formulate_problem(self, state, goal):
        return HanoiProblem(state, goal)

    def search(self, problem):
        node = depth_limited_search(problem, 15)
        if node in ("failure", "cutoff", None):
            return None

        return node.solution()


class HanoiAgentAstarProgram(SimpleProblemSolvingAgentProgram):
    def update_state(self, state, percept):
        return percept

    def formulate_goal(self, state):
        return state.finished()

    def formulate_problem(self, state, goal):
        return HanoiProblem(state, goal)

    def search(self, problem):
        node = astar_search(problem, astar_node_heuristic)
        if node in ("failure", "cutoff", None):
            return None

        return node.solution()


def astar_node_heuristic(node: Node):
    if node in ("failure", "cutoff", None):
        return 0

    return node.state.get_cost()


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