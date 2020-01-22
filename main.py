import math

from ABC.bee_colony import Colony
from network.network import Network
from environment import *

if __name__ == "__main__":
    network = Network(100 )
    network.set_up_network_data("res.dat")
    env = Environment(network, 10)
    env.setup_demands()
    print("Minimal cost if all transponders would be on 1st band taking first path is: {0}".format(env.get_minimal_cost()))

    print("Network setup. Searching for basic solution started")
    env.find_solution()
    env.check_first_constraint()
    env.update()

    print(env.solutions[0].cost)

    bee_colony = Colony(3, 5, 2, env)  # workers_count; onlookers_count; scouts_count

    bee_colony.search_for_best_solution(100)

    if bee_colony.best_solution_network.cost != math.inf:
        print("Cheapest solution found:", bee_colony.best_solution_network.cost)
    else:
        print("No possible solution found:")

    print("END")





