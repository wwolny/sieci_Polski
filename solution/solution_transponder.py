class SolutionTransponder:
    def __init__(self, t_type, start_slice, path, band):
        self.type = t_type  # object of transponder in use
        self.start_slice = start_slice  # starting slice on edge
        self.path = path  # which edges
        self.band = band  # 1 or 2
