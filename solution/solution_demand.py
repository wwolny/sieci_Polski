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

    def add_transponder(self, path, transponder_type, start_slice, band):
        new_transponder = SolutionTransponder(transponder_type, start_slice, path, band)
        self.transponders[path].append(new_transponder)
        self.cost += transponder_type.costs.get(band)
        self.unused_resources += transponder_type.bitrate

    def reset(self):
        self.unused_resources = 0  # przywracamy stan pierwotny
        self.cost = 0
        self.transponders = [[], [], []]

    def current_cheapest_transponder_set(self):
        resources = self.unused_resources
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
