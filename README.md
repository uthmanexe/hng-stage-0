A simple asynchronous API built with **FastAPI** that determines the gender of a given name. It fetches data from the **Genderize API** and calculates a "confidence" score based on statistical probability and sample size.

## Technologies used Stack
- **Language:** Python
- **Framework:** FastAPI (Running on Uvicorn)
- **Async Client:** HTTPX
- **Deployment:** Railway

## How to Use
Call the endpoint using `curl`, **Postman**, **Bruno**, or any HTTP client of your choice.

**Base URL:** `https://web-production-f2430.up.railway.app`  
**Endpoint:** `/api/classify`

## Request reference:
<Base_URL>/api/classify/?name=mike (GET Method)

Response:
{
  "status": "success",
  "data": {
    "name": "mike",
    "gender": "male",
    "probability": 1.0,
    "sample_size": 1145946,
    "is_confident": true,
    "processed_at": "2026-04-12T14:15:30.843464+00:00"
  }
}
