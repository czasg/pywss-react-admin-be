# coding: utf-8
from typing import List

from db import Session
from db.model import UserRole, UserRoleMid
from utils.exception import StrException


def get_user_roles(uid: int) -> List[UserRole]:
    with Session() as session:
        return session.query(UserRole). \
            join(UserRoleMid, UserRoleMid.rid == UserRole.id). \
            filter(UserRoleMid.uid == uid). \
            order_by(UserRole.id). \
            all()


def update_user_roles(uid: int, roleNames: list):
    with Session() as session:
        mid = []
        for roleName in roleNames:
            existRole = session.query(UserRole.id).where(UserRole.name == roleName).scalar()
            if not existRole:
                raise StrException(f"存在未知角色[{roleName}]")
            mid.append(UserRoleMid(uid=uid, rid=existRole.id))
        session.query(UserRoleMid).where(UserRoleMid.uid == uid).delete()
        session.bulk_save_objects(mid)
        session.commit()
