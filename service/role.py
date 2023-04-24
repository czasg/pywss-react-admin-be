# coding: utf-8
from typing import List

from db import Session
from db.model import UserRole, UserRoleMid


def get_roles():
    with Session() as session:
        return session.query(UserRole). \
            order_by(UserRole.id). \
            all()


def get_user_roles(uid: int) -> List[UserRole]:
    with Session() as session:
        return session.query(UserRole). \
            join(UserRoleMid, UserRoleMid.rid == UserRole.id). \
            filter(UserRoleMid.uid == uid). \
            order_by(UserRole.id). \
            all()
