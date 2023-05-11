# coding: utf-8
from sqlalchemy import *

from . import base


class Exam(base):
    __tablename__ = 'exams'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(Text(), nullable=False)
    description = Column(Text())
    exam_type = Column(Text())
    language_type = Column(Text(), nullable=False)
    created_by = Column(Text(), nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now())


class ExamRecord(base):
    __tablename__ = 'exam_records'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    uid = Column(Integer(), nullable=False)
    eid = Column(Integer(), nullable=False)
    qid = Column(Text(), nullable=False)
    done = Column(Boolean(), nullable=False)
    score = Column(Text(), nullable=False)
    created_by = Column(Text(), nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now())


class ExamQuestion(base):
    __tablename__ = 'exam_questions'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    question = Column(Text(), nullable=False)
    answer = Column(Text(), nullable=False)
    exam_type = Column(Text(), nullable=False)
    language_type = Column(Text(), nullable=False)
    created_by = Column(Text(), nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now())
