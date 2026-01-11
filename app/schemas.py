from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

#Item schema
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    model_config = ConfigDict(extra='ignore')

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    quantity: int
    is_active: bool
    created_at: datetime
    low_stock: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


#Orders Schema

class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    customer_name: str
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    item_id: int
    name: str
    unit_price: float
    quantity: int
    line_total: float

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse]

    # Pydantic v2 config: enable ORM mode
    model_config = ConfigDict(from_attributes=True)