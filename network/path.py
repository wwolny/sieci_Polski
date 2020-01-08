class Path:
    def __init__(self):
        self.id = 0
        self.edges = []

    def __repr__(self):
        return "\nPathid:"+str(self.id)+"\nedges:"+str(self.edges)+"\ntransponder_id:"

    def __str__(self):
        return "\nPathid:"+str(self.id)+"\nedges:"+str(self.edges)+"\ntransponder_id:"
