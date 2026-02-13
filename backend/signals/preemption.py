from signals.signal_map import SIGNAL_MAP
from signals.fsm import SignalFSM

def trigger_signal_preemption(redis_client, route, ambulance_id):
    """
    route: list of nodes, e.g. ["A", "B", "C"]
    """

    for node in route:
        if node in SIGNAL_MAP:
            signal_id = SIGNAL_MAP[node]

            fsm = SignalFSM(redis_client, signal_id)

            if fsm.can_preempt(ambulance_id):
                fsm.enter_preempt(ambulance_id)
                print(f"[PREEMPT] Signal {signal_id} preempted by {ambulance_id}")
            else:
                print(f"[SKIP] Signal {signal_id} already owned")

            break  # preempt only ONE signal ahead


def release_signal_if_passed(redis_client, route, current_node, ambulance_id):
    """
    Release signals that are behind the ambulance.
    Safe against current_node not being in route.
    """

    # Case 1: Ambulance is past the entire route
    if current_node not in route:
        for node, signal_id in SIGNAL_MAP.items():
            fsm = SignalFSM(redis_client, signal_id)
            current = redis_client.hgetall(fsm.key)

            if current and current.get("owner") == ambulance_id:
                fsm.enter_recovery()
                print(f"[RECOVERY] Signal {signal_id} released (route completed)")
        return

    # Case 2: Ambulance is somewhere on the route
    current_index = route.index(current_node)
    passed_nodes = route[:current_index]

    for node in passed_nodes:
        if node in SIGNAL_MAP:
            signal_id = SIGNAL_MAP[node]
            fsm = SignalFSM(redis_client, signal_id)

            current = redis_client.hgetall(fsm.key)
            if current and current.get("owner") == ambulance_id:
                fsm.enter_recovery()
                print(f"[RECOVERY] Signal {signal_id} released")
