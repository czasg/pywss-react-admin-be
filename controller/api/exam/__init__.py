# coding: utf-8
import pywss

from collections import defaultdict
from typing import List
from pydantic import BaseModel

from db import Session
from db.model import Exam
from utils.http import Response
from service import db as dbService


class Service:

    def get_all_exams(self) -> List:
        exams = defaultdict(list)
        with Session() as session:
            for exam in session.query(Exam).all():
                exams[exam.exam_type].append({
                    "id": exam.id,
                    "name": exam.name,
                    "description": exam.description,
                    "created_by": exam.created_by,
                    "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": exam.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                })
        return [
            {
                "name": "单选题集",
                "exam": exams.get("single_choice", [])
            },
            {
                "name": "多选题集",
                "exam": exams.get("multiple_choice", [])
            },
            {
                "name": "编程题集",
                "exam": exams.get("program", [])
            },
        ]


class HttpPostRequest(BaseModel):
    name: str
    description: str
    exam_type: str
    language_type: str


class View(Service):

    @pywss.openapi.docs("考试列表")
    def http_get(self, ctx: pywss.Context):
        resp = Response()
        resp.data = self.get_all_exams()
        ctx.write(resp)

    @pywss.openapi.docs("新增考试类型")
    def http_post(self, ctx: pywss.Context):
        req = HttpPostRequest(**ctx.json())
        exam = Exam(
            name=req.name,
            description=req.description,
            exam_type=req.exam_type,
            language_type=req.language_type,
            created_by=ctx.data.jwt_payload["username"],
        )
        dbService.add_model(exam)
        ctx.write(Response())
