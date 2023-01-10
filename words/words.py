from random import random
from datetime import datetime

from db.crud import count_words, get_word_by_num


def calculate_word(rand, db):
    line_num = round(count_words(db) * rand)
    return get_word_by_num(line_num, db)


def random_word(query: str, db):
    if query is None:
        return calculate_word(random(), db)
    byte_array = bytes(query, 'utf-8')
    byte_sum = 0
    for b in byte_array:
        byte_sum += b
    now = datetime.now()
    time = now.hour * now.minute
    r = byte_sum * time * random()
    return calculate_word(r - r // 1, db)


def random_words(query, n, db):
    result = []
    for i in range(n):
        result.append(random_word(query, db))
    return result

