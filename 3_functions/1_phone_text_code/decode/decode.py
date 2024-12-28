def decode_numbers(numbers: str) -> str | None:
    keypad = {
        '1': ['.', ',', '?', '!', ':', ';'],
        '2': ['а', 'б', 'в', 'г'],
        '3': ['д', 'е', 'ж', 'з'],
        '4': ['и', 'й', 'к', 'л'],
        '5': ['м', 'н', 'о', 'п'],
        '6': ['р', 'с', 'т', 'у'],
        '7': ['ф', 'х', 'ц', 'ч'],
        '8': ['ш', 'щ', 'ъ', 'ы'],
        '9': ['ь', 'э', 'ю', 'я'],
        '0': [' ']
    }

    groups = numbers.split()

    for group in groups:
        if not group.isdigit() or len(group) > 6 or len(group) == 0 or len(set(group)) != 1:
            return None

    result = []
    for group in groups:
        digit = group[0]
        count = len(group)
        if digit in keypad and count <= len(keypad[digit]):
            result.append(keypad[digit][count - 1])
        else:
            return None

    return ''.join(result)