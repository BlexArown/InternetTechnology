from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="comments-svc-s07")


class Comment(BaseModel):
    id: int
    text: str
    author: str


comments_db: List[Comment] = [
    Comment(id=1, text="First comment", author="Alice"),
    Comment(id=2, text="Second comment", author="Bob"),
]


@app.get("/")
def root():
    return {
        "project_code": "comments-s07",
        "service": "comments-svc-s07",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/comments")
def get_comments():
    return comments_db
