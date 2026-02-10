from routing.graph import Graph

NODE_COORDS = {
    "A": (28.6139, 77.2090),
    "B": (28.6200, 77.2100),
    "C": (28.6300, 77.2150),
}

def create_sample_graph():
    g = Graph()

    g.add_edge("A", "B", 10)
    g.add_edge("B", "C", 15)
    g.add_edge("A", "C", 30)

    return g