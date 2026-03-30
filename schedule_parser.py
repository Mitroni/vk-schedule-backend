import re
from datetime import datetime, timedelta
import locale

try:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'russian')
    except:
        pass

TIMETABLE = {}

def load_timetable(timetable_data):
    """Загружает расписание звонков"""
    global TIMETABLE
    TIMETABLE = {}
    
    if not timetable_data:
        print("⚠️ Расписание звонков не загружено")
        return
    
    for row in timetable_data:
        if len(row) >= 2:
            pair_cell = str(row[0]).strip().lower()
            time_range = str(row[1]).strip()
            
            if "перерыв" in pair_cell:
                continue
            if pair_cell in ["№ пары", "пара", "пары", "№"]:
                continue
            
            match = re.search(r'(\d+)', pair_cell)
            if match:
                pair_number = match.group(1)
                TIMETABLE[pair_number] = time_range
                print(f"   ✅ {pair_number} пара: {time_range}")
    
    print(f"📊 Загружено расписание для {len(TIMETABLE)} пар")

def get_pair_time(pair_num):
    """Получить время пары"""
    match = re.search(r'(\d+)', str(pair_num))
    if match:
        return TIMETABLE.get(match.group(1), "")
    return ""

def parse_schedule(data):
    """
    Парсит расписание с определением корпуса из колонки E
    """
    if not data:
        return {}
    
    schedule = {}
    current_date = None
    current_pairs = []
    
    for row in data:
        if len(row) < 5:
            row = row + [''] * (5 - len(row))
        
        date_cell = row[0].strip() if row[0] else ""
        pair_num = row[1].strip() if len(row) > 1 and row[1] else ""
        discipline = row[2].strip() if len(row) > 2 and row[2] else ""
        room = row[3].strip() if len(row) > 3 and row[3] else ""
        building_cell = row[4].strip() if len(row) > 4 and row[4] else ""
        
        building = "Первый учебный корпус"
        if building_cell:
            building_lower = building_cell.lower()
            if "2" in building_lower or "второй" in building_lower or "втор" in building_lower:
                building = "Второй учебный корпус"
            elif "1" in building_lower or "первый" in building_lower or "перв" in building_lower:
                building = "Первый учебный корпус"
        
        if not date_cell and not pair_num and not discipline:
            continue
        
        is_date = False
        if date_cell:
            if not re.match(r'^\d+\s*пара', date_cell, re.IGNORECASE):
                if not date_cell.startswith('Условные'):
                    if not date_cell.startswith('Первый'):
                        if not date_cell.startswith('Второй'):
                            if not date_cell.startswith('Дата'):
                                is_date = True
        
        if is_date:
            if current_date and current_pairs:
                schedule[current_date] = current_pairs
            
            date_cell = date_cell.replace("вотрник", "вторник")
            date_cell = date_cell.replace("стреда", "среда")
            
            current_date = date_cell
            current_pairs = []
            
            if pair_num:
                current_pairs.append((pair_num, discipline, room, building))
        else:
            if current_date and pair_num:
                current_pairs.append((pair_num, discipline, room, building))
    
    if current_date and current_pairs:
        schedule[current_date] = current_pairs
    
    return schedule

def find_date_in_schedule(schedule_dict, target_date):
    """Ищет дату в расписании (гибкий поиск с нормализацией пробелов)"""
    day = target_date.day
    month_num = target_date.month

    months_ru = {
        1: ['января', 'январь'], 2: ['февраля', 'февраль'],
        3: ['марта', 'март'], 4: ['апреля', 'апрель'],
        5: ['мая', 'май'], 6: ['июня', 'июнь'],
        7: ['июля', 'июль'], 8: ['августа', 'август'],
        9: ['сентября', 'сентябрь'], 10: ['октября', 'октябрь'],
        11: ['ноября', 'ноябрь'], 12: ['декабря', 'декабрь'],
    }

    variants = []
    for month_var in months_ru[month_num]:
        variants.append(f"{day} {month_var}")
        variants.append(f"{day:02d} {month_var}")

    for key_date in schedule_dict.keys():
        key_normalized = ' '.join(key_date.split())
        for variant in variants:
            if variant in key_normalized:
                return schedule_dict[key_date]

    return None

def get_day_name(date_obj):
    """Возвращает название дня недели на русском"""
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    return days[date_obj.weekday()]

def format_schedule(date_obj, pairs):
    """Форматирует расписание для отправки с адресами корпусов"""
    if not pairs:
        day_name = get_day_name(date_obj)
        return f"📅 {date_obj.day} {date_obj.strftime('%B')} ({day_name})\n\n✅ Пар нет. Выходной день!"
    
    day_name = get_day_name(date_obj)
    months_ru = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }
    month_name = months_ru[date_obj.month]
    
    text = f"📚 РАСПИСАНИЕ\n"
    text += f"📅 {date_obj.day} {month_name} {date_obj.year} ({day_name})\n"
    text += "═" * 35 + "\n\n"
    
    buildings = set()
    
    for pair_data in pairs:
        if len(pair_data) == 4:
            pair_num, discipline, room, building = pair_data
        else:
            pair_num, discipline, room = pair_data[:3]
            building = "Первый учебный корпус"
        
        if not discipline:
            text += f"⚪ {pair_num}: ❌ НЕТ ПАРЫ\n\n"
            continue
        
        time_str = f" [{get_pair_time(pair_num)}]" if get_pair_time(pair_num) else ""
        text += f"🔵 {pair_num}{time_str}: {discipline}\n"
        if room and room != "":
            text += f"   🪑 Ауд. {room}\n"
        if building:
            text += f"   📍 {building}\n"
            buildings.add(building)
        text += "\n"
    
    text += f"🍽️ **Обеденный перерыв: 11:40 - 12:20**\n\n"
    
    if buildings:
        text += "─" * 35 + "\n\n"
        text += "📍 АДРЕСА КОРПУСОВ:\n"
        for b in buildings:
            if "Первый" in b:
                text += "   🏛️ **Первый учебный корпус** — Тутаевское ш., 58\n"
            elif "Второй" in b:
                text += "   🏛️ **Второй учебный корпус** — ул. Е. Колесовой, 70\n"
            else:
                text += f"   🏛️ {b}\n"
    
    text += "\n" + "═" * 35
    return text
import re
from datetime import datetime, timedelta
import locale

try:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'russian')
    except:
        pass

TIMETABLE = {}

def load_timetable(timetable_data):
    """Загружает расписание звонков"""
    global TIMETABLE
    TIMETABLE = {}
    
    if not timetable_data:
        print("⚠️ Расписание звонков не загружено")
        return
    
    for row in timetable_data:
        if len(row) >= 2:
            pair_cell = str(row[0]).strip().lower()
            time_range = str(row[1]).strip()
            
            if "перерыв" in pair_cell:
                continue
            if pair_cell in ["№ пары", "пара", "пары", "№"]:
                continue
            
            match = re.search(r'(\d+)', pair_cell)
            if match:
                pair_number = match.group(1)
                TIMETABLE[pair_number] = time_range
                print(f"   ✅ {pair_number} пара: {time_range}")
    
    print(f"📊 Загружено расписание для {len(TIMETABLE)} пар")

def get_pair_time(pair_num):
    """Получить время пары"""
    match = re.search(r'(\d+)', str(pair_num))
    if match:
        return TIMETABLE.get(match.group(1), "")
    return ""

def parse_schedule_with_building(data):
    """
    Парсит расписание с определением корпуса из колонки E
    Возвращает словарь: {дата: [(номер_пары, дисциплина, аудитория, корпус), ...]}
    """
    if not data:
        return {}
    
    schedule = {}
    current_date = None
    current_pairs = []
    
    for row in data:
        if len(row) < 5:
            row = row + [''] * (5 - len(row))
        
        date_cell = row[0].strip() if row[0] else ""
        pair_num = row[1].strip() if len(row) > 1 and row[1] else ""
        discipline = row[2].strip() if len(row) > 2 and row[2] else ""
        room = row[3].strip() if len(row) > 3 and row[3] else ""
        building_cell = row[4].strip() if len(row) > 4 and row[4] else ""
        
        # Определяем корпус
        building = "Первый учебный корпус"
        if building_cell:
            if building_cell in ["2", "Второй", "второй", "2 корпус"]:
                building = "Второй учебный корпус"
            elif building_cell in ["1", "Первый", "первый", "1 корпус"]:
                building = "Первый учебный корпус"
        
        # Пропускаем пустые строки
        if not date_cell and not pair_num and not discipline:
            continue
        
        # Проверяем, является ли ячейка датой
        is_date = False
        if date_cell:
            if not re.match(r'^\d+\s*пара', date_cell, re.IGNORECASE):
                if not date_cell.startswith('Условные'):
                    if not date_cell.startswith('Первый'):
                        if not date_cell.startswith('Второй'):
                            if not date_cell.startswith('Дата'):
                                is_date = True
        
        if is_date:
            if current_date and current_pairs:
                schedule[current_date] = current_pairs
            
            # Исправляем опечатки
            date_cell = date_cell.replace("вотрник", "вторник")
            date_cell = date_cell.replace("стреда", "среда")
            
            current_date = date_cell
            current_pairs = []
            
            if pair_num:
                current_pairs.append((pair_num, discipline, room, building))
        else:
            if current_date and pair_num:
                current_pairs.append((pair_num, discipline, room, building))
    
    if current_date and current_pairs:
        schedule[current_date] = current_pairs
    
    return schedule

def find_date_in_schedule(schedule_dict, target_date):
    """Ищет дату в расписании"""
    day = target_date.day
    month_num = target_date.month
    
    months_ru = {
        1: ['января', 'январь'], 2: ['февраля', 'февраль'],
        3: ['марта', 'март'], 4: ['апреля', 'апрель'],
        5: ['мая', 'май'], 6: ['июня', 'июнь'],
        7: ['июля', 'июль'], 8: ['августа', 'август'],
        9: ['сентября', 'сентябрь'], 10: ['октября', 'октябрь'],
        11: ['ноября', 'ноябрь'], 12: ['декабря', 'декабрь'],
    }
    
    days_ru = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    target_weekday = days_ru[target_date.weekday()]
    
    search_variants = []
    for month_var in months_ru[month_num]:
        search_variants.append(f"{day} {month_var}")
        search_variants.append(f"{day} {month_var} {target_weekday}")
    
    for key_date in schedule_dict.keys():
        for variant in search_variants:
            if variant.lower() in key_date.lower():
                return schedule_dict[key_date]
    
    return None

def get_day_name(date_obj):
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    return days[date_obj.weekday()]

def format_schedule(date_obj, pairs):
    """Форматирует расписание для отправки с адресами корпусов"""
    if not pairs:
        return f"📅 {date_obj.day} {date_obj.strftime('%B')}\n\n✅ Пар нет. Выходной день!"
    
    day_name = get_day_name(date_obj)
    months_ru = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
                 5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
                 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'}
    month_name = months_ru[date_obj.month]
    
    text = f"📚 РАСПИСАНИЕ\n"
    text += f"📅 {date_obj.day} {month_name} {date_obj.year} ({day_name})\n"
    text += "═" * 30 + "\n\n"
    
    buildings = set()
    
    for pair_data in pairs:
        if len(pair_data) == 4:
            pair_num, discipline, room, building = pair_data
        else:
            pair_num, discipline, room = pair_data[:3]
            building = None
        
        if not discipline:
            text += f"⚪ {pair_num}: ❌ НЕТ ПАРЫ\n\n"
            continue
        
        time_str = f" [{get_pair_time(pair_num)}]" if get_pair_time(pair_num) else ""
        text += f"🔵 {pair_num}{time_str}: {discipline}\n"
        if room:
            text += f"   🪑 Ауд. {room}\n"
        if building:
            text += f"   📍 {building}\n"
            buildings.add(building)
        text += "\n"
    
    text += f"🍽️ **Обеденный перерыв: 11:40 - 12:20**\n\n"
    
    if buildings:
        text += "─" * 30 + "\n\n"
        text += "📍 АДРЕСА КОРПУСОВ:\n"
        for b in buildings:
            if "Первый" in b:
                text += "🏛️ Тутаевское ш., 58\n"
            elif "Второй" in b:
                text += "🏛️ ул. Е. Колесовой, 70\n"
    
    text += "\n" + "═" * 30
    return text