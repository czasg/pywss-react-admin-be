# coding: utf-8
# coding: utf-8
import pywss

from pydantic import BaseModel
from sqlalchemy import func
from db import Session
from db.model import ExamRecord
from utils.http import Response


class HttpGetRequest(BaseModel):
    pageSize: int = 10
    pageNum: int = 0
    name: str = ""

    def bind_query(self, query, ignore_page=False):
        queries = [
            (bool(self.name), ExamRecord.created_by.contains(self.name)),
        ]
        for enable, query_filter in queries:
            if enable:
                query = query.filter(query_filter)
        if not ignore_page:
            query = query.limit(self.pageSize).offset(self.pageNum * self.pageSize)
        return query


class Service:

    def record_count(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(func.count(ExamRecord.id))
            query = request.bind_query(query, ignore_page=True)
            return query.scalar()

    def get_records(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(ExamRecord). \
                order_by(ExamRecord.id.desc())
            query = request.bind_query(query)
            return query.all()


class View(Service):

    @pywss.openapi.docs("考试记录列表")
    def http_get(self, ctx: pywss.Context):
        req = HttpGetRequest(**ctx.url_params)
        resp = Response()
        resp.data = {
            "total": self.record_count(req),
            "data": [
                {
                    "id": data.id,
                    "done": data.done,
                    "score": data.score,
                    "created_by": data.created_by,
                    "created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": data.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for data in self.get_records(req)
            ],
        }
        ctx.write(resp)
