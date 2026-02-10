from routing.nearest_node import find_nearest_node
from routing.nearest_hospital import find_nearest_hospital
from signals.preemption import trigger_signal_preemption

def compute_route_from_gps(lat, lon, redis_client, ambulance_id):
    start_node = find_nearest_node(lat, lon)
    hospital_result = find_nearest_hospital(start_node)

    route = hospital_result["path"]

    trigger_signal_preemption(redis_client, route, ambulance_id)

    return {
        "start_node": start_node,
        "hospital_id": hospital_result["hospital_id"],
        "path": route,
        "estimated_time": hospital_result["estimated_time"]
    }

    
