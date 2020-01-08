from solution.solution_network import SolutionNetwork


class Environment:
    def __init__(self, network, N):
        self.network = network
        self.solutions = []  # list of network solutions
        for i in range(N):
            self.solutions.append(SolutionNetwork(self.network))

    def setup_demands(self):
        for i in range(len(self.network.demands)):
            for j in range(len(self.solutions)):  # MOVE THESE 2 LINES TO SOLUTION NETWORK
                self.solutions[j].demands[i].unused_resources = -1 * self.network.demands[i].value

    def update_cost(self):
        for solution in self.solutions:
            solution.update_cost()

    def update_unused_resources(self):
        for solution in self.solutions:
            solution.update_unused_resources()

    def find_solution(self):  # check first constraint
        for sol in self.solutions:
            sol.start_solution()

    def check_first_constraint(self):
        for i in range(len(self.solutions)):
            if len(self.solutions[i].update_constraint_1()) != 0:
                print("First constraint not meet for solution: " + str(i))

    def check_second_constraint(self):
        for i in range(len(self.solutions)):
            if len(self.solutions[i].update_constraint_2()) != 0:
                print("Second constraint not meet for solution: " + str(i))
