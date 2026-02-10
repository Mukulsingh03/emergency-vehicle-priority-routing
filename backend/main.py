from routing.nearest_node import find_nearest_node
from routing.sample_map import create_sample_graph
from routing.dijkstra import dijkstra


from fastapi import FastAPI
from pydantic import BaseModel
import redis
import time 

app= FastAPI()

#connect to redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

@app.on_event("startup")
def startup_check():
    redis_client.ping()
    print("Redis connected successfully")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "redis": "connected"
    }

class AmbulanceGPS(BaseModel):
    ambulance_id: str
    lat: float
    lon: float
    speed: float
    


@app.post("/ambulance/gps")
def update_ambulance_gps(data: AmbulanceGPS):
    key = f"ambulance:{data.ambulance_id}"

    redis_client.hset(key, mapping={
        "lat": data.lat,
        "lon": data.lon,
        "speed": data.speed,
        "last_seen": int(time.time())
        
    })

    # Set TTL to 10 seconds
    redis_client.expire(key, 10)

    return {
        "message": "GPS updated",
        "ambulance_id": data.ambulance_id
    }

@app.get("/route")
def compute_route(start: str, end: str):
    graph = create_sample_graph()
    path, time_taken = dijkstra(graph, start, end)

    return {
        "path": path,
        "estimated_time": time_taken
    }



@app.get("/nearest-node")
def nearest_node(lat: float, lon: float):
    node = find_nearest_node(lat, lon)
    
    return {
        "lat": lat,
        "lon": lon,
        "nearest_node": node
    }