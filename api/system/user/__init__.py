# coding: utf-8
import re
import pywss
import hashlib

from pydantic import BaseModel

from db import Session
from db.model import User
from utils.http import Response

username_regex = re.compile("^[a-zA-Z]+$")


class HttpGetRequest(BaseModel):
    pageSize: int = 10
    pageNum: int = 0
    username: str = ""
    alias: str = ""

    def bind_query(self, query):
        queries = [
            (bool(self.username), User.username.contains(self.username)),
            (bool(self.alias), User.alias.contains(self.alias)),
        ]
        for enable, query_filter in queries:
            if enable:
                query = query.filter(query_filter)
        query = query.limit(self.pageSize).offset(self.pageNum)
        return query


class HttpPostRequest(BaseModel):
    alias: str
    username: str
    password: str


class UserService:

    def get_users(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(User.id, User.alias, User.username)
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
        resp.data = [
            {
                "id": uid,
                "alias": alias,
                "username": username,
            }
            for uid, alias, username in self.get_users(req)
        ]
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
        user = User(alias=req.alias, username=req.username, password=pwd256Digest)
        try:
            self.add_user(user)
        except Exception as e:
            resp.code = 99999
            resp.message = f"{e}"
        ctx.write(resp)
