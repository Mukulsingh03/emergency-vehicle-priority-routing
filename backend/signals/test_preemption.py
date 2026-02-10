from redis import Redis
from signals.preemption import trigger_signal_preemption

redis_client = Redis(decode_responses=True)

route = ["A", "B", "C"]

trigger_signal_preemption(redis_client, route, "AMB001")
