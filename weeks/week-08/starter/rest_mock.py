from fastapi import FastAPI

app = FastAPI()


@app.get("/sessions")
def get_sessions():
    return [
        {"id": "1", "ip": "192.168.0.1"},
        {"id": "2", "ip": "192.168.0.2"}
    ]
