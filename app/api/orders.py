from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import OrderCreate, OrderResponse
from app.crud.order import create_order, get_order as get_order_crud, list_orders as list_orders_crud, cancel_order as cancel_order_crud
from app.models import Order
from app.core.security import api_key_auth

router = APIRouter(dependencies=[Depends(api_key_auth)])

@router.post("/orders", response_model=OrderResponse)
def create(payload: OrderCreate, db: Session = Depends(get_db)):
    order = create_order(db, payload)

    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "items": [
            {
                "item_id": oi.item_id,
                "name": oi.item.name,
                "unit_price": oi.unit_price,
                "quantity": oi.quantity,
                "line_total": oi.line_total
            } for oi in order.items
        ]
    }

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get(order_id: int, db: Session = Depends(get_db)):
    order = get_order_crud(db, order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "items": [
            {
                "item_id": oi.item_id,
                "name": oi.item.name if oi.item else None,
                "unit_price": oi.unit_price,
                "quantity": oi.quantity,
                "line_total": oi.line_total
            } for oi in order.items
        ]
    }

@router.get("/orders")
def list_orders(
    page: int = 1,
    page_size: int = 10,
    customer_name: str | None = None,
    status: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    db: Session = Depends(get_db)
):
    return list_orders_crud(db, page, page_size, customer_name, status, from_date, to_date)

@router.post("/orders/{order_id}/cancel", response_model=OrderResponse)
def cancel(order_id: int, db: Session = Depends(get_db)):
    order = cancel_order_crud(db, order_id)
    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "items": [
            {
                "item_id": oi.item_id,
                "name": oi.item.name if oi.item else None,
                "unit_price": oi.unit_price,
                "quantity": oi.quantity,
                "line_total": oi.line_total
            } for oi in order.items
        ]
    }
