# coding: utf-8
import pywss

from pydantic import BaseModel
from sqlalchemy import func
from db import Session
from db.model import Exam, ExamQuestion
from utils.http import Response
from service import db as dbService
from typing import List

__route__ = "/{eid}"


class Service:

    def get_rand_question(self, eid) -> List[ExamQuestion]:
        with Session() as session:
            query = session.query(ExamQuestion). \
                where(ExamQuestion.exam_id == eid). \
                order_by(func.rand()). \
                limit(10)
            return query.all()


class View(Service):

    @pywss.openapi.docs("试题列表")
    def http_get(self, ctx: pywss.Context):
        eid: int = int(ctx.route_params["eid"])
        resp = Response()
        resp.data = [
            {
                "id": question.id,
                "type": question.alias,
                "question": question.username,
                "created_by": question.created_by,
                "created_at": question.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": question.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for question in self.get_rand_question(eid)
        ]
        ctx.write(resp)

    @pywss.openapi.docs("创建考试")
    def http_post(self, ctx: pywss.Context):
        pass
