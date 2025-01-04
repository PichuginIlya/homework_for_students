from datetime import datetime, timezone, timedelta
from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class WeatherDescription(BaseModel):
    """Отвечает за структуру одного объекта из массива weather."""

    description: Optional[str] = Field("N/A", description="Описание погоды")


class Main(BaseModel):
    """Основные параметры: температура, ощущаемая температура и т.д."""

    temp: float = Field(0.0, description="Текущая температура (С)")
    feels_like: float = Field(0.0, description="Ощущаемая температура (С)")


class Wind(BaseModel):
    """Скорость ветра."""

    speed: float = Field(0.0, description="Скорость ветра (м/с)")


class OpenWeatherAPIResponse(BaseModel):
    """
    Отражает структуру JSON-ответа от OpenWeatherMap.
    Можно дополнять другими полями при необходимости.
    """

    dt: int = Field(..., description="Время в Unix-формате")
    timezone: int = Field(..., description="Смещение часового пояса в секундах")
    name: str | None = Field("N/A", description="Название города")
    weather: List[WeatherDescription] = Field(default_factory=list, description="Список описаний погодных условий") # noqa
    main: Main = Field(..., description="Основные параметры погоды")
    wind: Wind | None = Field(None, description="Скорость ветра (м/с)")


class WeatherData(BaseModel):
    """
    Pydantic-модель для валидации и структурирования данных о погоде,
    получаемых от API.
    """

    request_type: Literal["По названию города", "Текущая локация по IP", None] = Field(
        None, description="Тип запроса"
    )
    current_time: datetime = Field(..., description="Время в часовом поясе города")
    city_name: str = Field(..., description="Название города")
    description: str = Field(..., description="Описание погоды")
    temperature_c: float = Field(..., description="Температура (C)")
    feels_like_c: float = Field(..., description="Ощущаемая температура (C)")
    wind_speed: float = Field(..., description="Скорость ветра (м/с)")

    @classmethod
    def from_openweather(
        cls,
        raw_data: OpenWeatherAPIResponse,
        request_type: Literal["По названию города", "Текущая локация по IP"],
    ) -> "WeatherData":
        """
        Создаёт WeatherData напрямую из распарсенного OpenWeatherAPIResponse.
        """
        offset = timezone(timedelta(seconds=raw_data.timezone))
        local_time = datetime.fromtimestamp(raw_data.dt, tz=offset)

        desc = raw_data.weather[0].description if raw_data.weather else "N/A"

        wind_speed = raw_data.wind.speed if raw_data.wind else 0.0

        return cls(
            request_type=request_type,
            current_time=local_time,
            city_name=raw_data.name.strip() if raw_data.name else "N/A",
            description=desc.strip() if desc else "N/A",
            temperature_c=raw_data.main.temp,
            feels_like_c=raw_data.main.feels_like,
            wind_speed=wind_speed,
        )



class Coordinates(BaseModel):
    latitude: float = Field(..., description="Широта")
    longitude: float = Field(..., description="Долгота")
