from enum import Enum

import typer
from pydantic import ValidationError

from utils import (
    get_current_coordinates,
    get_weather_by_city,
    get_weather_by_coordinates,
    load_history,
    print_current_weather_info,
    print_history_weather_info,
    add_and_save_to_history,
)


class MenuChoice(Enum):
    BY_CITY = "1"
    BY_CURRENT_LOCATION = "2"
    SHOW_HISTORY = "3"
    EXIT = "4"


app = typer.Typer()


@app.command()
def menu():
    """
    Интерактивное консольное меню; программа не завершится,
    пока пользователь явно не выберет выход.
    """
    while True:
        typer.secho(
            "============================\n"
            "1) Погода по названию города\n"
            "2) Погода по текущему месту (IP)\n"
            "3) Посмотреть последние n запросов\n"
            "4) Выход",
            fg=typer.colors.MAGENTA,
            bold=True,
        )
        user_choice = typer.prompt("Ваш выбор").strip()

        if user_choice == MenuChoice.BY_CITY.value:
            typer.secho("Введите название города:", fg=typer.colors.CYAN, bold=True)
            city = typer.prompt(">").strip()
            try:
                current_weather_data = get_weather_by_city(city)
                print_current_weather_info(current_weather_data)
                add_and_save_to_history(current_weather_data)
            except (RuntimeError, ValidationError) as err:
                typer.secho(str(err), fg=typer.colors.RED)

        elif user_choice == MenuChoice.BY_CURRENT_LOCATION.value:
            try:
                coordinates = get_current_coordinates()
                current_weather_data = get_weather_by_coordinates(coordinates.latitude, coordinates.longitude)
                print_current_weather_info(current_weather_data)
                add_and_save_to_history(current_weather_data)
            except (RuntimeError, ValidationError) as err:
                typer.secho(str(err), fg=typer.colors.RED)

        elif user_choice == MenuChoice.SHOW_HISTORY.value:
            typer.secho("Сколько записей истории вывести?", fg=typer.colors.CYAN, bold=True)
            try:
                n = int(typer.prompt(">").strip())
                history = load_history(n)
                print_history_weather_info(history)
            except ValueError as e:
                typer.secho(f"Ошибка при вводе числа: {e}", fg=typer.colors.RED)
                typer.secho(
                    "Пожалуйста, введите целое число. Попробуйте еще раз.",
                    fg=typer.colors.YELLOW,
                )
            except Exception as e:
                typer.secho(f"Произошла непредвиденная ошибка: {e}", fg=typer.colors.RED)

        elif user_choice == MenuChoice.EXIT.value:
            typer.secho("Выход из программы.", fg=typer.colors.GREEN, bold=True)
            break

        else:
            typer.secho("Неверный ввод. Повторите попытку.", fg=typer.colors.RED)
