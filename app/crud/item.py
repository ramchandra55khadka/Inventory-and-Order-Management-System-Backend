from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_
from app.models import Item

def create_item(db: Session, data):
    exists = db.query(Item).filter(
        and_(Item.name == data.name, Item.is_active == True)
    ).first()
    if exists:
        raise HTTPException(400, "Item name already exists")

    item = Item(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_items(db: Session, page: int = 1, page_size: int = 10, search: str | None = None,
               min_price: float | None = None, max_price: float | None = None):
    q = db.query(Item).filter(Item.is_active == True)
    if search:
        q = q.filter(Item.name.ilike(f"%{search}%"))
    if min_price is not None:
        q = q.filter(Item.price >= min_price)
    if max_price is not None:
        q = q.filter(Item.price <= max_price)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id, Item.is_active == True).first()

def update_item(db: Session, item_id: int, data):
    item = db.query(Item).filter(Item.id == item_id, Item.is_active == True).first()
    if not item:
        raise HTTPException(404, "Item not found")
    if data.name and data.name != item.name:
        conflict = db.query(Item).filter(and_(Item.name == data.name, Item.is_active == True, Item.id != item_id)).first()
        if conflict:
            raise HTTPException(400, "Item name already exists")
    # apply changes
    payload = data.model_dump(exclude_unset=True)
    if not payload:
        return item
    for k, v in payload.items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item

def soft_delete_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id, Item.is_active == True).first()
    if not item:
        raise HTTPException(404, "Item not found")
    item.is_active = False
    db.commit()
    db.refresh(item)
    return item
