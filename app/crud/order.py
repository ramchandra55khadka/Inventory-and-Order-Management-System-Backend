from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Item, Order, OrderItem

def create_order(db: Session, payload):
    order_items = []
    total = 0

    for req in payload.items:
        item = db.query(Item).filter(
            Item.id == req.item_id,
            Item.is_active == True
        ).first()

        if not item:
            raise HTTPException(404, f"Item {req.item_id} not found")

        if item.quantity < req.quantity:
            raise HTTPException(400, f"Insufficient stock for item {item.name}")

        item.quantity -= req.quantity
        line_total = item.price * req.quantity
        total += line_total

        order_items.append(
            OrderItem(
                item_id=item.id,
                unit_price=item.price,
                quantity=req.quantity,
                line_total=line_total
            )
        )

    order = Order(
        customer_name=payload.customer_name,
        status="confirmed",
        total_amount=total,
        items=order_items
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def list_orders(db: Session, page: int = 1, page_size: int = 10, customer_name: str | None = None,
                status: str | None = None, from_date: str | None = None, to_date: str | None = None):
    q = db.query(Order)
    if customer_name:
        q = q.filter(Order.customer_name.ilike(f"%{customer_name}%"))
    if status:
        q = q.filter(Order.status == status)
    if from_date:
        q = q.filter(Order.created_at >= from_date)
    if to_date:
        q = q.filter(Order.created_at <= to_date)
    total = q.count()
    orders = q.offset((page - 1) * page_size).limit(page_size).all()
    return {"orders": orders, "total": total, "page": page, "page_size": page_size}

def cancel_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    if order.status == "cancelled":
        return order
    # restore stock
    for oi in order.items:
        item = db.query(Item).filter(Item.id == oi.item_id).first()
        if item:
            item.quantity += oi.quantity
    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return order
