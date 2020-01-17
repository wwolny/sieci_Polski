class Onlooker:
    def __init__(self, start_solution, network):
        self.current_solution = start_solution
        self.network = network
        self.DEL_LEVEL = 150

    def search_for_new_solution(self):
        self.del_all_trans_over()
        self.current_solution.get_current_cheapest_transponder_set()
        for demand in self.current_solution.demands:
            while len(demand.cheapest_transponder_set) > 0:
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
                                if self.current_solution.band_slices[edge - 1][start_slice - 1 + slice_number] is True:
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
                        self.current_solution.band_slices[edge - 1][first_slice_used + slice_number] = True
                #   USED flag set
                if first_slice_used is not -1:
                    band = self.network.slices_bands.get(first_slice_used + 1)
                    demand.add_transponder(transponder_path_id, transponder, first_slice_used, band)
                else:
                    print("Couldn't meet demand for {0}".format(demand.demand_id))
                    break
        # update costs and resources before next iteration
        self.current_solution.update()

    def del_all_trans_over(self):
        # delete transponders and free slice bands
        for d_id, demand in enumerate(self.current_solution.demands):
            for p_id, path in enumerate(demand.transponders):
                for id, transponder in enumerate(path):
                    if transponder.start_slice >= self.DEL_LEVEL:
                        self.current_solution.demands[d_id].transponders[p_id].pop(id)
                        self.current_solution.free_trans_on_slice(transponder.start_slice, transponder.type.slice_width, self.network.demands[d_id].paths[p_id].edges, 1)
                        if transponder.start_slice >= self.network.sec_band_start:
                            self.current_solution.demands[d_id].del_from_2_band(transponder.start_slice, transponder.path)


