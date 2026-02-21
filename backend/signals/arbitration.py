import time

def compute_priority(
        emergency_level: int,
        distance_to_signal: int,
        waiting_since: int
):
    W1, W2, W3 = 100, 10 ,1

    waiting_time = int(time.time()) - waiting_since

    return (
        W1 * emergency_level
        + W2 * (1 / max(distance_to_signal, 1))
        + W3 * waiting_time
    )

def submit_claim(
    redis_client,
    signal_id,
    ambulance_id,
    priority_score
):
    claims_key = f"signal:{signal_id}:claims"

    redis_client.zadd(
        claims_key,
        {ambulance_id: priority_score}
    )

    redis_client.expire(claims_key, 10)


def elect_winner(redis_client, signal_id):
    print("ELECT_WINNER CALLED")
    owner_key = f"signal:{signal_id}:owner"
    claims_key = f"signal:{signal_id}:claims"

    # 1. If an owner already exists, respect it
    current_owner = redis_client.get(owner_key)
    print(f"CURRENT OWNER IN REDIS: {current_owner}")
    if current_owner:
        return current_owner

    # 2. Otherwise elect highest priority claimant
    winner = redis_client.zrevrange(claims_key, 0, 0)

    if not winner:
        return None

    winner_id = winner[0]

    redis_client.set(owner_key, winner_id, ex=10)
    return winner_id


