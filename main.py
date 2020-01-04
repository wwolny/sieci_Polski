from network import Network
from other_classes import *

if __name__ == "__main__":
    network = Network()
    network.set_up_network_data("res2.dat")
    env = Environment(network, 10)
    env.setup_demands()
    env.update_cost()
    env.update_unused_resources()
    env.check_first_constraint()
    env.check_second_constraint()

    print("Network setup. Searching for basic solution started")
    env.find_solution()
    env.check_first_constraint()
    env.check_second_constraint()

    # network.print()
    print("END")





