from scipy.constants import Planck, e
import random
from solution.solution_demand import SolutionDemand


class SolutionNetwork:
    def __init__(self, network):
        self.network = network
        self.demands = []
        for j in range(len(network.demands)):
            self.demands.append(SolutionDemand(self.network, j))
        self.cost = 0  # ile kosztuje to rozwiązanie
        self.unused_resources = 0  # ile GB ponad jest niewykorzystywanych
        self.demand_nr = len(network.demands)
        self.band_slices = [[False] * 384 for i in range(
            len(network.edges_ids))]  # lista o długości liczby krawędzi, dla każdej liczba sliców z wartością 1/0
        self.constraint_1_not_met = []
        self.constraint_2_not_met = []
        self.transponders_2_band = []  # demands in which here are transponders in second band
        self.setup_demands()

    def update_cost(self):
        f_cost_ = 0
        for band in self.network.band_cost:
            sum_ybE = 0
            if band == 1:
                for edge in self.band_slices:
                    if True in edge[:int(len(self.network.slices_bands) / 2) + 1]:
                        sum_ybE += 1
            if band == 2:
                for edge in self.band_slices:
                    if True in edge[int(len(self.network.slices_bands) / 2) + 1:]:
                        sum_ybE += 1

            # Obliczamy sumę kosztów transponderów
            sum_eTb = 0
            for demand in self.demands:
                for path in demand.transponders:
                    for trans in path:
                        if trans.band == band:
                            sum_eTb += trans.type.costs.get(band)
            f_cost_ += band * sum_ybE + sum_eTb
        self.cost = f_cost_
        return f_cost_

    def min_cost(self):
        f_cost_ = 0
        for demand in self.demands:
            trans = demand.current_cheapest_transponder_set()
            for t in trans:
                f_cost_ += self.network.transponders[t].costs.get(1)
        f_cost_ += len(self.network.edges_ids)
        return f_cost_

    def update_unused_resources(self):
        self.unused_resources = 0
        self.transponders_2_band = []
        for i in range(self.demand_nr):
            self.unused_resources += self.demands[i].unused_resources
            if len(self.demands[i].transponders_in_2_band) > 0:
                self.transponders_2_band.append(i)
        return self.unused_resources

    def update_constraint_1(self):
        self.constraint_1_not_met = []

        for i, demand in enumerate(self.demands):
            if len(demand.current_cheapest_transponder_set()) > 0:
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

    def are_constraints_met(self):
        if len(self.update_constraint_1()) == 0 and len(self.update_constraint_2()) == 0:
            return True
        else:
            return False

    def update(self):
        self.update_unused_resources()
        self.update_cost()
        self.get_current_cheapest_transponder_set()

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
            while len(demand.current_cheapest_transponder_set()) > 0:
                transponder_type = 0
                transponder_path_id = 0

                # choose cheapest transponder for given demand.
                # If biggest transponder still does not satisfy demand than choose it and continue with function
                while True:
                    if self.network.transponders[transponder_type].bitrate > -1*demand.unused_resources:
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
                    #  path taken

                #   set all slices to USED for all edges in path
                for edge in self.network.demands[demand.demand_id].paths[transponder_path_id].edges:
                    for slice_number in range(transponder.slice_width):
                        self.band_slices[edge - 1][first_slice_used + slice_number] = True
                #   USED flag set
                if first_slice_used is not -1:
                    band = self.network.slices_bands.get(first_slice_used + 1)
                    demand.add_transponder(transponder_path_id, transponder, first_slice_used, band)
                else:
                    print("Couldn't meet demand for {0}".format(demand.demand_id))
                    break
            # update costs and resources before next iteration
            self.update()

    # Nie sprawdza, czy można postawić
    # ustawia True na danych krawędziach na odpowienidnich slicach
    def add_trans_on_slice(self, slice, width, edges, start_edge):
        if start_edge != 0 and start_edge != 1:
            return -1
        for edge in edges:
            for i in range(width):
                self.band_slices[edge-start_edge][slice+i] = True
        return 1

    def free_trans_on_slice(self, slice, width, edges, start_edge=0):
        if start_edge != 0 and start_edge != 1:
            return -1
        for edge in edges:
            for i in range(width):
                self.band_slices[edge-start_edge][slice+i] = False
        return 1

    # if you cna fit transponder on slice
    # return True
    # else return False
    def check_trans_on_slice(self, slice, width, edges, start_edge=0):
        if start_edge != 0 and start_edge != 1:
            return -1
        possible = True
        for edge in edges:
            for i in range(width):
                if self.band_slices[edge - start_edge][slice + i] == True:
                    possible = False
                    break
            if not possible:
                break
        return possible

    def reset_solution(self):
        for demand in self.demands:
            demand.reset()

        #  set all slices for all edges to NOT USED (False)
        self.band_slices = [[False] * 384 for i in range(len(self.network.edges_ids))]

        self.setup_demands()
        self.update()
        self.update_constraint_1()
        self.update_constraint_2()

    def setup_demands(self):
        for i in range(len(self.network.demands)):
            self.demands[i].unused_resources = -1 * self.network.demands[i].value
            self.demands[i].demand_val = -1 * self.network.demands[i].value

    def print_current_cheapest_transponder_set(self):
        for demand in self.demands:
            print("Demand: {0}: list of cheapest needed transponders: {1}".format(demand.demand_id, demand.current_cheapest_transponder_set()))

    # return dictionary key demand id, value list of transponders type
    def get_current_cheapest_transponder_set(self):
        cheapest = {}
        for demand in self.demands:
            demand.current_cheapest_transponder_set()
            if len(demand.cheapest_transponder_set) > 0:
                cheapest[demand.demand_id] = demand.current_cheapest_transponder_set()
        return cheapest

    def print_transponders(self):
        for demand in self.demands:
            transponders = [[],[],[]]
            for i, path in enumerate(demand.transponders):
                for transponder in path:
                    transponders[i].append(transponder.type.id-1)
            print("Demand: {0}: list of transponders: {1}".format(demand.demand_id, transponders))

    # input dict of key: demand id and value: number of transponders needed
    # return set of demands paths where should be put the most powerful transponders to cover
    # whole 3 slices in whole network on the same start slice
    def make_set_for_three(self, list_of_demands_ids):
        # return dict of path that should be used to fully cover slice
        # key is path id and value is list of demand id and which element in demand path takes
        chosen_paths = {}
        available_paths = {}
        available_edges = list(range(1, len(self.network.edges_ids)+1))
        for id in list(list_of_demands_ids.keys()):
            for i, path in enumerate(self.network.demands[id].paths):
                available_paths[path.id] = [id, i]
        while 0 < len(available_paths) and len(available_edges) != 0:
            path = random.choice(list(available_paths.keys()))
            dem_id = available_paths.get(path)[0]
            nr_path = available_paths.get(path)[1]
            if list_of_demands_ids.get(dem_id) <= 0:
                available_paths.pop(path)
                continue
            to_remove = []
            for edge in self.network.demands[dem_id].paths[nr_path].edges:
                to_remove.append(edge)
            if len(list(set(available_edges).intersection(to_remove))) != len(to_remove):
                available_paths.pop(path)
                continue
            available_edges = [x for x in available_edges if x not in to_remove]
            chosen_paths[path] = [dem_id, nr_path]
            available_paths.pop(path)
            list_of_demands_ids[dem_id] -= 1
        return chosen_paths

