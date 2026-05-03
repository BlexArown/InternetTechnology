from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI(title="shipments-svc-s07")


class ShipmentCreate(BaseModel):
    recipient: str
    address: str
    tracking: str


class Shipment(BaseModel):
    id: int
    recipient: str
    address: str
    tracking: str
    status: str


shipments_db: List[Shipment] = [
    Shipment(
        id=1,
        recipient="Alice",
        address="Amsterdam",
        tracking="TRK-001",
        status="created"
    )
]


@app.get("/")
def root():
    return {
        "project_code": "shipments-s07",
        "service": "shipments-svc-s07",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/shipments", response_model=List[Shipment])
def get_shipments():
    return shipments_db


@app.get("/shipments/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: int):
    for shipment in shipments_db:
        if shipment.id == shipment_id:
            return shipment
    raise HTTPException(status_code=404, detail="Shipment not found")


@app.post("/shipments", response_model=Shipment)
def create_shipment(data: ShipmentCreate):
    new_shipment = Shipment(
        id=len(shipments_db) + 1,
        recipient=data.recipient,
        address=data.address,
        tracking=data.tracking,
        status="created"
    )

    shipments_db.append(new_shipment)

    try:
        requests.post(
            "http://notification-service:8232/notifications",
            json={
                "message": f"Shipment {new_shipment.tracking} created"
            },
            timeout=2
        )
    except Exception:
        pass

    return new_shipment


@app.get("/shipments/{shipment_id}/tracking")
def get_tracking(shipment_id: int):
    shipment = get_shipment(shipment_id)

    try:
        response = requests.get(
            f"http://tracking-service:8231/tracking/{shipment.tracking}",
            timeout=2
        )
        return response.json()
    except Exception:
        raise HTTPException(status_code=503, detail="Tracking service unavailable")
