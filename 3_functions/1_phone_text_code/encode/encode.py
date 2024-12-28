def encode_text(text: str) -> str | None:
    keypad = {
        '.': '1',
        ',': '11',
        '?': '111',
        '!': '1111',
        ':': '11111',
        ';': '111111',
        'а': '2',
        'б': '22',
        'в': '222',
        'г': '2222',
        'д': '3',
        'е': '33',
        'ж': '333',
        'з': '3333',
        'и': '4',
        'й': '44',
        'к': '444',
        'л': '4444',
        'м': '5',
        'н': '55',
        'о': '555',
        'п': '5555',
        'р': '6',
        'с': '66',
        'т': '666',
        'у': '6666',
        'ф': '7',
        'х': '77',
        'ц': '777',
        'ч': '7777',
        'ш': '8',
        'щ': '88',
        'ъ': '888',
        'ы': '8888',
        'ь': '9',
        'э': '99',
        'ю': '999',
        'я': '9999',
        ' ': '0'
    }

    result = []
    for char in text:
        if char in keypad:
            result.append(keypad[char])
        else:
            return None

    return ' '.join(result)
    
