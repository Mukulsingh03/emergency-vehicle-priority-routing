import heapq


def dijkstra(graph, start, end, use_ml=True):
    pq = []
    heapq.heappush(pq, (0, start))

    distances = {start: 0}
    previous = {}

    # Import only if ML is enabled
    if use_ml:
        from ml.predict_delay import predict_delay

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node == end:
            break

        for edge in graph.adj.get(current_node, []):
            neighbor = edge["to"]
            base_time = edge["base_time"]

            predicted_delay = 0

            if use_ml:
                try:
                    predicted_delay = predict_delay(base_time)

                    # Safety lower bound
                    predicted_delay = max(predicted_delay, -base_time)

                    # Optional upper bound
                    predicted_delay = min(predicted_delay, base_time * 3)

                except Exception:
                    predicted_delay = 0

            actual_time = base_time + predicted_delay
            new_dist = current_dist + actual_time

            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_dist, neighbor))

    if end not in distances:
        return None, float("inf")

    # Reconstruct path
    path = []
    node = end

    while node != start:
        path.append(node)
        node = previous[node]

    path.append(start)
    path.reverse()

    return path, distances[end]
