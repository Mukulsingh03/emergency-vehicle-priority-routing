def has_deviated(redis_client, ambulance_id):
    data = redis_client.hgetall(f"ambulance:{ambulance_id}")

    if not data or "route" not in data or "current_node" not in data:
        return False

    route = data["route"].split(",")
    current_node = data["current_node"]

    return current_node not in route
