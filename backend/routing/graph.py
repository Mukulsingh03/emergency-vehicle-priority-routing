class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, from_node, to_node, travel_time):
        if from_node not in self.adj:
            self.adj[from_node] = []
        if to_node not in self.adj:
            self.adj[to_node] = []

        self.adj[from_node].append({
            "to": to_node,
            "base_time": travel_time
        })

    # Add reverse edge
        self.adj[to_node].append({
            "to": from_node,
            "base_time": travel_time
        })

