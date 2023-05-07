# coding: utf-8
import pywss

from pydantic import BaseModel
from db.model import AsyncTask
from utils.http import Response
from service import db as dbService

__route__ = "/{tid}"


class HttpPostRequest(BaseModel):
    name: str
    description: str
    task_all_number: int = 100
    task_success_number: int


class View:

    @pywss.openapi.docs("任务详情")
    def http_get(self, ctx: pywss.Context):
        tid: int = int(ctx.route_params["tid"])
        task: AsyncTask = dbService.get_model_by_id(AsyncTask, tid)
        resp = Response()
        resp.data = {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "task_all_number": task.task_all_number,
            "task_success_number": task.task_success_number,
            "created_by": task.created_by,
            "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        ctx.write(resp)

    @pywss.openapi.docs("更新任务")
    def http_post(self, ctx: pywss.Context):
        req = HttpPostRequest(**ctx.json())
        tid: int = int(ctx.route_params["tid"])
        dbService.update_model_by_id(AsyncTask, tid, **req.dict())
        ctx.write(Response())

    @pywss.openapi.docs("删除任务")
    def http_delete(self, ctx: pywss.Context):
        tid: int = int(ctx.route_params["tid"])
        dbService.delete_model_by_id(AsyncTask, tid)
        ctx.write(Response())
