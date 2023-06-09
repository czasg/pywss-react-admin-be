# coding: utf-8
import pywss
import hashlib

from pydantic import BaseModel
from sqlalchemy import func

from db import Session
from db.model import User, UserRole, UserRoleMid
from service import role as roleService
from utils.exception import StrException
from utils.http import Response
from utils import verify


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
            query = query.limit(self.pageSize).offset(self.pageNum * self.pageSize)
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
            return query.scalar()

    def get_users(self, request: HttpGetRequest):
        with Session() as session:
            query = session.query(User)
            query = request.bind_query(query)
            return query.all()

    def add_user(self, user: User):
        with Session() as session:
            existUser = session.query(User).filter(User.username == user.username).first()
            if existUser:
                raise StrException(f"用户[{user.username}]已存在")
            session.add(user)
            session.flush()
            role = session.query(UserRole.id).filter(UserRole.name == 'guest').first()
            if role:
                session.add(UserRoleMid(uid=user.id, rid=role.id))
            session.commit()


class View:

    def __init__(self, userService: UserService):
        self.userService = userService

    @pywss.openapi.docs(summary="用户列表", params=HttpGetRequest().dict())
    def http_get(self, ctx: pywss.Context):
        req = HttpGetRequest(**ctx.url_params)
        resp = Response()
        resp.data = {
            "total": self.userService.get_users_count(req),
            "data": [
                {
                    "id": user.id,
                    "alias": user.alias,
                    "username": user.username,
                    "enable": user.enable,
                    "roles": [
                        {
                            'name': role.name,
                            'alias': role.alias,
                        }
                        for role in roleService.get_user_roles(user.id)
                    ],
                    "created_by": user.created_by,
                    "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for user in self.userService.get_users(req)
            ],
        }
        ctx.write(resp)

    @pywss.openapi.docs(summary="新增用户", request={
        "alias": "default",
        "username": "",
        "password": "",
    })
    def http_post(self, ctx: pywss.Context):
        req = HttpPostRequest(**ctx.json())
        verify.letter_name(req.username)
        sha256 = hashlib.sha256()
        sha256.update(req.password.encode())
        user = User(
            alias=req.alias,
            username=req.username,
            password=sha256.hexdigest(),
            created_by=req.created_by or req.username,
        )
        self.userService.add_user(user)
        ctx.write(Response())
