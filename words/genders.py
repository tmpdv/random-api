from random import random

from db.crud import count_genders, get_gender_by_id


def calculate_gender(db):
    line_num = round(count_genders(db) * random())
    return get_gender_by_id(line_num, db)
