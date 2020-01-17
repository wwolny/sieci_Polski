import random


class Scout:
    def __init__(self, start_solution_network, network):
        self.current_solution_network = start_solution_network
        self.network = network

    def search_for_new_solution(self):
        self.current_solution_network.reset_solution()

        random.shuffle(self.current_solution_network.demands)

        for demand in self.current_solution_network.demands:
            while demand.unused_resources < 0:
                transponder_type = 0
                transponder_path_id = 0

                # choose cheapest transponder for given demand.
                # If biggest transponder still does not satisfy demand than choose it and continue with function
                while True:
                    if transponder_type + 1 == len(self.network.transponders):
                        break
                    # # 40 % to choose smaller transponder than potentially needed
                    if random.randrange(10) < 5:
                        break
                    if self.network.transponders[transponder_type].bitrate > self.network.demands[demand.demand_id].value:
                        break
                    # transponder_type += 1
                    transponder_type += 1

                transponder = self.network.transponders[transponder_type]
                # transponder type chosen

                can_continue = True
                first_slice_used = -1

                while True:
                    # randomly choose index of Path that we will use
                    path_id = random.choice(range(len(self.network.demands[demand.demand_id].paths)))
                    path = self.network.demands[demand.demand_id].paths[path_id]

                    for start_slice in transponder.slices:

                        # check if given start slice is not taken for all edges in path
                        for edge in path.edges:
                            for slice_number in range(transponder.slice_width):
                                if self.current_solution_network.band_slices[edge - 1][start_slice - 1 + slice_number] is True:
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
                        self.current_solution_network.band_slices[edge - 1][first_slice_used + slice_number] = True
                #   USED flag set

                band = self.network.slices_bands.get(first_slice_used + 1)
                demand.add_transponder(transponder_path_id, transponder, first_slice_used, band)

        # update costs and resources before next iteration
        self.current_solution_network.update()

        print("Scout found new solution with cost:", self.current_solution_network.cost)
