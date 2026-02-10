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
