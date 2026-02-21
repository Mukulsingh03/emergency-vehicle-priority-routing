import random
from datetime import datetime

def simulate_traffic(base_time, from_node, to_node):
    hour = datetime.now().hour

    # Peak traffic intensity
    if 8 <= hour <= 10 or 17 <= hour <= 20:
        base_multiplier = random.uniform(0.8, 1.4)
    else:
        base_multiplier = random.uniform(0.2, 0.6)

    # Non-linear penalty (break proportional scaling)
    nonlinear_component = (base_time ** 1.2) / 10

    # Deterministic edge-specific variation
    edge_seed = hash((from_node, to_node, hour))
    random.seed(edge_seed)
    edge_variation = random.uniform(-3, 6)

    delay = base_time * base_multiplier + nonlinear_component + edge_variation
    actual_time = base_time + delay

    return hour, actual_time, delay
