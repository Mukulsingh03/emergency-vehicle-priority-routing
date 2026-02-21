from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routing.deviation import has_deviated
from routing.route_from_gps import compute_route_from_gps
from routing.route_from_gps import compute_route_from_gps
from routing.nearest_hospital import find_nearest_hospital
from routing.nearest_node import find_nearest_node
from routing.sample_map import create_sample_graph
from routing.dijkstra import dijkstra
from fastapi import FastAPI
from pydantic import BaseModel
import redis
from time import time 
import threading
import time
from ambulance.state import is_ambulance_alive
from signals.cancel import cancel_all_signals

app= FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

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
def update_ambulance_gps(data: dict):
    ambulance_id = data["ambulance_id"]
    lat = data["lat"]
    lon = data["lon"]

    current_node = find_nearest_node(lat, lon)

    key = f"ambulance:{ambulance_id}"

    redis_client.hset(
        key,
        mapping={
            "lat": lat,
            "lon": lon,
            "current_node": current_node,
            "last_seen": int(time.time())
        }
    )
    redis_client.expire(key, 10)

    # ===============================
    # INITIAL ROUTE COMPUTATION
    # ===============================
    if not redis_client.hexists(key, "route"):
        compute_route_from_gps(
            lat,
            lon,
            redis_client,
            ambulance_id
        )

    # ===============================
    # DEVIATION-BASED REROUTE
    # ===============================
    elif has_deviated(redis_client, ambulance_id):
        compute_route_from_gps(
            lat,
            lon,
            redis_client,
            ambulance_id
        )

    return {"status": "GPS updated"}


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



@app.get("/nearest-hospital")
def nearest_hospital(start_node: str, use_ml: bool = True):
    result = find_nearest_hospital(start_node, use_ml)
    print("USE_ML RECEIVED:", use_ml)     

    return result


@app.get("/route-from-gps")
def route_from_gps(lat: float, lon: float, ambulance_id: str):
    result = compute_route_from_gps(lat, lon, redis_client, ambulance_id)
    return result

def monitor_ambulances():
    while True:
        for key in redis_client.scan_iter("ambulance:*"):
            ambulance_id = key.split(":")[1]
            if not is_ambulance_alive(redis_client, ambulance_id):
                cancel_all_signals(redis_client, ambulance_id)
        time.sleep(2)
        


threading.Thread(target=monitor_ambulances, daemon=True).start()