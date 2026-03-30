import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import SPREADSHEET_ID

def get_creds():
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    if not creds_json:
        raise Exception("GOOGLE_CREDENTIALS environment variable not set")
    creds_dict = json.loads(creds_json)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return creds

def get_sheet(sheet_name):
    creds = get_creds()
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
    return sheet

def get_schedule_data():
    sheet = get_sheet("Учебное Расписание")
    return sheet.get_all_values()

def get_timetable_data():
    sheet = get_sheet("Расписание звонков")
    return sheet.get_all_values()

def get_students_data():
    sheet = get_sheet("Основная таблица")
    return sheet.get_all_values()
