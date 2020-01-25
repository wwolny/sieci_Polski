# implementation of Artificial Bee Colony Algorithm
import math
import random

from matplotlib import pylab

from ABC.onlooker import Onlooker
from ABC.scout import Scout
from ABC.worker import Worker


# TODO: change solutions for bees
class Colony:
    def __init__(self, workers_count, onlookers_count, scouts_count, environment):

        self.environment = environment

        self.check_if_bee_count_correct(workers_count, onlookers_count, scouts_count)

        self.workers = []
        self.onlookers = []
        self.scouts = []

        self.acceptable_solution_networks = []
        self.acceptable_solution_count = 0
        self.ACCEPTABLE_SOLUTION_CAP = 10

        self.promising_solution_networks = []
        self.promising_solution_count = 0
        self.PROMISING_SOLUTION_CAP = 50

        self.set_networks_for_bees(workers_count, onlookers_count, scouts_count)

        # Musimy na starcie ustawić jakieś rozwiązanie jako najlepsze
        # Jego koszt to nieskonczosc bo chcemy je zastapic dowolnym prawidlowym rozwiazaniem
        self.best_solution_network = environment.solutions[0].copy()
        self.best_solution_network.cost = math.inf

    def search_for_best_solution(self, iteration_number):
        current_iteration = 1

        while current_iteration <= iteration_number:
            print(f"\nSearch iteration: {current_iteration} started")

            for worker in self.workers:
                worker.search_for_new_solution()
                self.check_worker_attempt_cap(worker)

                self.update_acceptable_solution_networks(worker.current_solution)

                if worker.current_solution.cost < self.best_solution_network.cost:
                    if worker.current_solution.are_constraints_met():
                        self.best_solution_network = worker.current_solution.copy()

            for onlooker in self.onlookers:
                onlooker.search_for_new_solution()
                self.check_onlooker_attempt_cap(onlooker)

                self.update_acceptable_solution_networks(onlooker.current_solution)

                if onlooker.current_solution.cost < self.best_solution_network.cost:
                    if onlooker.current_solution.are_constraints_met():
                        self.best_solution_network = onlooker.current_solution.copy()

            for scout in self.scouts:
                scout.search_for_new_solution()

                self.update_promising_solution_networks(scout.current_solution)
                self.update_acceptable_solution_networks(scout.current_solution)

                if scout.current_solution.cost < self.best_solution_network.cost:
                    if scout.current_solution.are_constraints_met():
                        self.best_solution_network = scout.current_solution.copy()

            print(f"Search iteration: {current_iteration} ended \n")

            current_iteration += 1

        self.environment.check_first_constraint()
        self.environment.check_second_constraint()

    def check_if_bee_count_correct(self, workers_count, onlookers_count, scouts_count):
        if workers_count + onlookers_count + scouts_count > len(self.environment.solutions):
            print("Total count of bees must be equal to number of initial solution networks")
            exit(1)

    def set_networks_for_bees(self, workers_count, onlookers_count, scouts_count):
        # Starting solutions should all be found by scouts
        for i in range(self.environment.size):
            self.scouts.append(Scout(self.environment.solutions[i], self.environment.network))
        for scout in self.scouts:
            scout.search_for_new_solution()
        self.scouts = []

        current_network_number = 0

        for _ in range(workers_count):
            self.workers.append(Worker(self.environment.solutions[current_network_number], self.environment.network))
            current_network_number += 1

        for _ in range(onlookers_count):
            self.onlookers.append(
                Onlooker(self.environment.solutions[current_network_number], self.environment.network))
            current_network_number += 1

        for _ in range(scouts_count):
            self.scouts.append(Scout(self.environment.solutions[current_network_number], self.environment.network))
            current_network_number += 1

    def update_promising_solution_networks(self, solution_network):
        # first add any solution if pool is not filled
        if self.promising_solution_count < self.PROMISING_SOLUTION_CAP:
            self.promising_solution_networks.append(solution_network)
            self.promising_solution_count += 1

        # if pool is full then we check if new solution is better than any existing
        else:
            for i in range(self.promising_solution_count):
                if solution_network.cost < self.promising_solution_networks[i].cost:
                    self.promising_solution_networks[i] = solution_network.copy()
                    break

    def update_acceptable_solution_networks(self, solution_network):
        # first add any solution that is correct if pool is not filled
        if self.acceptable_solution_count < self.ACCEPTABLE_SOLUTION_CAP:
            if solution_network.are_constraints_met():
                self.acceptable_solution_networks.append(solution_network)
                self.acceptable_solution_count += 1

        # if pool is full then we check if new solution is better than any existing
        else:
            for i in range(self.acceptable_solution_count):
                if solution_network.cost < self.acceptable_solution_networks[i].cost:
                    if solution_network.are_constraints_met():
                        self.acceptable_solution_networks[i] = solution_network.copy()
                        break

    def check_worker_attempt_cap(self, worker):
        if worker.current_solution.cost < worker.best_solution_cost:
            worker.best_solution_cost = worker.current_solution.cost
            worker.attempt_number = 0
            return

        if worker.attempt_number >= worker.MAX_ATTEMPT_CAP:
            worker.attempt_number = 0
            worker.current_solution = random.choice(self.promising_solution_networks).copy()
            print('Worker changed network')
            print('New starting network cost', worker.current_solution.cost)

        else:
            worker.attempt_number += 1

    def check_onlooker_attempt_cap(self, onlooker):
        if onlooker.current_solution.cost < onlooker.best_solution_cost:
            onlooker.best_solution_cost = onlooker.current_solution.cost
            onlooker.attempt_number = 0
            return

        if onlooker.attempt_number >= onlooker.MAX_ATTEMPT_CAP:
            onlooker.attempt_number = 0
            onlooker.current_solution = random.choice(self.acceptable_solution_networks).copy()

            print('Onlooker changed network')
            print('New starting network cost', onlooker.current_solution.cost)

        else:
            onlooker.attempt_number += 1

    def search_for_best_solution_and_draw(self, iteration_number):
        best_solutions = []
        current_iteration = 1

        while current_iteration <= iteration_number:
            print(f"\nSearch iteration: {current_iteration} started")

            for worker in self.workers:
                worker.search_for_new_solution()
                self.check_worker_attempt_cap(worker)

                self.update_acceptable_solution_networks(worker.current_solution)

                if worker.current_solution.cost < self.best_solution_network.cost:
                    if worker.current_solution.are_constraints_met():
                        self.best_solution_network = worker.current_solution.copy()

            for onlooker in self.onlookers:
                onlooker.search_for_new_solution()
                self.check_onlooker_attempt_cap(onlooker)

                self.update_acceptable_solution_networks(onlooker.current_solution)

                if onlooker.current_solution.cost < self.best_solution_network.cost:
                    if onlooker.current_solution.are_constraints_met():
                        self.best_solution_network = onlooker.current_solution.copy()

            for scout in self.scouts:
                scout.search_for_new_solution()

                self.update_promising_solution_networks(scout.current_solution)
                self.update_acceptable_solution_networks(scout.current_solution)

                if scout.current_solution.cost < self.best_solution_network.cost:
                    if scout.current_solution.are_constraints_met():
                        self.best_solution_network = scout.current_solution.copy()

            print(f"Search iteration: {current_iteration} ended \n")

            if self.best_solution_network.cost == math.inf:
                best_solutions.append(0)
            else:
                best_solutions.append(self.best_solution_network.cost)

            current_iteration += 1

        x = range(iteration_number)

        pylab.plot(x, best_solutions)
        pylab.title("Najlepsze rozwiązanie dla danej sieci telekomunikacyjnej")
        pylab.xlabel("Numer iteracji")
        pylab.ylabel("Minimum funkcji kosztu")

        pylab.savefig('results.png')
        pylab.show()

        self.environment.check_first_constraint()
        self.environment.check_second_constraint()
