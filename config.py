import os
from dotenv import load_dotenv

load_dotenv()

# Google Sheets
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
CREDENTIALS_FILE = "credentials.json"  # загрузите в корень бэкенда

# VK (для проверки админов)
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
# Пример: ADMIN_IDS=123456789,987654321

# Настройки кэша и обновления
UPDATE_INTERVAL_MINUTES = 60
CACHE_TTL_SECONDS = 3600

# Путь к БД SQLite
DATABASE_URL = "sqlite:///./users.db"