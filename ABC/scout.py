import random


class Scout:
    def __init__(self, start_solution, network):
        self.current_solution = start_solution
        self.network = network
        self.MAX_ITERATION = 100

    def search_for_new_solution(self):
        self.current_solution.reset_solution()
        iteration = 0
        current_slice = 0
        transponder = 3
        while len(self.current_solution.constraint_1_not_met) > 0 and iteration < self.MAX_ITERATION and current_slice < self.network.MaxFreqSlices and transponder >= 0:
            if current_slice + 1 not in self.network.transponders[transponder].slices:
                current_slice += 1
                iteration += 1
                continue
            cheapest_trans_dict = self.current_solution.get_current_cheapest_transponder_set()
            demand_ids = {}
            for demand_id in cheapest_trans_dict:
                arr = cheapest_trans_dict.get(demand_id)
                if transponder in arr:
                    demand_ids[demand_id] = arr.count(transponder)
            if len(demand_ids) == 0:
                transponder -= 1
                continue
            chosen_paths = self.current_solution.make_set_for_three(demand_ids)
            taken_edges = []
            for path in chosen_paths:
                dem_id = chosen_paths.get(path)[0]
                path_id = chosen_paths.get(path)[1]
                if len(self.network.demands[dem_id].paths[path_id].edges) == 0:
                    continue
                taken_edges.extend(self.network.demands[dem_id].paths[path_id].edges)
                self.current_solution.demands[dem_id].add_transponder(path_id, self.network.transponders[transponder],
                                                                      current_slice,
                                                                      self.network.slices_bands.get(current_slice + 1))
            self.current_solution.add_trans_on_slice(current_slice, max(1, transponder), taken_edges, 1)
            # 0 i 1 trans zajmują 1 slice, 2 trans 2 slicy, 3 trans 3 slicy
            current_slice += max(1, transponder)
            iteration += 1
            self.current_solution.update_constraint_1()
            self.current_solution.update()
        print("Scout found new solution with cost:", self.current_solution.cost)
        print("First constraint not meet for:{0}".format(self.current_solution.constraint_1_not_met))



        # self.current_solution_network.reset_solution()
        #
        # random.shuffle(self.current_solution_network.demands)
        #
        # for demand in self.current_solution_network.demands:
        #     while demand.unused_resources < 0:
        #         transponder_type = 0
        #         transponder_path_id = 0
        #
        #         # choose cheapest transponder for given demand.
        #         # If biggest transponder still does not satisfy demand than choose it and continue with function
        #         while True:
        #             if transponder_type + 1 == len(self.network.transponders):
        #                 break
        #             # # 40 % to choose smaller transponder than potentially needed
        #             if random.randrange(10) < 5:
        #                 break
        #             if self.network.transponders[transponder_type].bitrate > self.network.demands[demand.demand_id].value:
        #                 break
        #             # transponder_type += 1
        #             transponder_type += 1
        #
        #         transponder = self.network.transponders[transponder_type]
        #         # transponder type chosen
        #
        #         can_continue = True
        #         first_slice_used = -1
        #
        #         while True:
        #             # randomly choose index of Path that we will use
        #             path_id = random.choice(range(len(self.network.demands[demand.demand_id].paths)))
        #             path = self.network.demands[demand.demand_id].paths[path_id]
        #
        #             for start_slice in transponder.slices:
        #
        #                 # check if given start slice is not taken for all edges in path
        #                 for edge in path.edges:
        #                     for slice_number in range(transponder.slice_width):
        #                         if self.current_solution_network.band_slices[edge - 1][start_slice - 1 + slice_number] is True:
        #                             can_continue = False
        #                             break
        #                     if can_continue is False:
        #                         break
        #                 # check ended
        #
        #                 if can_continue is True:
        #                     first_slice_used = start_slice - 1
        #                     break
        #                 else:
        #                     can_continue = True
        #
        #             #  if we managed to choose any slice for given path then choose this path
        #             if first_slice_used is not -1:
        #                 transponder_path_id = path_id
        #                 break
        #             #  path choosed
        #
        #         #   set all slices to USED for all edges in path
        #         for edge in self.network.demands[demand.demand_id].paths[transponder_path_id].edges:
        #             for slice_number in range(transponder.slice_width):
        #                 self.current_solution_network.band_slices[edge - 1][first_slice_used + slice_number] = True
        #         #   USED flag set
        #
        #         band = self.network.slices_bands.get(first_slice_used + 1)
        #         demand.add_transponder(transponder_path_id, transponder, first_slice_used, band)
        #
        # # update costs and resources before next iteration
        # self.current_solution_network.update()
        #
        # print("Scout found new solution with cost:", self.current_solution_network.cost)
