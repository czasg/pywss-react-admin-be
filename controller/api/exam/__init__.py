# coding: utf-8
import pywss

from pydantic import BaseModel
from sqlalchemy import func
from db import Session
from db.model import Exam
from utils.http import Response
from service import db as dbService


class HttpGetRequest(BaseModel):
    pageSize: int = 10
    pageNum: int = 0
    name: str = ""

    def bind_query(self, query, ignore_page=False):
        queries = [
            (bool(self.name), Exam.name.contains(self.name)),
        ]
        for enable, query_filter in queries:
            if enable:
                query = query.filter(query_filter)
        if not ignore_page:
            query = query.limit(self.pageSize).offset(self.pageNum * self.pageSize)
        return query


class Service:

    def exam_count(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(func.count(Exam.id))
            query = request.bind_query(query, ignore_page=True)
            return query.scalar()

    def get_exams(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(Exam)
            query = request.bind_query(query)
            return query.all()


class HttpPostRequest(BaseModel):
    name: str
    description: str


class View(Service):

    @pywss.openapi.docs("考试类型列表")
    def http_get(self, ctx: pywss.Context):
        req = HttpGetRequest(**ctx.url_params)
        resp = Response()
        resp.data = {
            "total": self.exam_count(req),
            "data": [
                {
                    "id": exam.id,
                    "name": exam.name,
                    "description": exam.description,
                    "created_by": exam.created_by,
                    "created_at": exam.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": exam.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for exam in self.get_exams(req)
            ],
        }
        ctx.write(resp)

    @pywss.openapi.docs("新增考试类型")
    def http_post(self, ctx: pywss.Context):
        req = HttpPostRequest(**ctx.json())
        exam = Exam(
            name=req.name,
            description=req.description,
            created_by=ctx.data.jwt_payload["username"],
        )
        dbService.add_model(exam)
        ctx.write(Response())
