# coding: utf-8
from sqlalchemy import *

from . import base


class StatApi(base):
    __tablename__ = 'stat_api'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    api = Column(Text(), nullable=False)
    method = Column(Text(), nullable=False)
    code = Column(Integer(), nullable=False)
    created_by = Column(Text(), nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
