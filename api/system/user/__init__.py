# coding: utf-8
import re
import pywss
import hashlib

from pydantic import BaseModel
from sqlalchemy import func
from datetime import datetime

from db import Session
from db.model import User
from utils.http import Response
from service.role import get_user_roles

username_regex = re.compile("^[a-zA-Z]+$")
datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class HttpGetRequest(BaseModel):
    pageSize: int = 10
    pageNum: int = 0
    username: str = ""
    alias: str = ""
    enable: bool = None

    def bind_query(self, query, ignore_page=False):
        queries = [
            (bool(self.username), User.username.contains(self.username)),
            (bool(self.alias), User.alias.contains(self.alias)),
            (self.enable is not None, User.enable == self.enable),
        ]
        for enable, query_filter in queries:
            if enable:
                query = query.filter(query_filter)
        if not ignore_page:
            query = query.limit(self.pageSize).offset(self.pageNum)
        return query


class HttpPostRequest(BaseModel):
    alias: str
    username: str
    password: str
    created_by: str = None


class UserService:

    def get_users_count(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(func.count(User.id))
            query = request.bind_query(query, ignore_page=True)
            return query.one()

    def get_users(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(User)
            query = request.bind_query(query)
            return query.all()

    def add_user(self, user: User):
        with Session() as session:
            existUser = session.query(User).filter(User.username == user.username).first()
            if existUser:
                raise Exception(f"用户[{user.username}]已存在")
            session.add(user)
            session.commit()


class View(UserService):

    @pywss.openapi.docs(summary="用户列表", params=HttpGetRequest().dict())
    def http_get(self, ctx: pywss.Context):
        resp = Response()
        req = HttpGetRequest(**ctx.url_params)
        resp.data = {
            "total": self.get_users_count(req)[0],
            "data": [
                {
                    "id": user.id,
                    "alias": user.alias,
                    "username": user.username,
                    "enable": user.enable,
                    "roles": [{'name': role.name, 'alias': role.alias} for role in get_user_roles(user.id)],
                    "created_by": user.created_by,
                    "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for user in self.get_users(req)
            ],
        }
        ctx.write(resp)

    @pywss.openapi.docs(summary="新增用户", request={
        "alias": "default",
        "username": "",
        "password": "",
    })
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        try:
            req = HttpPostRequest(**ctx.json())
        except:
            resp.code = 99999
            resp.message = "请求参数异常"
            ctx.write(resp)
            return
        if not username_regex.match(req.username):
            resp.code = 99999
            resp.message = "无效用户名，仅支持大小写字母"
            ctx.write(resp)
            return
        sha256 = hashlib.sha256()
        sha256.update(req.password.encode())
        pwd256Digest = sha256.hexdigest()
        user = User(
            alias=req.alias,
            username=req.username,
            password=pwd256Digest,
            created_by=req.created_by or req.username,
        )
        try:
            self.add_user(user)
        except Exception as e:
            resp.code = 99999
            resp.message = f"{e}"
        ctx.write(resp)