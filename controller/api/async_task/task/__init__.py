# coding: utf-8
import pywss

from sqlalchemy import func
from db import Session
from pydantic import BaseModel
from db.model import AsyncTask
from utils.http import Response
from service import db as dbService


class HttpGetRequest(BaseModel):
    pageSize: int = 10
    pageNum: int = 0
    name: str = ""
    description: str = ""

    def bind_query(self, query, ignore_page=False):
        queries = [
            (bool(self.name), AsyncTask.name.contains(self.name)),
            (bool(self.description), AsyncTask.description.contains(self.description)),
        ]
        for enable, query_filter in queries:
            if enable:
                query = query.filter(query_filter)
        if not ignore_page:
            query = query.limit(self.pageSize).offset(self.pageNum * self.pageSize)
        return query


class HttpPostRequest(BaseModel):
    name: str
    description: str
    task_all_number: int = 100
    task_success_number: int


class Service:

    def get_total_count(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(func.count(AsyncTask.id))
            query = request.bind_query(query, ignore_page=True)
            return query.scalar()

    def get_tasks(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(AsyncTask)
            query = request.bind_query(query)
            return query.all()


class View(Service):

    @pywss.openapi.docs("任务列表")
    def http_get(self, ctx: pywss.Context):
        req = HttpGetRequest(**ctx.url_params)
        resp = Response()
        resp.data = {
            "total": self.get_total_count(req),
            "data": [
                {
                    "id": task.id,
                    "name": task.name,
                    "description": task.description,
                    "task_all_number": task.task_all_number,
                    "task_success_number": task.task_success_number,
                    "created_by": task.created_by,
                    "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for task in self.get_tasks(req)
            ],
        }
        ctx.write(resp)

    @pywss.openapi.docs("创建任务")
    def http_post(self, ctx: pywss.Context):
        req = HttpPostRequest(**ctx.json())
        task = AsyncTask(
            name=req.name,
            description=req.description,
            task_all_number=req.task_all_number,
            task_success_number=req.task_success_number,
            created_by=ctx.data.jwt_payload["username"],
        )
        dbService.add_model(task)
        ctx.write(Response())
