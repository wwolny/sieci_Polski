# implementation of Artificial Bee Colony Algorithm
import copy

from ABC.onlooker import Onlooker
from ABC.scout import Scout
from ABC.worker import Worker


class Colony:
    def __init__(self, workers_count, onlookers_count, scouts_count, environment):

        check_if_bee_count_correct(workers_count, onlookers_count, scouts_count, environment.solutions)

        self.environment = environment
        self.workers = []
        self.onlookers = []
        self.scouts = []

        set_networks_for_bees(self, workers_count, onlookers_count, scouts_count, environment.solutions, environment.network)

        self.best_solution_network = environment.solutions[0]

    def search_for_best_solution(self, iteration_number):
        current_iteration = 1

        while current_iteration <= iteration_number:
            for worker in self.workers:
                worker.search_for_new_solution()

                if worker.current_solution_network.cost < self.best_solution_network.cost:
                    self.best_solution_network = copy.copy(worker.current_solution_network)

            for onlooker in self.onlookers:
                onlooker.search_for_new_solution()

                if onlooker.current_solution_network.cost < self.best_solution_network.cost:
                    self.best_solution_network = copy.copy(onlooker.current_solution_network)

            for scout in self.scouts:
                scout.search_for_new_solution()

                if scout.current_solution_network.cost < self.best_solution_network.cost:
                    self.best_solution_network = copy.copy(scout.current_solution_network)

            current_iteration += 1

        self.environment.check_first_constraint()
        self.environment.check_second_constraint()


def check_if_bee_count_correct(workers_count, onlookers_count, scouts_count, initial_solution_networks):
    if workers_count + onlookers_count + scouts_count > len(initial_solution_networks):
        print("Total count of bees must be equal to number of initial solution networks")
        exit(1)


def set_networks_for_bees(self, workers_count, onlookers_count, scouts_count, solution_networks, network):
    current_network_number = 0

    for _ in range(workers_count):
        self.workers.append(Worker(solution_networks[current_network_number], network))
        current_network_number += 1

    for _ in range(onlookers_count):
        self.onlookers.append(Onlooker(solution_networks[current_network_number], network))
        current_network_number += 1

    for _ in range(scouts_count):
        self.scouts.append(Scout(solution_networks[current_network_number], network))
        current_network_number += 1
