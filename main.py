from fastapi import FastAPI, Query, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import httpx

client = httpx.AsyncClient()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Gender_URL = "https://api.genderize.io"

@app.get("/api/classify")
async def gender_classifier(name: str = Query(None)):
    if not name:
        raise HTTPException(status_code=400, detail="A name parameter is required")
    try:
        response = await client.get(f"{Gender_URL}?name={name}")
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        raise HTTPException(status_code=error.response.status_code, detail=error.response.text)
    data = response.json()

    gender = data.get("gender")
    probability = data.get("probability", 0)
    sample_size = data.get("count", 0)

    if not gender or sample_size == 0:
        raise HTTPException(status_code=422, detail=f"Failed to determin gender for name '{name}'.")

    is_confident = probability > 0.7 and sample_size >= 100

    timestamp = datetime.now(timezone.utc).isoformat()

    return {
        "name": name,
        "gender": gender,
        "probability": probability,
        "sample_size": sample_size,
        "is_confident": is_confident,
        "timestamp": timestamp,
    }
