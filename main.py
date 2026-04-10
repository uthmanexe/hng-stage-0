from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import httpx

client = httpx.AsyncClient()
Gender_URL = "https://api.genderize.io"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail},
    )

@app.get("/api/classify")
async def gender_classifier(name: str = Query(None)):
    if not name or name.strip() == "":
        raise HTTPException(status_code=400, detail="Missing or empty name parameter")

    try:
        response = await client.get(Gender_URL, params={"name": name}, timeout=5.0)
        response.raise_for_status()
        data = response.json()
    except Exception:
        raise HTTPException(status_code=502, detail="Upstream server failure")

    gender = data.get("gender")
    probability = data.get("probability", 0)
    sample_size = data.get("count", 0)

    if not gender or sample_size == 0:
        raise HTTPException(status_code=422, detail="No prediction available for the provided name")

    is_confident = bool(probability >= 0.7 and sample_size >= 100)

    return {
        "status": "success",
        "data": {
            "name": name,
            "gender": gender,
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": is_confident,
            "processed_at": datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
        }
    }
