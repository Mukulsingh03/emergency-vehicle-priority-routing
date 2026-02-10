from routing.graph import Graph

def create_sample_graph():
    g = Graph()

    g.add_edge("A", "B", 10)
    g.add_edge("B", "C", 15)
    g.add_edge("A", "C", 30)

    return g