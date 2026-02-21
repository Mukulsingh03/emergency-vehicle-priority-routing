from routing.sample_map import create_sample_graph
from routing.dijkstra import dijkstra
from routing.hospitals import HOSPITALS


def find_nearest_hospital(start_node, use_ml=True):
    graph = create_sample_graph()

    # ---- ML Route ----
    selected_result = _find_best_route(graph, start_node, use_ml)

    comparison_base = _find_best_route(graph, start_node, use_ml=False)

    return {
        "hospital_id": selected_result["hospital_id"],
        "path": selected_result["path"],
        "ml_time": selected_result["estimated_time"],
        "base_time": comparison_base["estimated_time"]
    }



def _find_best_route(graph, start_node, use_ml):
    best_hospital = None
    best_time = float("inf")
    best_path = None

    for hospital_id, hospital_node in HOSPITALS.items():

        # Already at hospital
        if start_node == hospital_node:
            return {
                "hospital_id": hospital_id,
                "path": [start_node],
                "estimated_time": 0
            }

        path, travel_time = dijkstra(graph, start_node, hospital_node, use_ml)

        if path is None:
            continue

        if travel_time < best_time:
            best_time = travel_time
            best_hospital = hospital_id
            best_path = path

    if best_path is None:
        raise ValueError("No reachable hospital from current node")

    return {
        "hospital_id": best_hospital,
        "path": best_path,
        "estimated_time": best_time
    }
