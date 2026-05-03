from fastapi import FastAPI, Request
from typing import List

app = FastAPI(title="reviews-svc-s07")

reviews_db = [
    {"id": 1, "text": "Good", "rating": 5, "user_id": 1},
    {"id": 2, "text": "Bad", "rating": 1, "user_id": 2},
]

# Hardcoded secret (уязвимость)
SECRET_KEY = "super_secret_key"

@app.get("/")
def root():
    return {
        "project_code": "reviews-s07",
        "service": "reviews-svc-s07",
        "status": "ok"
    }

# Нет проверки доступа (Broken Access Control)
@app.get("/reviews/{review_id}")
def get_review(review_id: int):
    for r in reviews_db:
        if r["id"] == review_id:
            return r
    return {"error": "not found"}

# Нет валидации rating
@app.post("/reviews")
async def create_review(request: Request):
    data = await request.json()

    review = {
        "id": len(reviews_db) + 1,
        "text": data.get("text"),
        "rating": data.get("rating"),
        "user_id": data.get("user_id")
    }

    reviews_db.append(review)
    return review

# Debug endpoint (лишний)
@app.get("/debug")
def debug():
    return {
        "db": reviews_db,
        "secret": SECRET_KEY
    }
