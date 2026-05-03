from fastapi import FastAPI

app = FastAPI(title="tracking-service")


@app.get("/")
def root():
    return {
        "service": "tracking-service",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tracking/{tracking_code}")
def get_tracking(tracking_code: str):
    return {
        "tracking": tracking_code,
        "status": "in_transit",
        "location": "Sorting center",
        "updated_at": "2026-05-04"
    }
