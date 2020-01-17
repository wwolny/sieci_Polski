class Worker:
    def __init__(self, start_solution_network, network):
        self.current_solution = start_solution_network
        self.network = network
        self.MAX_ITERATION = 100

    # TO BE IMPLEMENTED
    def search_for_new_solution(self):
        self.current_solution.reset_solution()
        iteration = 0
        current_slice = 0
        transponder = 3
        while len(self.current_solution.constraint_1_not_met) > 0 and iteration < self.MAX_ITERATION and current_slice < self.network.MaxFreqSlices or transponder >= 0:
            if current_slice+1 not in self.network.transponders[transponder].slices:
                current_slice += 1
                iteration +=1
                continue
            cheapest_trans_dict = self.current_solution.get_current_cheapest_transponder_set()
            demand_ids = []
            for demand_id in cheapest_trans_dict:
                arr = cheapest_trans_dict.get(demand_id)
                if transponder in arr:
                    demand_ids.append(demand_id)
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
                self.current_solution.demands[dem_id].add_transponder(path_id, self.network.transponders[transponder], current_slice, self.network.slices_bands.get(current_slice+1))
            self.current_solution.add_trans_on_slice(current_slice, max(1, transponder), taken_edges, 1)
            # 0 i 1 trans zajmują 1 slice, 2 trans 2 slicy, 3 trans 3 slicy
            current_slice += max(1, transponder)
            iteration += 1
            self.current_solution.update_constraint_1()
            self.current_solution.update()
        print("Worker found new solution with cost:", self.current_solution.cost)