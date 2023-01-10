from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse

from coin.coin import toss
from db.database import SessionLocal
from numgen.numgen import Generator
from words import words, genders

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.middleware("http")
async def simple_security(request: Request, call_next):
    auth = request.headers.get('Kui')
    if auth != 'Gd83CMntb9BaY0R33x3Jr9-TbJxQtXVwPv0c3A0u':
        return PlainTextResponse('Access denied', status_code=403)
    return await call_next(request)


@app.get("/coin")
async def coin():
    return toss()


@app.get("/coin/{n}")
async def coin_many(n: int):
    result = []
    for i in range(n):
        result.append(toss())
    return result


@app.get("/number")
async def number(min_value: int, max_value: int, may_repeat: bool = True, allow_fractions: bool = False):
    gen = Generator(may_repeat=may_repeat, fractions_allowed=allow_fractions)
    return gen.generate_one(min_value, max_value)


@app.get("/numbers/{n}")
async def number_many(n: int, min_value: int, max_value: int,
                      may_repeat: bool = True, allow_fractions: bool = False):
    gen = Generator(may_repeat=may_repeat, fractions_allowed=allow_fractions)
    return gen.generate_many(min_value, max_value, n)


@app.get("/word")
async def russian_word(query: str = None, db: Session = Depends(get_db)):
    return words.random_word(query, db)


@app.get("/words/{n}")
async def russian_words(n: int, query: str = None, db: Session = Depends(get_db)):
    return words.random_words(query, n, db)


@app.get("/gender")
async def gender(db: Session = Depends(get_db)):
    return genders.calculate_gender(db)
