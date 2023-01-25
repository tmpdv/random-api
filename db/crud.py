from sqlalchemy import text
from sqlalchemy.orm import Session

from .models import Word, Gender, User


def get_words(db: Session):
    return db.query(Word).all()


def get_word_by_num(num: int, db: Session):
    return db.query(Word).filter(Word.num == num).first().word


def get_gender_by_id(pk, db: Session):
    return db.query(Gender).filter(Gender.id == pk).first().name


def count_words(db: Session):
    return db.query(text('count(*) FROM words')).scalar()


def count_genders(db: Session):
    return db.query(text('count(*) FROM genders')).scalar()


def get_user_by_login(login: str, db: Session):
    return db.query(User).filter(User.login == login).first()


def save_word(db: Session, word):
    db.add(word)
    db.commit()
    db.refresh(word)
    return word


def save_user(user: User, db: Session):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_entity(entity, db: Session):
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity
