import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import CREDENTIALS_FILE, SPREADSHEET_ID

def get_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
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