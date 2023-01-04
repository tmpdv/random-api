import random
from datetime import datetime


FILE_NAME = 'russian_singular_and_plural.txt'
ENCODING = 'utf-8'


def count_lines(file_name, chunk_size=1 << 13):
    with open(file_name) as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))


def calculate_word(rand):
    line_num = round(count_lines(FILE_NAME) * rand)
    with open(FILE_NAME, 'r', encoding=ENCODING) as file:
        for _ in range(line_num):
            next(file)
        return file.readline()


def random_word(query):
    if query is None:
        return calculate_word(random.random())
    byte_array = bytes(query, ENCODING)
    byte_sum = 0
    for b in byte_array:
        byte_sum += b
    now = datetime.now()
    time = now.hour * now.minute
    r = byte_sum * time * random.random()
    return calculate_word(r - r // 1)
