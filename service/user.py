# coding: utf-8
from db import Session
from db.model import User

from datetime import datetime


def update_user_by_id(uid: int, **kwargs):
    kwargs["updated_at"] = datetime.now()
    with Session() as session:
        session.query(User).where(User.id == uid).update(kwargs)
        session.commit()


def get_user_by_id(uid: int) -> User:
    with Session() as session:
        return session.query(User). \
            filter(User.id == uid). \
            first()
