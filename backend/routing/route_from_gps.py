from routing.nearest_node import find_nearest_node
from routing.nearest_hospital import find_nearest_hospital

def compute_route_from_gps(lat, lon):
    start_node = find_nearest_node(lat, lon)

    hospital_result = find_nearest_hospital(start_node)

    return {
        "start_node": start_node,
        "hospital_id": hospital_result["hospital_id"],
        "path": hospital_result["path"],
        "estimated_time": hospital_result["estimated_time"]
    }
