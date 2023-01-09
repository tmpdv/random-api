import random

from fastapi import HTTPException

__CHAR_TYPES__ = {
    'whitespaces': ' \t\n\r\v\f',
    'lowercase_letters': 'abcdefghijklmnopqrstuvwxyz',
    'uppercase_letters': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'digits': '0123456789',
    'parenthesis': r"""()<>[]_{}"""
}


def generate_charset(n: int, char_types: list = None):
    if char_types is None or not isinstance(char_types, list) or len(char_types) == 0:
        char_types = ['lowercase_letters', 'uppercase_letters', 'digits']
    chars = ''
    for c in char_types:
        current = __CHAR_TYPES__.get(c)
        chars += current
        if current is None:
            raise HTTPException(status_code=400, detail="Invalid char type: " + c)
    res = []
    for i in range(n):
        res.append(random.choice(chars))
    return res


def generate_string(n: int, char_types: list = None):
    res = ''
    for c in generate_charset(n, char_types):
        res += c
    return res

