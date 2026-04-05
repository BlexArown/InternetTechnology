from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI(title="orders-svc-s07")


class Order(BaseModel):
    id: int
    name: str
    priority: int


class OrderCreate(BaseModel):
    name: str
    priority: int


orders_db: List[Order] = [
    Order(id=1, name="First order", priority=1),
    Order(id=2, name="Second order", priority=2),
]


@app.get("/")
def root():
    return {
        "service": "orders-svc-s07",
        "resource": "orders",
        "status": "ok"
    }


@app.get("/orders", response_model=List[Order])
def get_orders():
    return orders_db


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    for order in orders_db:
        if order.id == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")


@app.post("/orders", response_model=Order)
def create_order(order_data: OrderCreate):
    new_id = 1
    if orders_db:
        new_id = orders_db[-1].id + 1

    new_order = Order(
        id=new_id,
        name=order_data.name,
        priority=order_data.priority
    )
    orders_db.append(new_order)
    return new_order
