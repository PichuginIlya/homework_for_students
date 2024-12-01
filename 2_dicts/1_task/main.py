import os
from decimal import Decimal

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SPLIT_SYMBOL = '\n'


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        file_article = file.read()
    return file_article


def get_employees_info() -> list[str]:
    """Внешнее апи, которое возвращает вам список строк с данными по сотрудникам."""
    return read_file(os.path.join(
        BASE_DIR, '1_task', 'input_data.txt',
    )).split(SPLIT_SYMBOL)


def get_parsed_employees_info() -> list[dict[str, int | str]]:
    """Функция парсит данные, полученные из внешнего API и приводит их к стандартизированному виду."""
    employees_info = get_employees_info()
    parsed_employees_info = []

    for line in employees_info:
        words = line.split()
        employee_data = {}
        for i in range(0, len(words), 2):
            key = words[i]
            value = words[i + 1]
            if key in ['id', 'age']:
                employee_data[key] = int(value)
            elif key == 'salary':
                employee_data[key] = Decimal(value)
            elif key in ['name', 'last_name', 'position']:
                employee_data[key] = value
        parsed_employees_info.append(employee_data)

    return parsed_employees_info
