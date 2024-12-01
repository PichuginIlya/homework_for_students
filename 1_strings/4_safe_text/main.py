import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SPLIT_SYMBOL = '.\n'


def get_article(path: str) -> str:
    with open(path, 'r') as file:
        file_article = file.read()
    return file_article


def get_correct_article() -> str:
    return get_article(os.path.join(BASE_DIR, '4_safe_text', 'articles', 'correct_article.txt'))


def get_wrong_article() -> str:
    return get_article(os.path.join(BASE_DIR, '4_safe_text', 'articles', 'wrong_article.txt'))


def recover_article() -> str:
    wrong_article = get_wrong_article()

    
    sentences = wrong_article.split(SPLIT_SYMBOL)

    recovered_sentences = []
    for sentence in sentences:
        if sentence.strip(): 
            
            sentence = sentence.rstrip('!') # Удаление строки восклицательных знаков
            sentence = sentence[::-1] # Разворот предложения
            sentence = sentence.lower().replace("woof-woof", "cat") # Замена
            sentence = sentence.capitalize() # Перевод в нижний регистр и заглавие первой буквы
            recovered_sentences.append(sentence + SPLIT_SYMBOL)

    recovered_article = ''.join(recovered_sentences)

    return recovered_article

