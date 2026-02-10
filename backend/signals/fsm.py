import time

STATE_NORMAL = "NORMAL"
STATE_PREEMPT = "PREEMPT"
STATE_RECOVERY = "RECOVERY"

class SignalFSM:
    def __init__(self, redis_client, signal_id):
        self.redis = redis_client
        self.signal_id = signal_id
        self.key = f"signal:{signal_id}"

    def _set_state(self, state, owner=None, ttl=None):
        data = {
            "state": state,
            "owner": owner if owner else "",
            "last_updated": int(time.time())
        }

        self.redis.hset(self.key, mapping=data)

        if ttl:
            self.redis.expire(self.key, ttl)
    
    def enter_normal(self):
        self._set_state(STATE_NORMAL)

    def enter_preempt(self, ambulance_id, max_preempt_sec=120):
        self._set_state(
            STATE_PREEMPT,
            owner=ambulance_id,
            ttl=max_preempt_sec
        )

    def enter_recovery(self):
        self._set_state(STATE_RECOVERY)

    
    def can_preempt(self, ambulance_id):
        current = self.redis.hgetall(self.key)

        if not current:
            return True

        if current.get("state") != STATE_PREEMPT:
            return True

        return current.get("owner") == ambulance_id

        