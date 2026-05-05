# event-service/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer
import asyncio
import json
import os

app = FastAPI()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = "user-events"

producer = None


class Event(BaseModel):
    user_id: str
    event_type: str
    item_id: str
    timestamp: int


@app.on_event("startup")
async def startup_event():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()


@app.post("/events")
async def send_event(event: Event):
    message = json.dumps(event.dict()).encode("utf-8")
    await producer.send_and_wait(TOPIC, message)
    return {"status": "event sent"}
