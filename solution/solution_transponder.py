class SolutionTransponder:
    def __init__(self, t_type, start_slice, path, band=0):
        self.type = t_type  # object of transponder in use
        self.start_slice = start_slice  # starting slice on edge counting from 0
        self.path = path  # which edges
        self.band = band  # 1 or 2
