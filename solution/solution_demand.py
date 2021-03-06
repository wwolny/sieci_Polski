import copy

from solution.solution_transponder import SolutionTransponder


class SolutionDemand:
    def __init__(self, network, demand_id=-1):
        if demand_id <= -1:
            self.demand_id = -1
        else:
            self.demand_id = demand_id  # id zapotrzebowania w liście zapotrzebowań w sieci
        self.unused_resources = 0  # ile GB ponad zapotrzebowanie produkuje rozwiązanie zapotrzebowania
        self.cost = 0  # koszt pokrycia zapotrzebowania
        self.transponders = [[], [], []]  # id jest numer ścieżki a wartością lista solutionTransponder
        self.cheapest_transponder_set = []
        self.network = network
        self.demand_val = 0
        self.transponders_in_2_band = []

    def copy(self):
        new_solution_demand = SolutionDemand(self.network, self.demand_id)
        new_solution_demand.unused_resources = self.unused_resources
        new_solution_demand.cost = self.cost
        new_solution_demand.transponders = copy.deepcopy(self.transponders)
        new_solution_demand.cheapest_transponder_set = copy.deepcopy(self.cheapest_transponder_set)
        new_solution_demand.demand_val = self.demand_val
        new_solution_demand.transponders_in_2_band = copy.deepcopy(self.transponders_in_2_band)

        return new_solution_demand

    def add_transponder(self, path, transponder_type, start_slice, band):
        new_transponder = SolutionTransponder(transponder_type, start_slice, path, band)
        self.transponders[path].append(new_transponder)
        self.cost += transponder_type.costs.get(band)
        self.unused_resources += transponder_type.bitrate
        if band == 2:
            self.transponders_in_2_band.append(new_transponder)

    def reset(self):
        self.unused_resources = self.demand_val  # przywracamy stan pierwotny
        self.cost = 0
        self.transponders = [[], [], []]
        self.transponders_in_2_band = []

    def current_cheapest_transponder_set(self):
        resources = self.unused_resources
        self.cheapest_transponder_set = []

        while resources < 0:
            transponder_type = 0
            while True:
                if self.network.transponders[transponder_type].bitrate > -1*resources:
                    break
                if transponder_type + 1 == len(self.network.transponders):
                    break
                transponder_type += 1
            resources += self.network.transponders[transponder_type].bitrate
            self.cheapest_transponder_set.append(transponder_type)

        return self.cheapest_transponder_set

    def del_from_2_band(self, start_slice, path):
        for id, trans in enumerate(self.transponders_in_2_band):
            if trans.start_slice == start_slice and trans.path == path:
                self.transponders_in_2_band.pop(id)
                return 1
        return 0

    def del_transponder(self, path, id):
        transponder = self.transponders[path][id]
        self.cost -= transponder.type.costs.get(transponder.band)
        self.unused_resources -= transponder.type.bitrate
        if transponder.band == 2:
            self.del_from_2_band(transponder.start_slice, transponder.path)
        self.transponders[path].pop(id)