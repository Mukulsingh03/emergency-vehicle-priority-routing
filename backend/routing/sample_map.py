from routing.graph import Graph

NODE_COORDS = {
    "A": (28.6139, 77.2090),
    "B": (28.6200, 77.2100),
    "C": (28.6300, 77.2150),
    "D": (28.6400, 77.2200),
    "E": (28.6500, 77.2250),
    "F": (28.6600, 77.2300),
    "G": (28.6700, 77.2350),
    "H": (28.6800, 77.2400),
}

from routing.graph import Graph

def create_sample_graph():
    g = Graph()

    edges = [

        # Route to Hospital_2 (F) → Base 20
        ("G", "E", 10),
        ("E", "F", 10),

        # Route to Hospital_1 (C) → Base 21
        ("G", "D", 11),
        ("D", "C", 10),

    ]

    for u, v, w in edges:
        g.add_edge(u, v, w)
        g.add_edge(v, u, w)

    return g
