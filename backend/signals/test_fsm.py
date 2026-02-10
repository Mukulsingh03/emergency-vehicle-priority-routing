from redis import Redis
from signals.fsm import SignalFSM

redis_client = Redis(decode_responses=True)

signal = SignalFSM(redis_client, "SIG_1")

signal.enter_normal()
print("State:", redis_client.hget("signal:SIG_1", "state"))

signal.enter_preempt("AMB001")
print("State:", redis_client.hget("signal:SIG_1", "state"))
print("Owner:", redis_client.hget("signal:SIG_1", "owner"))
