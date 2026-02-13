import heapq

def dijkstra(graph, start, end):
    pq = []
    heapq.heappush(pq, (0, start))

    distances = {start: 0}
    previous = {}

    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_node == end:
            break

        for neighbor, weight in graph.adj.get(current_node, []):
            new_dist = current_dist + weight

            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_dist, neighbor)
                               )
    
    if end not in previous:
        return None, float("inf")



    path = []
    node = end

    while node != start:
        path.append(node)    
        node = previous[node]

    path.append(start)
    path.reverse()


    return path, distances[end]        