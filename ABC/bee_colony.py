# implementation of Artificial Bee Colony Algorithm
import copy

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

        self.set_networks_for_bees(workers_count, onlookers_count, scouts_count)

        self.best_solution_network = environment.solutions[0]

    def search_for_best_solution(self, iteration_number):
        current_iteration = 1

        while current_iteration <= iteration_number:
            for worker in self.workers:
                worker.search_for_new_solution()

                if worker.current_solution.cost < self.best_solution_network.cost:
                    self.best_solution_network = copy.copy(worker.current_solution)

            for onlooker in self.onlookers:
                onlooker.search_for_new_solution()

                if onlooker.current_solution.cost < self.best_solution_network.cost:
                    self.best_solution_network = copy.copy(onlooker.current_solution)

            for scout in self.scouts:
                scout.search_for_new_solution()

                if scout.current_solution.cost < self.best_solution_network.cost:
                    self.best_solution_network = copy.copy(scout.current_solution)


            current_iteration += 1

        self.environment.check_first_constraint()
        self.environment.check_second_constraint()

    def check_if_bee_count_correct(self, workers_count, onlookers_count, scouts_count):
        if workers_count + onlookers_count + scouts_count > len(self.environment.solutions):
            print("Total count of bees must be equal to number of initial solution networks")
            exit(1)

    def set_networks_for_bees(self, workers_count, onlookers_count, scouts_count):
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
            self.onlookers.append(Onlooker(self.environment.solutions[current_network_number], self.environment.network))
            current_network_number += 1

        for _ in range(scouts_count):
            self.scouts.append(Scout(self.environment.solutions[current_network_number], self.environment.network))
            current_network_number += 1
