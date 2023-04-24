# coding: utf-8
import re
import pywss

from pydantic import BaseModel
from typing import List

from db import Session
from db.model import UserRole
from utils.http import Response, ParamsErrResponse, UnknownErrResponse
from utils.exception import StrException

name_regex = re.compile("^[a-zA-Z]+$")


class HttpGetRequest(BaseModel):
    pageSize: int = 10
    pageNum: int = 0
    name: str = ""
    alias: str = ""

    def bind_query(self, query, ignore_page=False):
        queries = [
            (bool(self.name), UserRole.name.contains(self.name)),
            (bool(self.alias), UserRole.alias.contains(self.alias)),
        ]
        for enable, query_filter in queries:
            if enable:
                query = query.filter(query_filter)
        if not ignore_page:
            query = query.limit(self.pageSize).offset(self.pageNum)
        return query


class HttpPostRequest(BaseModel):
    name: str
    alias: str
    created_by: str


class RoleService:

    def get_roles(self, request: HttpGetRequest) -> List[UserRole]:
        with Session() as session:
            query = session.query(UserRole)
            query = request.bind_query(query)
            return query.all()

    def add_role(self, role: UserRole):
        with Session() as session:
            existRole = session.query(UserRole).filter(UserRole.name == role.name).scalar()
            if existRole:
                raise StrException(f"角色[{role.name}]已存在")
            session.add(role)
            session.commit()


class View(RoleService):

    @pywss.openapi.docs(summary="获取角色列表")
    def http_get(self, ctx: pywss.Context):
        resp = Response()
        req = HttpGetRequest(**ctx.url_params)
        try:
            resp.data = [
                {
                    "id": role.id,
                    "name": role.name,
                    "alias": role.alias,
                    "created_by": role.created_by,
                    "created_at": role.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": role.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for role in self.get_roles(req)
            ]
        except StrException as e:
            resp.code = 99999
            resp.message = f"{e}"
        except:
            resp = UnknownErrResponse
            ctx.log.traceback()
        ctx.write(resp)

    @pywss.openapi.docs(summary="创建角色")
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        try:
            req = HttpPostRequest(**ctx.json())
        except:
            ctx.write(ParamsErrResponse)
            return
        if not name_regex.match(req.name):
            resp.code = 99999
            resp.message = "无效角色名，仅支持大小写字母"
            ctx.write(resp)
            return
        role = UserRole(
            name=req.name,
            alias=req.alias,
            created_by=req.created_by,
        )
        try:
            self.add_role(role)
        except StrException as e:
            resp.code = 99999
            resp.message = f"{e}"
        except:
            resp = UnknownErrResponse
            ctx.log.traceback()
        ctx.write(resp)
