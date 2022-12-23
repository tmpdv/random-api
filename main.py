from fastapi import FastAPI

from coin.coin import toss
from numgen.numgen import Generator

app = FastAPI()


@app.get("/coin")
async def coin():
    return {"result": toss()}


@app.get("/coin/{n}")
async def coin_many(n: int):
    result = []
    for i in range(n):
        result.append(toss())
    return {"result": result}


@app.get("/number")
async def number(min_value: int, max_value: int, may_repeat: bool = True, allow_fractions: bool = False):
    gen = Generator(may_repeat=may_repeat, fractions_allowed=allow_fractions)
    return {"result": gen.generate_one(min_value, max_value)}


@app.get("/number/{amount}")
async def number_many(amount: int, min_value: int, max_value: int,
                      may_repeat: bool = True, allow_fractions: bool = False):
    gen = Generator(may_repeat=may_repeat, fractions_allowed=allow_fractions)
    return {"result": gen.generate_many(min_value, max_value, amount)}
