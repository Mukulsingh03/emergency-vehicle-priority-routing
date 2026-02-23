from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from routing.deviation import has_deviated
from routing.route_from_gps import compute_route_from_gps
from routing.nearest_hospital import find_nearest_hospital
from routing.nearest_node import find_nearest_node
from routing.sample_map import create_sample_graph
from routing.dijkstra import dijkstra
from fastapi import Body, FastAPI, Request
from pydantic import BaseModel
import redis
from time import time 
import threading
import time
from ambulance.state import is_ambulance_alive
from signals.cancel import cancel_all_signals

app= FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
        
@app.post("/compute-route")
async def compute_dashboard_route(payload: dict = Body(...)):

    start_node = payload["start_node"]
    enable_ml = payload["enable_ml"]

    result = find_nearest_hospital(start_node, enable_ml)

    return result


@app.get("/graph")
def get_graph():

    graph_obj = create_sample_graph()
    adjacency = graph_obj.adj   # <-- THIS is correct attribute

    edges = []
    seen = set()  # prevent duplicate undirected edges

    for node, neighbors in adjacency.items():
        for edge in neighbors:
            neighbor = edge["to"]

            # create sorted tuple to avoid duplicates
            edge_key = tuple(sorted([node, neighbor]))

            if edge_key not in seen:
                seen.add(edge_key)
                edges.append({
                    "source": node,
                    "target": neighbor
                })

    return {
        "nodes": list(adjacency.keys()),
        "edges": edges
    }

threading.Thread(target=monitor_ambulances, daemon=True).start()

