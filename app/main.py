from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.requests import Request
from app.database import engine, Base
from app.api import items, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory & Orders Managemnt  API")

app.include_router(items.router)

app.include_router(orders.router)

# Global fallback error handler for uncaught exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
	return JSONResponse(status_code=500, content={"detail": "Internal server error"})
