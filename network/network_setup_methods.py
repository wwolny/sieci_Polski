from re import findall

from network.demand import Demand
from network.path import Path
from network.transponder import Tranponder


def set_up_network_data(self, data_file_path):
    with open(data_file_path) as file:
        text = file.read()
        self.set_up_other_parameters([text])
        self.set_up_edges([text])
        self.set_up_demands([text])
        self.set_up_paths_in_demands([text])
        self.set_up_transponders([text])
        self.setup_band_cost([text])
        self.setup_slices_bands([text])
        self.setup_ilas([text])
        self.set_up_slices_losses([text])
        self.set_up_bands_fr([text])


def set_up_demands(self, text):
    rows = findall('param demand := .*:=\n([\s\S]*?)\n;', text[0])[0].replace("\t", " ").split("\n")
    demands_id_counter = 0
    for row_iter, row in enumerate(rows):
        values = row.split(" ")

        while '' in values:
            values.remove('')

        for col_iter, value in enumerate(values[1:]):
            if not value == ".":
                demand = Demand()
                demand.paths = [Path() for _ in range(self.maxPaths)]
                demand.id = demands_id_counter
                demands_id_counter += 1
                demand.start_node_id = row_iter + 1
                demand.end_node_id = col_iter + 1
                self.demands.append(demand)
                self.demands_dict[(demand.start_node_id, demand.end_node_id)] = len(self.demands) - 1
                demand.value = float(value)


def set_up_paths_in_demands(self, text):
    blocks = findall('param epaths [\s\S]*?\n;', text[0])[0].replace("\t", " ").split("\n\n")
    blocks = blocks[:-1]
    blocks[0] = blocks[0][blocks[0].find("\n") + 1:]

    paths_id_counter = 0
    for block in blocks:
        rows = block.split("\n")
        if [] in rows:
            rows.remove([])

        for row_count, row in enumerate(rows):
            if row == "":
                continue
            values = row.split(" ")
            while '' in values:
                values.remove('')

            edge_id = int(values[2])
            path_id = int(values[1])
            for col_count, value in enumerate(values[3:]):
                if value == '1':
                    node_1_id = row_count + 1
                    node_2_id = col_count + 1
                    if (node_1_id, node_2_id) in self.demands_dict:
                        pos = self.demands_dict[(node_1_id, node_2_id)]

                        path = self.demands[pos].paths[path_id - 1]
                        path.edges.append(edge_id)
                        path.id = paths_id_counter
                        paths_id_counter += 1
                        self.paths.append(path)

                        self.edges_paths[edge_id].append(path)


def set_up_transponders(self, text):
    transponders = findall("set TRAN := (.*);", text[0])[0].split(" ")
    for transponder_id in transponders:
        transponder = Tranponder()
        transponder.id = int(transponder_id)
        self.transponders.append(transponder)

    transponder_costs = findall('param trcost [\s\S]*?\n;', text[0])[0].replace("\t", " ").split("\n")
    transponder_costs = transponder_costs[1:]
    transponder_costs = transponder_costs[:-1]
    for row in transponder_costs:
        band_id = int(row.split(" ")[2])
        costs = row.split(" ")[3:]
        for t_iter, cost in enumerate(costs):
            self.transponders[t_iter].costs[band_id] = float(cost)

    rows = findall('param bitrate:=\n([\s\S]*?)\n;', text[0])[0].replace("\t", " ").split("\n")
    for row_iter, row in enumerate(rows):
        values = row.split(" ")
        while '' in values:
            values.remove('')
        self.transponders[row_iter].bitrate = float(values[-1])

    rows = findall('param osnr:=\n([\s\S]*?)\n;', text[0])[0].replace("\t", " ").split("\n")
    for row_iter, row in enumerate(rows):
        values = row.split(" ")
        while '' in values:
            values.remove('')
        self.transponders[row_iter].osnr = float(values[1])

    rows = findall('param trcenter := .*\n([\s\S]*?)\n;', text[0])[0].replace("\t", " ").split("\n")
    for row in rows:
        values = row.split(" ")
        while '' in values:
            values.remove('')
        values = values[2:]

        if '1' not in values:
            break

        for col_iter, value in enumerate(values):
            if value == '1':
                self.transponders[col_iter].slice_width += 1

        self.transponders[row_iter].band = float(values[1])

    lists = findall('set FREQT.*:= ([\s\S]*?);', text[0])
    for iter, list in enumerate(lists):
        slices = list.split(" ")
        for slice in slices:
            self.transponders[iter].slices.append(int(slice))

    rows = findall('param trband:=\n([\s\S]*?)\n;', text[0])[0].replace("\t", " ").split("\n")
    for row_iter, row in enumerate(rows):
        values = row.split(" ")
        while '' in values:
            values.remove('')
        self.transponders[row_iter].band = float(values[1])


def set_up_other_parameters(self, text):
    self.MaxFreqSlices = int(findall('param MaxFreqSlices:= (.*);', text[0])[0])
    self.ila_loss = float(findall('param ilaloss:= (.*);', text[0])[0])
    self.nloss = float(findall('param nloss:= (.*);', text[0])[0])
    self.maxPaths = int(findall('param MaxPaths:= (.*);', text[0])[0])
    self.p0 = float(findall('param P0:= (.*);', text[0])[0])


def setup_band_cost(self, text):
    band_costs = findall('param bcost:=\n([\s\S]*?)\n;', text[0])[0].replace("\t", " ").split("\n")
    for band_cost in band_costs:
        self.band_cost[int(band_cost.split(" ")[1])] = int(band_cost.split(" ")[2])


def setup_slices_bands(self, text):
    lists = findall('set FREQB.*:= ([\s\S]*?);', text[0])
    for iter, list in enumerate(lists):
        slices = list.split(" ")
        for slice in slices:
            self.slices_bands[int(slice)] = iter + 1


def setup_ilas(self, text):
    rows = findall('param ila:=\n([\s\S]*?)\n;', text[0])[0].replace("\t", " ").split("\n")
    for row_iter, row in enumerate(rows):
        values = row.split(" ")
        while '' in values:
            values.remove('')
        self.ilas[int(values[0])] = int(values[1])


def set_up_slices_losses(self, text):
    rows = findall('param loss:=\n([\s\S]*?)\n;', text[0])[0].replace("\t", " ").split("\n")
    for row_iter, row in enumerate(rows):
        values = row.split(" ")
        while '' in values:
            values.remove('')
        self.slices_losses[int(values[0])] = float(values[1])

    self.slices = self.slices_losses.keys()


def set_up_edges(self, text):
    rows = findall('param length:=\n([\s\S]*?)\n;', text[0])[0].replace("\t", " ").split("\n")
    for row_iter, row in enumerate(rows):
        values = row.split(" ")
        while '' in values:
            values.remove('')
        self.edges_lengths[int(values[0])] = int(values[1])

    self.edges_ids = self.edges_lengths.keys()
    for edge_id in self.edges_ids:
        self.edges_paths[edge_id] = []


def set_up_bands_fr(self, text):
    rows = findall('param fr:=\n([\s\S]*?)\n;', text[0])[0].replace("\t", " ").split("\n")
    for row_iter, row in enumerate(rows):
        values = row.split(" ")
        while '' in values:
            values.remove('')
        self.bands_fr[int(values[0])] = float(values[1])
