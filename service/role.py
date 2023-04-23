# coding: utf-8
from typing import List

from db import Session
from db.model import UserRole, UserRoleMid


def get_user_roles(uid: int) -> List[UserRole]:
    with Session() as session:
        return session.query(UserRole). \
            join(UserRoleMid, UserRoleMid.rid == UserRole.id). \
            filter(UserRoleMid.uid == uid). \
            all()
