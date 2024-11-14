"""
Вам дан список предложений.
Предложение содержит только слова, которые разделены единичными пробелами.
Необходимо вернуть максимальное количество слов, которое содержится в одном предложении.
sentences[i] - это одно предложение.
Если ни одно из предложений не содержит слов, то нужно вернуть 0
Проверка:
pytest ./1_strings/3_maximum_number_of_words/test.py
"""


def get_max_number_of_words_from_sentences(sentences: list[str]) -> int:
    max_words = 0
    for sentence in sentences:
        words = sentence.split()
        max_words = max(max_words, len(words))
    return max_words

