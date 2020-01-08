class Demand:
    def __init__(self):
        self.id = 0
        self.paths = []
        self.start_node_id = 0
        self.end_node_id = 0
        self.value = 0

    def __repr__(self):
        return "\nDemandid:"+str(self.id)+"\npaths:"+str(self.paths)+"\nstart_node:"+str(self.start_node_id)+"\nend node id:"+str(self.end_node_id)+"\nvalue:"+str(self.value)

    def __str__(self):
        return "\nDemandid:"+str(self.id)+"\npaths:"+str(self.paths)+"\nstart_node:"+str(self.start_node_id)+"\nend node id:"+str(self.end_node_id)+"\nvalue:"+str(self.value)
