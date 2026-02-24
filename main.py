from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Order(BaseModel):
    id: Optional[str] = None
    item: str
    quantity: int
    status: str = "created"

fake_db = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/orders")
def create_order(order: Order):
    order_id = str(len(fake_db) + 1)
    order.id = order_id
    fake_db[order_id] = order
    return order

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = fake_db.get(order_id)
    if not order:
        return {"error": "not found"}
    return order

@app.put("/orders/{order_id}")
def update_order(order_id: str, order_update: Order):
    if order_id not in fake_db:
        return {"error": "not found"}
    stored = fake_db[order_id]
    update_data = order_update.dict(exclude_unset=True)
    updated = stored.copy(update=update_data)
    fake_db[order_id] = updated
    return updated