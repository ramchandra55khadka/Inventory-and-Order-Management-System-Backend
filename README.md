# Inventory & Orders Management API

## Overview
This project provides a simple backend API for managing inventory items and customer orders. It includes:
- Item CRUD with soft delete and filtering/pagination
- Order creation with stock validation, total computation, and item breakdown
- Order listing with filters and pagination, read by ID, and cancel (stock restoration)
- Simple API key authentication on all endpoints

Tech stack:
- FastAPI, SQLAlchemy
- Pydantic v2 for request/response models
- Alembic for database migrations

## Setup

### 1) Environment variables
Create an `.env` file (or set environment variables) with at least:
- `DATABASE_URL` (e.g., `postgresql://postgres:ramchandra@localhost:5432/inventory_db` or `sqlite:///./dev.db`)
- `API_KEY` (e.g., `mysecretkey`)
- `LOW_STOCK_THRESHOLD` (default is 5 if not set)

### 2) Install dependencies
Using uv:
```zsh
uv sync
```

### 3) Database
Using Alembic migrations:
```zsh
export DATABASE_URL=postgresql://postgres:ramchandra@localhost:5432/inventory_db
alembic upgrade head
```


## Running the server
```zsh
uv run uvicorn app.main:app --reload
```

## Running tests
```zsh
uv run pytest -q
```

## API summary

Authentication: Every endpoint requires header `X-API-KEY: <your key>`.

### Items
- POST `/items` → Create an item
	- Body: `{ name, price, quantity, description? }`
	- Constraints: unique `name` among active items

- GET `/items` → List items with filters + pagination
	- Query: `search`, `min_price`, `max_price`, `page`, `page_size`
	- Response: `{ items, total, page, page_size }`

- GET `/items/{id}` → Get single item
	- If `quantity < LOW_STOCK_THRESHOLD`, response includes `low_stock: true`

- PUT/PATCH `/items/{id}` → Update item (name, description, price, quantity)
	- Respects name uniqueness

- DELETE `/items/{id}` → Soft delete (sets `is_active=false`)

### Orders
- POST `/orders` → Create order
	- Validates item IDs and stock
	- Deducts stock in a single transaction
	- Computes order total and returns item breakdown

- GET `/orders/{id}` → Get order by ID

- GET `/orders` → List orders with filters + pagination
	- Query: `customer_name`, `status`, `from_date`, `to_date`, `page`, `page_size`

- POST `/orders/{id}/cancel` → Cancel order
	- Restores stock and sets status to `cancelled`

### Errors
Standard FastAPI error responses, e.g.: `{ "detail": "Item not found" }`
- 400 validation / stock errors
- 404 not found
- 401 missing API key, 403 invalid API key
- 500 fallback internal server error

## Author
Ramchandra Khadka

Task Completed:Yes
