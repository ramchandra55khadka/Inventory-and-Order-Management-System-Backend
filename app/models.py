from sqlalchemy import ( 
    Column,Integer,String,Float,Boolean,ForeignKey,DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String, index=True)
    status = Column(String, default="confirmed")
    total_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    unit_price = Column(Float)
    quantity = Column(Integer)
    line_total = Column(Float)

    order = relationship("Order", back_populates="items")
    item = relationship("Item")
