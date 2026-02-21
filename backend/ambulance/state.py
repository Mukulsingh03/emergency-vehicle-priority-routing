def is_ambulance_alive(redis_client, ambulance_id):
    return redis_client.exists(f"ambulance:{ambulance_id}") == 1
