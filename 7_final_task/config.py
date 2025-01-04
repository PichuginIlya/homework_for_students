import os

from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env (если такой файл присутствует)
load_dotenv()

# Ключ для доступа к сервису погоды
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# Путь к файлу истории запросов
HISTORY_FILE = os.getenv("HISTORY_FILE", "data/history.json")

DB_NAME = os.getenv("DB_NAME", "weather_history.db")
