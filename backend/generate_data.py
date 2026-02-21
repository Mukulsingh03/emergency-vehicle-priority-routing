from routing.sample_map import create_sample_graph
from ml.traffic_simulator import simulate_traffic
from ml.data_logger import log_data


def generate_samples(n=5000):
    graph = create_sample_graph()

    edges = []

    for from_node in graph.adj:
        for edge in graph.adj[from_node]:
            edges.append((from_node, edge["to"], edge["base_time"]))

    for i in range(n):
        for from_node, to_node, base_time in edges:
            hour, actual_time, delay = simulate_traffic(base_time, from_node, to_node)
            log_data(from_node, to_node, hour, base_time, actual_time, delay)

        if i % 500 == 0:
            print(f"{i} samples generated")

    print("Data generation complete.")


if __name__ == "__main__":
    generate_samples(5000)
