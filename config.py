import os
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
CACHE_TTL_SECONDS = 3600
DATABASE_URL = "sqlite:///./users.db"
