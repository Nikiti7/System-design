# recommendation-service/main.py
from fastapi import FastAPI
import redis
import json
import httpx
import random
import os

app = FastAPI()

# --- Redis ---
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# --- Feature Service ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
FEATURE_SERVICE_URL = os.getenv("FEATURE_SERVICE_URL", "http://localhost:8002")

# --- Mock items ---
ITEMS = ["movie_1", "movie_2", "movie_3", "movie_4", "movie_5"]


# --- Mock ML model ---
def run_inference(features):
    scores = {}
    for item in ITEMS:
        scores[item] = random.random()
    return scores


# --- Ranking ---
def rank_items(scores):
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# --- API ---
@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    cache_key = f"rec:{user_id}"

    cached = redis_client.get(cache_key)
    if cached:
        return {"source": "cache", "data": json.loads(cached)}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FEATURE_SERVICE_URL}/features/{user_id}")
        features = response.json()

    scores = run_inference(features)
    ranked = rank_items(scores)
    recommendations = [item for item, _ in ranked[:3]]

    redis_client.setex(
        cache_key,
        600,  # TTL = 10 минут
        json.dumps(recommendations),
    )

    return {"source": "computed", "data": recommendations}
