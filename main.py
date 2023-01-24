from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse

from coin.coin import toss
from db.database import SessionLocal
from numgen.numgen import Generator
from words import words, genders
from auth import auth, dto

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return auth.get_current_active_user(token, db)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/test/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.post("/login", response_model=dto.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await auth.authenticate(form_data.username, form_data.password, db)


@app.get("/user/me")
async def get_user_me(current_user=Depends(get_current_user)):
    return current_user


@app.post("/user/create")
async def registration(request: Request, db: Session = Depends(get_db)):
    return await auth.create_user(request, db)


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


@app.post("/gender")
async def gender(db: Session = Depends(get_db)):
    return genders.calculate_gender(db)
