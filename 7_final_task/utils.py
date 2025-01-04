import sqlite3

import requests
import typer
from pydantic import ValidationError

from config import API_KEY, DB_NAME
from models import OpenWeatherAPIResponse, WeatherData, Coordinates


def init_db_if_not_exist() -> None:
    """
    Создаёт таблицу для сохранения истории, если её ещё нет.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_type TEXT,
                current_time TEXT,
                city_name TEXT,
                description TEXT,
                temperature_c REAL,
                feels_like_c REAL,
                wind_speed REAL
            )
        """
        )
        conn.commit()


def load_history(limit: int) -> list[WeatherData]:
    """
    Возвращает ранее сохранённую историю запросов из БД (SQLite)
    в виде списка pydantic-моделей WeatherData.
    Невалидные записи пропускаются и выводится информация о них.
    """
    init_db_if_not_exist()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_history ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()

    validated_entries = []
    for row in rows:
        record_dict = {
            "request_type": row[1],
            "current_time": row[2],
            "city_name": row[3],
            "description": row[4],
            "temperature_c": row[5],
            "feels_like_c": row[6],
            "wind_speed": row[7],
        }
        try:
            entry = WeatherData.model_validate(record_dict)
            validated_entries.append(entry)
        except ValidationError as e:
            typer.secho(
                f"Невалидная запись пропущена: {record_dict}\nПричина: {e}",
                fg=typer.colors.RED,
            )

    return validated_entries


def add_and_save_to_history(weather_data: WeatherData) -> None:
    """
    Сохраняет запрос погоды в БД (SQLite).
    """
    init_db_if_not_exist()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO weather_history (
                request_type,
                current_time,
                city_name,
                description,
                temperature_c,
                feels_like_c,
                wind_speed
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                weather_data.request_type,
                weather_data.current_time.isoformat(),
                weather_data.city_name,
                weather_data.description,
                weather_data.temperature_c,
                weather_data.feels_like_c,
                weather_data.wind_speed,
            ),
        )
        conn.commit()


def get_weather_by_city(city_name: str) -> WeatherData:
    """
    Отправляет запрос к OpenWeatherMap и возвращает данные о погоде
    в виде Pydantic-модели.
    """
    if not API_KEY:
        raise RuntimeError("Не задан OPENWEATHER_API_KEY. Проверьте .env файл.")

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru",
    }
    try:
        resp = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
        raw_json = resp.json()

        if resp.status_code == 404:
            if raw_json.get("message") == "city not found":
                raise RuntimeError(f"Не удалось найти город '{city_name}'.")

        if resp.status_code == 401:
            raise RuntimeError("Неверный ключ openweather api.")
        resp.raise_for_status()
        parsed_data = OpenWeatherAPIResponse.model_validate(raw_json)

        return WeatherData.from_openweather(parsed_data, request_type="По названию города")

    except (requests.RequestException, ValidationError, KeyError) as err:
        raise RuntimeError(f"Не удалось получить погоду по городу '{city_name}'. Причина: {err}")


def get_current_coordinates() -> Coordinates:
    """
    Определяет текущие координаты (широту, долготу) на основе IP.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get("https://ipapi.co/json", timeout=10, headers=headers)
        resp.raise_for_status()
        coordinates = Coordinates.model_validate(resp.json())
        return coordinates
    except (requests.RequestException, KeyError) as err:
        raise RuntimeError(f"Не удалось определить текущее местоположение. Причина: {err}")


def get_weather_by_coordinates(lat: float, lon: float) -> WeatherData:
    """
    Получить данные о погоде по географическим координатам (широта, долгота)
    через OpenWeatherMap в виде Pydantic-модели.
    """
    if not API_KEY:
        raise RuntimeError("Не задан OPENWEATHER_API_KEY. Проверьте настройки.")

    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric", "lang": "ru"}
    try:
        resp = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
        if resp.status_code == 401:
            raw_json = resp.json()
            raise RuntimeError("Неверный ключ openweather api.")
        resp.raise_for_status()
        raw_json = resp.json()

        parsed_data = OpenWeatherAPIResponse.model_validate(raw_json)
        return WeatherData.from_openweather(parsed_data, request_type="Текущая локация по IP")

    except (requests.RequestException, ValidationError, KeyError) as err:
        raise RuntimeError(f"Не удалось получить погоду по координатам ({lat}, {lon}). Причина: {err}")


def print_current_weather_info(weather_data: WeatherData) -> None:
    """
    Выводит удобочитаемую информацию о погоде с дополнительным форматированием.
    """
    typer.secho("===== Данные о текущей погоде =====", fg=typer.colors.GREEN, bold=True)
    typer.secho(f"Текущее время: {weather_data.current_time}", fg=typer.colors.CYAN)
    typer.secho(f"Название города: {weather_data.city_name}", fg=typer.colors.MAGENTA)
    typer.secho(f"Погодные условия: {weather_data.description}", fg=typer.colors.BLUE)
    typer.secho(f"Текущая температура: {weather_data.temperature_c}°C", fg=typer.colors.YELLOW)
    typer.secho(f"Ощущается как: {weather_data.feels_like_c}°C", fg=typer.colors.YELLOW)
    typer.secho(f"Скорость ветра: {weather_data.wind_speed} м/с", fg=typer.colors.RED)
    typer.secho("===========================", fg=typer.colors.GREEN, bold=True)


def print_history_weather_info(weather_history_entries: list[WeatherData]) -> None:
    """
    Выводит последние n записей из списка HistoryEntry.
    Если n <= 0, выводит предупреждение и ничего не печатает.
    При выводе каждой записи дополнительно отображается её request_type.
    """
    typer.secho("===== История запросов =====", fg=typer.colors.BLUE, bold=True)

    for weather_data in weather_history_entries:
        typer.secho(f"Тип запроса: {weather_data.request_type}", fg=typer.colors.MAGENTA)
        typer.secho(f"Время запроса: {weather_data.current_time}", fg=typer.colors.CYAN)
        typer.secho(f"Название города: {weather_data.city_name}", fg=typer.colors.MAGENTA)
        typer.secho(f"Погодные условия: {weather_data.description}", fg=typer.colors.BLUE)
        typer.secho(f"Температура: {weather_data.temperature_c}°C", fg=typer.colors.YELLOW)
        typer.secho(f"Ощущается как: {weather_data.feels_like_c}°C", fg=typer.colors.YELLOW)
        typer.secho(f"Скорость ветра: {weather_data.wind_speed} м/с", fg=typer.colors.RED)
        typer.secho("===========================", fg=typer.colors.GREEN, bold=True)