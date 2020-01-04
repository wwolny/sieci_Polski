class Network:
    def __init__(self):
        self.demands = []
        self.paths = []
        self.transponders = []
        self.demands_dict = {}
        self.band_cost = {}
        self.slices_bands = {}
        self.ilas = {}
        self.slices_losses = {}
        self.slices = []
        self.edges_lengths = {}
        self.edges_ids = []
        self.edges_paths = {}
        self.bands_fr = {}

        self.MaxFreqSlices = 0
        self.ila_loss = 0
        self.nloss = 0
        self.maxPaths = 0
        self.p0 = 0.0

    from network_setup_methods import set_up_network_data
    from network_setup_methods import set_up_demands
    from network_setup_methods import set_up_paths_in_demands
    from network_setup_methods import set_up_transponders
    from network_setup_methods import setup_band_cost
    from network_setup_methods import setup_slices_bands
    from network_setup_methods import setup_ilas
    from network_setup_methods import set_up_slices_losses
    from network_setup_methods import set_up_edges
    from network_setup_methods import set_up_other_parameters
    from network_setup_methods import set_up_bands_fr

    def print(self):
        print(self.demands)
        print(self.paths)
        print(self.transponders)
        print(self.demands_dict)
        print(self.band_cost)
        print(self.slices_bands)
        print(self.ilas)
        print(self.slices_losses)
        print(self.slices)
        print(self.edges_lengths)
        print(self.edges_ids)
        print(self.edges_paths)
        print(self.bands_fr)
        print(self.MaxFreqSlices)
        print(self.ila_loss)
        print(self.nloss)
        print(self.maxPaths)
        print(self.p0)
