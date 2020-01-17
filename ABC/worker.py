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
        while len(self.current_solution.constraint_1_not_met) > 0 and iteration > 0 and current_slice < self.network.MaxFreqSlices:
            cheapest_trans_dict = self.current_solution.get_current_cheapest_transponder_set()

            iteration += 1
            self.current_solution.update_constraint_1()
