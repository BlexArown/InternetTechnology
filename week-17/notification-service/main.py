from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="notification-service")


class NotificationCreate(BaseModel):
    message: str


notifications: List[dict] = []


@app.get("/")
def root():
    return {
        "service": "notification-service",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/notifications")
def create_notification(data: NotificationCreate):
    item = {
        "id": len(notifications) + 1,
        "message": data.message
    }
    notifications.append(item)
    return item


@app.get("/notifications")
def get_notifications():
    return notifications
