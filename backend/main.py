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


