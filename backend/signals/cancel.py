from signals.signal_map import SIGNAL_MAP
from signals.fsm import SignalFSM

def cancel_all_signals(redis_client, ambulance_id):
    for signal_id in SIGNAL_MAP.values():
        fsm = SignalFSM(redis_client, signal_id)
        data = redis_client.hgetall(fsm.key)

        if data and data.get("owner") == ambulance_id:
            fsm.enter_recovery()
