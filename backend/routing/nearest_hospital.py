from routing.sample_map import create_sample_graph
from routing.dijkstra import dijkstra
from routing.hospitals import HOSPITALS

def find_nearest_hospital(start_node):
    graph = create_sample_graph()

    best_hospital = None
    best_time = float("inf")
    best_path = None

    for hospital_id, hospital_node in HOSPITALS.items():
        path, travel_time = dijkstra(graph, start_node, hospital_node)

        if travel_time < best_time:
            best_time = travel_time
            best_hospital = hospital_id
            best_path = path


    return {
        "hospital_id": best_hospital,
        "path": best_path,
        "estimated_time": best_time
    }        