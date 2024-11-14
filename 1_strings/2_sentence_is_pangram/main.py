"""
Панграмма - предложение, которое использует каждую букву алфавита (в нашем случае - английского алфавита).
Необходимо реализовать код, который скажет, является предложение панграммой или нет.
Буквы в верхнем и нижнем регистрах считаются эквивалентными.
Предложения содержат только буквы английского алфавита, без пробелов и т.п.
Проверка:
pytest ./1_strings/2_sentence_is_pangram/test.py
"""


def is_sentence_is_pangram(sentence: str) -> bool:
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    sentence_test = set(sentence.lower())
    return alphabet.issubset(sentence_test)
