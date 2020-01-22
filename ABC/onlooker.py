import random


class Onlooker:
    def __init__(self, start_solution, network):
        self.current_solution = start_solution
        self.network = network
        self.DEL_LEVEL = 150
        self.MAX_ITERATION = 10

    def search_for_new_solution(self):
        if len(self.current_solution.constraint_1_not_met) == 0:
            self.del_all_trans_over()

        self.current_solution.update()
        self.current_solution.update_constraint_1()
        self.current_solution.get_current_cheapest_transponder_set()

        for path_id in range(self.network.maxPaths):
            if len(self.current_solution.constraint_1_not_met) == 0:
                break
            rand_demand = random.sample(range(len(self.current_solution.demands)), len(self.current_solution.demands))

            while len(rand_demand) > 0:
                demand = random.choice(rand_demand)
                rand_demand.remove(demand)
                iteration = 0

                while len(self.current_solution.demands[demand].current_cheapest_transponder_set()) > 0 and iteration < self.MAX_ITERATION:
                    transponder_type = self.current_solution.demands[demand].cheapest_transponder_set[0]
                    transponder = self.network.transponders[transponder_type]

                    can_continue = True
                    first_slice_used = -1
                    path = self.network.demands[demand].paths[path_id]
                    
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
                    #   USED flag set
                    if first_slice_used is not -1:
                        band = self.network.slices_bands.get(first_slice_used + 1)
                        self.current_solution.demands[demand].add_transponder(path_id, transponder, first_slice_used, band)
                        self.current_solution.add_trans_on_slice(first_slice_used, transponder.slice_width, self.network.demands[demand].paths[path_id].edges, 1)
                    else:
                        print("Couldn't meet demand for {0}".format(demand))
                        break
                    iteration += 1
                # update costs and resources before next iteration
                self.current_solution.update()
                self.current_solution.update_constraint_1()
        print("Onlooker found new solution with cost:", self.current_solution.cost)
        # print("First constraint not meet for:{0}".format(self.current_solution.constraint_1_not_met))

    def del_all_trans_over(self):
        # delete transponders and free slice bands
        for d_id, demand in enumerate(self.current_solution.demands):
            for p_id, path in enumerate(demand.transponders):
                del_trans = []
                for id, transponder in enumerate(path):
                    if transponder.start_slice >= self.DEL_LEVEL:
                        del_trans.append([id,transponder])
                for element in reversed(del_trans):
                    self.current_solution.demands[d_id].del_transponder(p_id, element[0])
                    self.current_solution.free_trans_on_slice(element[1].start_slice, element[1].type.slice_width, self.network.demands[d_id].paths[p_id].edges, 1)

