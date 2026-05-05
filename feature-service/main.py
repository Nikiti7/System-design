# feature-service/main.py
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
import asyncio
import json
import os

app = FastAPI()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = "user-events"
GROUP_ID = "feature-service-group"

feature_store = {}


# --- Kafka Consumer ---
async def consume_events():
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode("utf-8"))

            user_id = event["user_id"]
            event_type = event["event_type"]

            # --- обновление фичей ---
            if user_id not in feature_store:
                feature_store[user_id] = {"clicks": 0, "views": 0, "likes": 0}

            if event_type == "click":
                feature_store[user_id]["clicks"] += 1
            elif event_type == "view":
                feature_store[user_id]["views"] += 1
            elif event_type == "like":
                feature_store[user_id]["likes"] += 1

            print(f"Updated features for {user_id}: {feature_store[user_id]}")

    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_events())


# --- API ---
@app.get("/features/{user_id}")
async def get_features(user_id: str):
    return feature_store.get(user_id, {"message": "No features found"})
