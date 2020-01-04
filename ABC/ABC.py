# implementation of Artificial Bee Colony Algorithm
class Colony:
    def __init__(self, N):
        self.workers = []
        self.onlookers = []
        self.scouts = []
        self.colony_size = N
