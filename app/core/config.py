import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:ramchandra@localhost:5432/inventory_db")
API_KEY = os.getenv("API_KEY")
LOW_STOCK_THRESHOLD = int(os.getenv("LOW_STOCK_THRESHOLD", "5"))