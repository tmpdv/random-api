from enum import Enum
from random import random


class CoinSide(Enum):
    EAGLE = 'EAGLE'
    TAILS = 'TAILS'


def toss():
    if random() > 0.5:
        return CoinSide.EAGLE.value
    else:
        return CoinSide.TAILS.value
