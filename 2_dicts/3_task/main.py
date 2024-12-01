import re

def format_phone(phone_number: str) -> str:
   
    cleaned_phone_number = re.sub(r'\D', '', phone_number)

    # Проверка соответствия одному из допустимых форматов
    if re.match(r'^(8|7|9)\d{10}$', cleaned_phone_number) or re.match(r'^\+7\d{10}$', cleaned_phone_number) or re.match(r'^\d{10}$', cleaned_phone_number):
        # Форматирование номера
        if cleaned_phone_number.startswith('7') or cleaned_phone_number.startswith('8'):
            cleaned_phone_number = '8' + cleaned_phone_number[1:]
        elif cleaned_phone_number.startswith('+7'):
            cleaned_phone_number = '8' + cleaned_phone_number[2:]
        elif len(cleaned_phone_number) == 10:
            cleaned_phone_number = '8' + cleaned_phone_number

        formatted_phone_number = f"8 ({cleaned_phone_number[1:4]}) {cleaned_phone_number[4:7]}-{cleaned_phone_number[7:9]}-{cleaned_phone_number[9:]}"
    else:
        # Возврат очищенного номера, если он не соответствует ни одному из допустимых форматов
        formatted_phone_number = cleaned_phone_number

    return formatted_phone_number
