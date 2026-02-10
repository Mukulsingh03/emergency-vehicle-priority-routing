import math
from routing.sample_map import NODE_COORDS

def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def find_nearest_node(lat, lon):
    nearest_node = None
    min_distance = float("inf")

    for node_id, (node_lat, node_lon) in NODE_COORDS.items():
        d = distance(lat, lon, node_lat, node_lon)

        if d < min_distance:
            min_distance = d
            nearest_node = node_id

    return nearest_node
