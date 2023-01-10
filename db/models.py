from enum import Enum

from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Lang(Enum):
    RU = 'RU'
    EN = 'EN'


class Word(Base):
    __tablename__ = "words"

    word = Column(String, primary_key=True, unique=True, index=True)
    num = Column(Integer, index=True)
    lang = Column(String)
    is_active = Column(Boolean, default=True)

    def __init__(self, word, lang, is_active=True):
        self.word = word
        self.lang = lang
        self.is_active = is_active


class Gender(Base):
    __tablename__ = "genders"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

    def __init__(self, name, is_active=True):
        self.name = name
        self.is_active = is_active
