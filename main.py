import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import CREDENTIALS_FILE, SPREADSHEET_ID

def get_sheet(sheet_name):
    # Получаем абсолютный путь к файлу credentials.json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(base_dir, CREDENTIALS_FILE)
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
    return sheet

# остальные функции без изменений