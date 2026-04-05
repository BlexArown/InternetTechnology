from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import redis


app = FastAPI(title="sessions-svc-s07")


class Session(BaseModel):
    id: int
    user: str
    ip: str


class SessionCreate(BaseModel):
    user: str
    ip: str


sessions_db: List[Session] = [
    Session(id=1, user="alice", ip="192.168.0.10"),
    Session(id=2, user="bob", ip="192.168.0.11"),
]


def get_redis_client():
    host = os.getenv("REDIS_HOST", "redis")
    port = int(os.getenv("REDIS_PORT", "6379"))
    return redis.Redis(host=host, port=port, decode_responses=True)


@app.get("/")
def root():
    return {
        "service": "sessions-svc-s07",
        "resource": "sessions",
        "status": "ok"
    }


@app.get("/health")
def health():
    try:
        client = get_redis_client()
        pong = client.ping()
        if pong:
            return {"status": "ok", "redis": "up"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Redis unavailable: {str(e)}")

    raise HTTPException(status_code=503, detail="Unknown health error")


@app.get("/sessions", response_model=List[Session])
def get_sessions():
    return sessions_db


@app.get("/sessions/{session_id}", response_model=Session)
def get_session(session_id: int):
    for session in sessions_db:
        if session.id == session_id:
            return session
    raise HTTPException(status_code=404, detail="Session not found")


@app.post("/sessions", response_model=Session)
def create_session(session_data: SessionCreate):
    new_id = 1
    if sessions_db:
        new_id = sessions_db[-1].id + 1

    new_session = Session(
        id=new_id,
        user=session_data.user,
        ip=session_data.ip
    )
    sessions_db.append(new_session)
    return new_session
