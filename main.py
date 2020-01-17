from ABC.bee_colony import Colony
from network.network import Network
from environment import *

if __name__ == "__main__":
    network = Network()
    network.set_up_network_data("res2.dat")
    env = Environment(network, 1)
    env.setup_demands()
    env.update_cost()
    env.update_unused_resources()
    env.check_first_constraint()
    env.check_second_constraint()

    env.test_make_set_3()

    print("Network setup. Searching for basic solution started")
    env.find_solution()
    env.check_first_constraint()
    env.check_second_constraint()
    # for solution in env.solutions:
    #     print(solution.cost)

    # env.print_used_transponders()
    # env.print_cheapest_tranponders()
    # env.reset_solutions()
    # env.print_cheapest_tranponders()

    bee_colony = Colony(2, 3, 5, env)

    # bee_colony.search_for_best_solution(10)

    print("Cheapest solution found:", bee_colony.best_solution_network.cost)
    print("END")





