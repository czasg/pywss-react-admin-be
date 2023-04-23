# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite+pysqlite:///sqlite.db", echo=True)
Session = scoped_session(sessionmaker(bind=engine))
