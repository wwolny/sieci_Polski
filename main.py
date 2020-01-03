from network import Network
from other_classes import *

if __name__ == "__main__":
    network = Network()
    network.set_up_network_data("res2.dat")
    # network.print()
    env = Environment(network, 10)
    env.setup_demands()
    env.update_cost()
    env.update_unused_resources()
    env.check_first_constraint()
    env.check_second_constraint()

    # cost function
    f_cost_ = 0
    # for band in network.band_cost:
    #     sum_ybE = 0
    #     for slice in network.slices_bands:
    #         if network.slices_bands.get(slice) == band:
    #             sum_ybE += 1
    #     print(sum_ybE)
    #     sum_xtnnps = 0
    #     eTb = 0
    #     for trans in network.transponders:
    #         eTb = trans.costs[band]
    #         xtnnps = 0
    #         for edge in network.edges_paths:
    #             for path in network.edges_paths.get(edge):
    #                 xtnnps+=1
    #         sum_xtnnps = eTb*xtnnps
    #     f_cost_ += band*sum_ybE+sum_xtnnps
    #     print(sum_xtnnps)
    # print(f_cost_)





