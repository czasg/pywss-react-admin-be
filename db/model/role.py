# coding: utf-8
from sqlalchemy import *

from . import base


class UserRole(base):
    __tablename__ = 'user_roles'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(Text(), unique=True, nullable=False)
    alias = Column(Text(), nullable=False)
    permission = Column(Text(), nullable=False, default="")
    created_by = Column(Text(), nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now())


class UserRoleMid(base):
    __tablename__ = 'user_role_mid'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    uid = Column(Integer(), nullable=False)
    rid = Column(Integer(), nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
