# coding: utf-8
import pywss

from pydantic import BaseModel
from sqlalchemy import func
from db import Session
from db.model import StatApi
from utils.http import Response
from datetime import datetime, timedelta


class HttpGetRequest(BaseModel):
    start: datetime
    end: datetime

    def bind_query(self, query):
        queries = [
            (bool(self.start), StatApi.created_at > self.start),
            (bool(self.end), StatApi.created_at < self.end),
        ]
        for enable, query_filter in queries:
            if enable:
                query = query.filter(query_filter)
        return query


class Service:

    def date_range(self, request: HttpGetRequest):
        return [
            (request.start + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((request.end - request.start).days + 1)
        ]

    def request_number_stat(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(
                func.date(StatApi.created_at),
                func.count(StatApi.id),
            ).group_by(
                func.date(StatApi.created_at),
            )
            query = request.bind_query(query)
            date_map = {
                date: num
                for date, num, in query.all()
            }
            return [
                date_map.get(date, 0)
                for date in self.date_range(request)
            ]

    def api_stat(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(
                StatApi.api,
                func.count(StatApi.id),
            ).group_by(
                StatApi.api,
            )
            query = request.bind_query(query)
            return [
                {api: num}
                for api, num, in query.all()
            ]

    def code_stat(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(
                StatApi.code,
                func.count(StatApi.id),
            ).group_by(
                StatApi.code,
            )
            query = request.bind_query(query)
            return [
                {code: num}
                for code, num, in query.all()
            ]

    def user_stat(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(
                StatApi.created_by,
                func.count(StatApi.id),
            ).group_by(
                StatApi.created_by,
            )
            query = request.bind_query(query)
            return [
                {user: num}
                for user, num, in query.all()
            ]


class View(Service):

    @pywss.openapi.docs(summary="统计接口", params={
        "start": "",
        "end": "",
    })
    def http_get(self, ctx: pywss.Context):
        req = HttpGetRequest(**ctx.url_params)
        resp = Response()
        resp.data = {
            "date": self.date_range(req),
            "request_number_stat": self.request_number_stat(req),
            "api_stat": self.api_stat(req),
            "code_stat": self.code_stat(req),
            "user_stat": self.user_stat(req),
        }
        ctx.write(resp)
