# coding: utf-8
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

from .async_task import AsyncTask
from .role import UserRole, UserRoleMid
from .stat import StatApi
from .user import User

from db import engine

base.metadata.create_all(engine)
