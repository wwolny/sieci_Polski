from ABC.bee_colony import Colony
from network.network import Network
from environment import *

if __name__ == "__main__":
    network = Network(100)
    network.set_up_network_data("res.dat")
    env = Environment(network, 10)
    env.setup_demands()
    # env.update()
    print("Minimal cost if all transponders would be on 1st band taking first path is: {0}".format(env.get_minimal_cost()))
    # env.check_first_constraint()
    # env.check_second_constraint()

    print("Network setup. Searching for basic solution started")
    env.find_solution()
    env.check_first_constraint()
    env.update()
    # env.check_second_constraint()
    print(env.solutions[0].cost)
        # print(solution.get_current_cheapest_transponder_set())

    # env.print_used_transponders()
    # env.print_cheapest_tranponders()
    # env.reset_solutions()
    # env.print_cheapest_tranponders()

    bee_colony = Colony(3, 5, 2, env) # workers_count; onlookers_count; scouts_count

    for _ in range(5):
        bee_colony.search_for_best_solution(1)

    print("Cheapest solution found:", bee_colony.best_solution_network.cost)
    print("END")





