from enum import Enum
from random import random

from sqlalchemy import Column, Integer, ForeignKey, ARRAY, String, DateTime, func
from sqlalchemy.orm import Session

from db.crud import save_entity
from db.database import Base
from db.models import User


class CoinSide(Enum):
    EAGLE = 'EAGLE'
    TAILS = 'TAILS'


class UserTossResult(Base):
    __tablename__ = "user_toss_results"

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    result = Column(ARRAY(String))
    saved_at = Column(DateTime(timezone=True), default=func.now())

    def __init__(self, user_id, result):
        self.user_id = user_id
        self.result = result


def toss():
    if random() > 0.5:
        return CoinSide.EAGLE.value
    else:
        return CoinSide.TAILS.value


async def toss_and_save(user: User, db: Session):
    res = toss()
    user = await user
    if not user.is_anon():
        save_entity(UserTossResult(user_id=user.id, result=[res]), db)
    return res


async def toss_and_save_many(n: int, user: User, db: Session):
    res = []
    for i in range(n):
        res.append(toss())
    user = await user
    if not user.is_anon():
        save_entity(UserTossResult(user_id=user.id, result=res), db)
    return res


async def get_coin_results(user: User, db: Session):
    user = await user
    return db.query(UserTossResult).filter(UserTossResult.user_id == user.id).all()
