from solution.solution_transponder import SolutionTransponder


class SolutionDemand:
    def __init__(self, demand_id=-1):
        if demand_id <= -1:
            self.demand_id = -1
        else:
            self.demand_id = demand_id  # id zapotrzebowania w liście zapotrzebowań w sieci
        self.unused_resources = 0  # ile GB ponad zapotrzebowanie produkuje rozwiązanie zapotrzebowania
        self.cost = 0  # koszt pokrycia zapotrzebowania
        self.transponders = [[], [], []]  # id jest numer ścieżki a wartością lista solutionTransponder

    def add_transponder(self, path, transponder_type, start_slice, band):
        new_transponder = SolutionTransponder(transponder_type, start_slice, path, band)
        self.transponders[path].append(new_transponder)
        self.cost += transponder_type.costs.get(band)
        self.unused_resources += transponder_type.bitrate

    def reset(self):
        self.unused_resources = 0  # przywracamy stan pierwotny
        self.cost = 0
        self.transponders = [[], [], []]
