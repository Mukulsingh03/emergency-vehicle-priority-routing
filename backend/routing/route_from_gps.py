from signals.signal_map import SIGNAL_MAP
import time
from routing.nearest_node import find_nearest_node
from routing.nearest_hospital import find_nearest_hospital
from signals.preemption import (
    trigger_signal_preemption,
    release_signal_if_passed
)

def compute_route_from_gps(lat, lon, redis_client, ambulance_id):
    current_node = find_nearest_node(lat, lon)

    if current_node is None:
        raise ValueError("Unable to map GPS to road node")

    hospital_result = find_nearest_hospital(current_node)
    route = hospital_result["path"]

    redis_client.hset(
    f"ambulance:{ambulance_id}",
    "route",
    ",".join(route)
    )

    if not route:
        raise ValueError("Computed route is empty")

    trigger_signal_preemption(redis_client, route, ambulance_id)
    release_signal_if_passed(redis_client, route, current_node, ambulance_id)


    route_length = len(route)
    num_signals = sum(1 for n in route if n in SIGNAL_MAP)

    now = time.localtime()
    is_peak = now.tm_hour in range(8, 11) or now.tm_hour in range(17, 20)

    actual_time = simulate_actual_time(
    hospital_result["estimated_time"],
    num_signals,
    is_peak
    )

    log_route_data(
    route_length,
    num_signals,
    hospital_result["estimated_time"],
    actual_time
    )


    return {
        "current_node": current_node,
        "hospital_id": hospital_result["hospital_id"],
        "path": route,
        "estimated_time": hospital_result["estimated_time"]
    }

