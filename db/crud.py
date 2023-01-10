from sqlalchemy import text
from sqlalchemy.orm import Session

from .models import Word, Gender


def get_words(db: Session):
    return db.query(Word).all()


def get_word_by_num(num: int, db: Session):
    return db.query(Word).filter(Word.num == num).first().word


def create_word(db: Session, word):
    db.add(word)
    db.commit()
    db.refresh(word)
    return word


def count_words(db: Session):
    return db.query(text('count(*) FROM words')).scalar()


def count_genders(db: Session):
    return db.query(text('count(*) FROM genders')).scalar()


def get_gender_by_id(pk, db: Session):
    return db.query(Gender).filter(Gender.id == pk).first().name
