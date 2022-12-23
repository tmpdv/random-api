from random import random


def generate_num(min_val, max_val):
    num = min_val + random() * (max_val - min_val)
    return num + (0.5 if num > 0 else -0.5)


def generate_int(min_val, max_val):
    return int(generate_num(min_val, max_val))


def generate_float(min_val, max_val):
    return float(generate_num(min_val, max_val))


def contains_repeats(lst: list, num):
    for i in lst:
        if i == num:
            return True
    return False


class Generator:
    may_repeat: bool
    fractions_allowed: bool

    def __init__(self, may_repeat: bool, fractions_allowed: bool):
        self.may_repeat = may_repeat
        self.fractions_allowed = fractions_allowed

    def generate_one(self, min_val, max_val):
        if self.fractions_allowed:
            return generate_float(min_val, max_val)
        else:
            return generate_int(min_val, max_val)

    def generate_many(self, min_val, max_val, amount):
        res = []
        for i in range(amount):
            num = self.generate_one(min_val, max_val)
            while self.may_repeat is False and contains_repeats(res, num):
                num = self.generate_one(min_val, max_val)
            res.append(num)
        return res
