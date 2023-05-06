# coding: utf-8
from sqlalchemy import *

from . import base


class AsyncTask(base):
    __tablename__ = 'async_tasks'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(Text(), nullable=False)
    description = Column(Text())
    task_all_number = Column(Integer())
    task_success_number = Column(Integer())
    created_by = Column(Text(), nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now())
