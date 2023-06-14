# coding: utf-8
import pywss
import json

from sqlalchemy import func
from db import Session
from db.model import Exam, ExamRecord, ExamQuestion
from utils.http import Response
from service import db as dbService
from typing import List

__route__ = "/{eid}"


class Service:

    def get_rand_question(self, exam: Exam) -> List[ExamQuestion]:
        with Session() as session:
            query = session.query(ExamQuestion). \
                where(ExamQuestion.exam_type == exam.exam_type). \
                where(ExamQuestion.language_type == exam.language_type). \
                order_by(func.random())
            if exam.exam_type in ["program"]:
                query = query.limit(1)
            else:
                query = query.limit(10)
            return query.all()


class View(Service):

    @pywss.openapi.docs("试题列表")
    def http_get(self, ctx: pywss.Context):
        ctx.set_status_code(pywss.StatusNotImplemented)

    @pywss.openapi.docs("创建考试")
    def http_post(self, ctx: pywss.Context):
        eid: int = int(ctx.route_params["eid"])
        exam = dbService.get_model_by_id(Exam, eid)
        resp = Response()
        questions = self.get_rand_question(exam)
        resp.data = [
            {
                "id": question.id,
                "question": json.loads(question.question),
                "exam_type": question.exam_type,
                "language_type": question.language_type,
                "created_by": question.created_by,
                "created_at": question.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": question.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for question in questions
        ]
        qid = [question.id for question in questions]
        qid.sort()
        record = ExamRecord(
            uid=ctx.data.jwt_payload["uid"],
            eid=eid,
            qid=",".join([f"{i}" for i in qid]),
            done=False,
            score="0",
            created_by=ctx.data.jwt_payload["username"],
        )
        dbService.add_model(record)
        ctx.write(resp)
