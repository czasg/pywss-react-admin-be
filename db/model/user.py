# coding: utf-8
from sqlalchemy import *

from . import base


class User(base):
    __tablename__ = 'users'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    alias = Column(Text(), nullable=False)
    username = Column(Text(), unique=True, nullable=False)
    password = Column(Text(), nullable=False)
    enable = Column(Boolean(), nullable=False, default=True)
    created_by = Column(Text())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now())
