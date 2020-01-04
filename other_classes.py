from scipy.constants import Planck
from math import e


class Demand:
    def __init__(self):
        self.id = 0
        self.paths = []
        self.start_node_id = 0
        self.end_node_id = 0
        self.value = 0

    def __repr__(self):
        return "\nDemandid:"+str(self.id)+"\npaths:"+str(self.paths)+"\nstart_node:"+str(self.start_node_id)+"\nend node id:"+str(self.end_node_id)+"\nvalue:"+str(self.value)

    def __str__(self):
        return "\nDemandid:"+str(self.id)+"\npaths:"+str(self.paths)+"\nstart_node:"+str(self.start_node_id)+"\nend node id:"+str(self.end_node_id)+"\nvalue:"+str(self.value)


class Path:
    def __init__(self):
        self.id = 0
        self.edges = []

    def __repr__(self):
        return "\nPathid:"+str(self.id)+"\nedges:"+str(self.edges)+"\ntransponder_id:"

    def __str__(self):
        return "\nPathid:"+str(self.id)+"\nedges:"+str(self.edges)+"\ntransponder_id:"


class Tranponder:
    def __init__(self):
        self.id = 0
        self.bitrate = 0
        self.costs = {}
        self.osnr = 0
        self.band = 0
        self.slice_width = 0
        self.slices = []

    def __repr__(self):
        return "\nTransponderid:"+str(self.id)+"\nbitrate:"+str(self.bitrate)+"\ncosts"+str(self.costs)+"\nosnr:"+str(self.osnr)+"\nband"+str(self.band)+"\nslice width:"+str(self.slice_width)+"\nslices:"+str(self.slices)

    def __str__(self):
        return "\nTransponderid:"+str(self.id)+"\nbitrate:"+str(self.bitrate)+"\ncosts"+str(self.costs)+"\nosnr:"+str(self.osnr)+"\nband"+str(self.band)+"\nslice width:"+str(self.slice_width)+"\nslices:"+str(self.slices)


class Environment:
    def __init__(self, network, N):
        self.network = network
        self.solutions = []  # list of network solutions
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


class SolutionNetwork:
    def __init__(self, network):
        self.demands = []
        self.network = network
        for j in range(len(network.demands)):
            self.demands.append(SolutionDemand(j))
        self.cost = 0  # ile kosztuje to rozwiązanie
        self.unused_resources = 0  # ile GB ponad jest niewykorzystywanych
        self.demand_nr = len(network.demands)
        self.band_slices = [[False] * 384 for i in range(
            len(network.edges_ids))]  # lista o długości liczby krawędzi, dla każdej liczba sliców z wartością 1/0
        self.constraint_1_not_met = []
        self.constraint_2_not_met = []

    def update_cost(self):
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
        for i, demand in enumerate(self.demands):
            if demand.unused_resources < 0:
                self.constraint_1_not_met.append(i)
        return self.constraint_1_not_met

    def update_constraint_2(self):
        self.constraint_2_not_met = []
        for i, demand in enumerate(self.demands):
            for j in range(self.network.maxPaths):
                transp = demand.transponders[j]
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
            f_e = self.network.ilas.get(edge)
            lambda_s = self.network.slices_losses.get(transponder.start_slice + 1)
            len_e = self.network.edges_lengths.get(edge)
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
            while demand.unused_resources < 0:
                transponder_type = 0
                transponder_path_id = 0

                # choose cheapest transponder for given demand.
                # If biggest transponder still does not satisfy demand than choose it and continue with function
                while True:
                    if self.network.transponders[transponder_type].bitrate > self.network.demands[demand.demand_id].value:
                        break
                    if transponder_type + 1 == len(self.network.transponders):
                        break
                    transponder_type += 1
                transponder = self.network.transponders[transponder_type]
                # transponder type chosen

                can_continue = True
                first_slice_used = -1
                for path_id, path in enumerate(self.network.demands[demand.demand_id].paths):
                    for start_slice in transponder.slices:

                        # check if given start slice is not taken for all edges in path
                        for edge in path.edges:
                            for slice_number in range(transponder.slice_width):
                                if self.band_slices[edge - 1][start_slice - 1 + slice_number] is True:
                                    can_continue = False
                                    break
                            if can_continue is False:
                                break
                        # check ended

                        if can_continue is True:
                            first_slice_used = start_slice - 1
                            break
                        else:
                            can_continue = True

                    #  if we managed to choose any slice for given path then choose this path
                    if first_slice_used is not -1:
                        transponder_path_id = path_id
                        break
                    #  path choosed

                #   set all slices to USED for all edges in path
                for edge in self.network.demands[demand.demand_id].paths[transponder_path_id].edges:
                    for slice_number in range(transponder.slice_width):
                        self.band_slices[edge - 1][first_slice_used + slice_number] = True
                #   USED flag set

                band = self.network.slices_bands.get(first_slice_used + 1)
                demand.add_transponder(transponder_path_id, transponder, first_slice_used, band)
        # update costs and resources before next iteration
        self.update_unused_resources()
        self.update_cost()


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
        self.cost += t_type.costs.get(band)
        self.unused_resources += t_type.bitrate


class SolutionTransponder:
    def __init__(self, t_type, start_slice, path, band):
        self.type = t_type
        self.start_slice = start_slice  # starting slice on edge
        self.path = path  # which edges
        self.band = band  # 1 or 2
