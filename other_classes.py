from scipy.constants import Planck
from math import e


class Demand:
    def __init__(self):
        self.id = 0
        self.paths = []
        self.start_node_id = 0
        self.end_node_id = 0
        self.value = 0

    # def __repr__(self):
    #     return "\nDemandid:"+str(self.id)+"\npaths:"+str(self.paths)+"\nstart_node:"+str(self.start_node_id)+"\nend node id:"+str(self.end_node_id)+"\nvalue:"+str(self.value)
    #
    # def __str__(self):
    #     return "\nDemandid:"+str(self.id)+"\npaths:"+str(self.paths)+"\nstart_node:"+str(self.start_node_id)+"\nend node id:"+str(self.end_node_id)+"\nvalue:"+str(self.value)


class Path:
    def __init__(self):
        self.id = 0
        self.edges = []

    # def __repr__(self):
    #     return "\nPathid:"+str(self.id)+"\nedges:"+str(self.edges)+"\ntransponder_id:"+str(self.transponder_id)
    #
    # def __str__(self):
    #     return "\nPathid:"+str(self.id)+"\nedges:"+str(self.edges)+"\ntransponder_id:"+str(self.transponder_id)


class Tranponder:
    def __init__(self):
        self.id = 0
        self.bitrate = 0
        self.costs = {}
        self.osnr = 0
        self.band = 0
        self.slice_width = 0
        self.slices = []

    # def __repr__(self):
    #     return "\nTransponderid:"+str(self.id)+"\nbitrate:"+str(self.bitrate)+"\ncosts"+str(self.costs)+"\nosnr:"+str(self.osnr)+"\nband"+str(self.band)+"\nslice width:"+str(self.slice_width)+"\nslices:"+str(self.slices)
    #
    # def __str__(self):
    #     return "\nTransponderid:"+str(self.id)+"\nbitrate:"+str(self.bitrate)+"\ncosts"+str(self.costs)+"\nosnr:"+str(self.osnr)+"\nband"+str(self.band)+"\nslice width:"+str(self.slice_width)+"\nslices:"+str(self.slices)


class Environment:
    def __init__(self, network, N):
        self.network = network
        self.solutions = []  # list of network solutions
        # def setup_solution_network_list(self, N):
        for i in range(N):
            self.solutions.append(SolutionNetwork(self.network))

    def setup_demands(self):
        for i in range(len(self.network.demands)):
            for j in range(len(self.solutions)):
                self.solutions[j].demands[i].unused_resources = -1 * self.network.demands[i].value

    def update_cost(self):
        for solution in self.solutions:
            solution.update_cost()

    def update_unused_resources(self):
        for solution in self.solutions:
            solution.update_unused_resources()

    def find_solution(self, solution):  # check first constraint
        for sol in self.solutions[solution]:
            sol.start_solution()

    def check_first_constraint(self):
        for i in range(len(self.solutions)):
            if not self.solutions[i].update_constraint_1():
                print("First constraint not meet for " + str(i) + " solution")

    def check_second_constraint(self):
        for i in range(len(self.solutions)):
            if not self.solutions[i].update_constraint_2():
                print("First constraint not meet for " + str(i) + " solution")


class SolutionNetwork:
    def __init__(self, network):
        self.demands = []
        self.network = network
        for j in range(len(network.demands)):
            self.demands.append(SolutionDemand(j))
        self.cost = 0  # ile kosztuje to rozwiązanie
        self.unused_resources = 0  # ile GB ponad jest niewykorzystywanych
        self.demand_nr = len(network.demands)
        self.band_slices = [[False] * 384] * len(
            network.edges_ids)  # lista o długości liczby krawędzi, dla każdej liczba sliców z wartością 1/0
        self.constraint_1_not_met = []
        self.constraint_2_not_met = []

    def update_cost(self):
        # cost = 0
        # for i in range(self.demand_nr):
        #     cost += self.demands[i].cost
        # self.cost = cost
        # return self.cost
        f_cost_ = 0
        for band in self.network.band_cost:
            sum_ybE = 0
            if band == 1:
                for edge in self.band_slices:
                    if True in edge[:int(len(self.network.slices_bands) / 2) + 1]:
                        sum_ybE += 1
            else:
                for edge in self.band_slices:
                    if True in edge[int(len(self.network.slices_bands) / 2) + 1:]:
                        sum_ybE += 1
            sum_eTb = 0
            for demand in self.demands:
                for path in demand.transponders:
                    for trans in path:
                        sum_eTb += trans.type.costs[band]
            f_cost_ += band * sum_ybE + sum_eTb
        self.cost = f_cost_
        return f_cost_


    def update_unused_resources(self):
        self.unused_resources = 0
        for i in range(self.demand_nr):
            self.unused_resources += self.demands[i].unused_resources
        return self.unused_resources

    def update_constraint_1(self):
        self.constraint_1_not_met = []
        for i in range(self.demand_nr):
            if self.demands[i].unused_resources < 0:
                self.constraint_1_not_met.append(i)
        return self.constraint_1_not_met

    def update_constraint_2(self):
        self.constraint_2_not_met = []
        for i in range(self.demand_nr):
            for j in range(self.network.maxPaths):
                transp = self.demands[i].transponders[j]
                if transp is None or len(transp) is 0:
                    continue
                else:
                    for trans in transp:
                        if not self.check_2_constraint(i, j, trans):
                            self.constraint_2_not_met.append(i)
        return self.constraint_2_not_met

    # zwraca czy 2 ograniczone jest spełnione dla danego zapotrzebowania odpowiedniej ścieżki i danego transpondera
    def check_2_constraint(self, demand, path, transponder):
        L1 = Planck * self.network.bands_fr.get(transponder.band) * transponder.type.osnr * transponder.type.band
        L2 = 0
        for edge in self.network.demands[demand].paths[path].edges:
            f_e = self.network.ilas[edge]
            lambda_s = self.network.slices_losses[transponder.start_slice]
            len_e = self.network.edges_lengths[edge]
            V = self.network.ila_loss
            W = self.network.nloss
            L2 += f_e * (e ** ((lambda_s * len_e) / (1 + f_e)) + V - 2) + (
                    e ** ((lambda_s * len_e) / (1 + f_e)) + W - 2)
        if L1 * L2 > self.network.p0:
            return False
        else:
            return True

    def start_solution(self):
        for demand in self.demands:
            #TODO
            return

class SolutionDemand:
    def __init__(self, demand_id=-1):
        if demand_id <= -1:
            self.demand_id = -1
        else:
            self.demand_id = demand_id  # id zapotrzebowania w liście zapotrzebowań w sieci
        self.unused_resources = 0  # ile GB ponad zapotrzebowanie produkuje rozwiązanie zapotrzebowania
        self.cost = 0  # koszt pokrycia zapotrzebowania
        self.transponders = [[], [], []]  # id jest numer ścieżki a wartością lista solutionTransponder

    def add_transponder(self, path, t_type, start_slice, band):
        new_t = SolutionTransponder(t_type, start_slice, path, band)
        self.transponders[path].append(new_t)
        self.cost += new_t.type.cost


class SolutionTransponder:
    def __init__(self, t_type, start_slice, path, band):
        self.type = t_type
        self.start_slice = start_slice  # starting slice on edge
        self.path = path  # which edges
        self.band = band  # 1 or 2