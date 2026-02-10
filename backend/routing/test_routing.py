from routing.sample_map import create_sample_graph
from routing.dijkstra import dijkstra

graph = create_sample_graph()
path, time_taken = dijkstra(graph, "A", "C")

print("Path:", path)
print("Time taken:", time_taken)