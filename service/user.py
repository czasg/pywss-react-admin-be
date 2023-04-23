# coding: utf-8
from db import Session
from db.model import User


def get_user_by_id(uid: int) -> User:
    with Session() as session:
        return session.query(User).filter(User.id == uid).first()
