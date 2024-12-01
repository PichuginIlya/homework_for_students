import re
from collections import Counter

def top_10_most_common_words(text: str) -> dict[str, int]:

    cleaned_text = re.sub(r'[^\w\s]', '', text).lower()

    words = cleaned_text.split()
    
    word_counts = Counter(word for word in words if len(word) >= 3)

    sorted_word_counts = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))

    most_common = dict(sorted_word_counts[:10])

    return most_common