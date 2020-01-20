import random


# TODO: change some transponders from 3rd/2nd path to 1st (shortest)
class Worker:
    def __init__(self, start_solution, network):
        self.current_solution = start_solution
        self.network = network
        self.MAX_ITERATION = 50

    def search_for_new_solution(self):
        for _ in range(self.MAX_ITERATION):
            cheapest_trans_dict = self.current_solution.get_current_cheapest_transponder_set()
            if len(cheapest_trans_dict) == 0:
                self._set_lower()
            else:
                self._add_new_trans(cheapest_trans_dict)
            self.current_solution.update_constraint_1()
            self.current_solution.update()
        print("Worker found new solution with cost:", self.current_solution.cost)
        # print("First constraint not meet for:{0}".format(self.current_solution.constraint_1_not_met))

    def _set_lower(self):
        demands_lst = self.current_solution.transponders_2_band
        if len(demands_lst) == 0:
            return 0
        dem_id = random.choice(demands_lst)
        transponder = None
        for path in range(3):
            for tran in self.current_solution.demands[dem_id].transponders[path]:
                if tran.band == 2:
                    if tran.type.id != 4:
                        transponder = tran
                        trans_path = path
                        break
            if transponder:
                break
        if not transponder:
            return -1
        trans_t = transponder.type.id -1
        chosen_path = -1
        chosen_slice = -1
        slice = self.network.sec_band_start - max(1, trans_t) +1
        while slice > max(1, trans_t):
            for path_id, path in enumerate(self.network.demands[dem_id].paths):
                for edge in path.edges:
                    nxt_path = False
                    if not self.current_solution.band_slices[edge-1][slice]:
                        for width in range(0, max(trans_t, 1) - 1):
                            if self.current_solution.band_slices[edge-1][slice - width]:
                                nxt_path = True
                                break
                        chosen_path = path_id
                        chosen_slice = slice
                    if nxt_path or chosen_slice != -1:
                        break
                if chosen_slice != -1:
                    break
            if chosen_slice != -1:
                break
            slice -= 1
        if chosen_slice != -1:
            self.current_solution.add_trans_on_slice(slice, max(1, trans_t),
                                                     self.network.demands[dem_id].paths[chosen_path].edges, 1)
            self.current_solution.free_trans_on_slice(transponder.start_slice, max(1, trans_t),
                                                     self.network.demands[dem_id].paths[transponder.path].edges, 1)
            # print("Worker set lower transponder on slice:{0}, type:{1}".format(chosen_slice, trans_t))
            if trans_path != chosen_path:
                for i in range(len(self.current_solution.demands[dem_id].transponders[trans_path])):
                    if self.current_solution.demands[dem_id].transponders[trans_path][i].start_slice == transponder.start_slice:
                        self.current_solution.demands[dem_id].transponders[trans_path].pop(i)
                        self.current_solution.demands[dem_id].transponders[chosen_path].append(transponder)
                        break
            self.current_solution.demands[dem_id].del_from_2_band(transponder.start_slice, transponder.path)
            # print("Worker set lower transponder on slice:{0}, type:{1}".format(chosen_slice, trans_t))
            transponder.start_slice = chosen_slice
            transponder.path = self.network.demands[dem_id].paths[chosen_path]
            transponder.band = 1
            return 1


    def _add_new_trans(self, dict_cheapest):
        if len(dict_cheapest) == 0:
            return 0
        chosen_dem_id = random.choice(list(dict_cheapest.keys()))
        trans_t = random.choice(dict_cheapest.get(chosen_dem_id))
        chosen_path = -1
        chosen_slice = -1
        slice = self.network.sec_band_start
        while slice > max(1, trans_t):
            for path_id, path in enumerate(self.network.demands[chosen_dem_id].paths):
                for edge in path.edges:
                    nxt_path = False
                    if not self.current_solution.band_slices[edge-1][slice]:
                        for width in range(0, max(trans_t, 1)-1):
                            if self.current_solution.band_slices[edge-1][slice-width]:
                                nxt_path = True
                                break
                        chosen_path = path_id
                        chosen_slice = slice
                    if nxt_path or chosen_slice != -1:
                        break
                if chosen_slice != -1:
                    break
            if chosen_slice != -1:
                break
            slice -= 1
        if chosen_slice != -1:
            self.current_solution.demands[chosen_dem_id].add_transponder(chosen_path, self.network.transponders[trans_t], chosen_slice-max(trans_t, 1)+1, 1)
            self.current_solution.add_trans_on_slice(slice, max(1, trans_t),
                                                     self.network.demands[chosen_dem_id].paths[chosen_path].edges, 1)
            # print("Worker added transponder on slice:{0}, type:{1}".format(chosen_slice, trans_t))
            return 1
        slice = self.network.MaxFreqSlices
        while slice > self.network.sec_band_start + max(1, trans_t):
            for path_id, path in enumerate(self.network.demands[chosen_dem_id].paths):
                for edge in path.edges:
                    nxt_path = False
                    if not self.current_solution.band_slices[edge-1][slice]:
                        for width in range(0, max(trans_t, 1) - 1):
                            if self.current_solution.band_slices[edge-1][slice - width]:
                                nxt_path = True
                                break
                        chosen_path = path_id
                        chosen_slice = slice
                    if nxt_path or chosen_slice != -1:
                        break
                if chosen_slice != -1:
                    break
            if chosen_slice != -1:
                break
            slice -= 1
        if chosen_slice != -1:
            self.current_solution.demand[chosen_dem_id].add_transponder(chosen_path, self.network.transponders[trans_t], chosen_slice-max(trans_t, 1)+1, 2)
            self.current_solution.add_trans_on_slice(slice, max(1, trans_t),
                                                     self.network.demands[chosen_dem_id].paths[chosen_path].edges, 1)
            # print("Worker added transponder on slice:{0}, type:{1}".format(chosen_slice, trans_t))
            return 1