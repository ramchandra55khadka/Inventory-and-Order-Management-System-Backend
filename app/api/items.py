from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import ItemCreate, ItemUpdate, ItemResponse
from app.models import Item
from app.crud.item import create_item, list_items as list_items_crud, get_item as get_item_crud, update_item as update_item_crud, soft_delete_item
from app.core.security import api_key_auth
from app.core.config import LOW_STOCK_THRESHOLD

router = APIRouter(dependencies=[Depends(api_key_auth)])

@router.post("/items", response_model=ItemResponse)
def create(data: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, data)

@router.get("/items")
def list_items(
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):
    return list_items_crud(db, page, page_size, search, min_price, max_price)

@router.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = get_item_crud(db, item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    response = ItemResponse.model_validate(item)
    response.low_stock = item.quantity < LOW_STOCK_THRESHOLD
    return response

@router.put("/items/{item_id}", response_model=ItemResponse)
def update_put(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    return update_item_crud(db, item_id, payload)

@router.patch("/items/{item_id}", response_model=ItemResponse)
def update_patch(
    item_id: int,
    payload: ItemUpdate | None = Body(default=None),
    db: Session = Depends(get_db)
):
    # Treat missing body as empty update
    data = payload or ItemUpdate()
    return update_item_crud(db, item_id, data)

@router.delete("/items/{item_id}", response_model=ItemResponse)
def soft_delete(item_id: int, db: Session = Depends(get_db)):
    return soft_delete_item(db, item_id)
