class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, from_node, to_node, travel_time):
        if from_node not in self.adj:
            self.adj[from_node] = []

        self.adj[from_node].append((to_node, travel_time))    