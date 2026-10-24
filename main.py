from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorData(BaseModel):
    co2: float
    pm25: float
    humidity: float
    soil_moisture: float

db = []

@app.post("/api/data")
def receive_data(data: SensorData):
    record = {
        **data.model_dump(),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    db.append(record)
    if len(db) > 50:
        db.pop(0)
    return {"status": "success", "data": record}

@app.get("/api/data")
def get_data():
    return db
