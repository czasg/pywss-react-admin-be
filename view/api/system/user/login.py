# coding: utf-8
import pywss
import hashlib

from pydantic import BaseModel

from db import Session
from db.model import User
from service import role as roleService
from utils.http import Response
from utils.exception import StrException


class HttpPostRequest(BaseModel):
    loginType: str
    username: str
    password: str


class LoginService:

    def check_user(self, req: HttpPostRequest) -> User:
        sha256 = hashlib.sha256()
        sha256.update(req.password.encode())
        pwd256Digest = sha256.hexdigest()
        with Session() as session:
            user = session.query(User).filter(User.username == req.username).first()
            if not user:
                raise StrException("用户/密码错误")
            if user.password != pwd256Digest:
                raise StrException("用户/密码错误")
            if not user.enable:
                raise StrException("用户禁止登录")
            return user


class View:

    def __init__(self, loginService: LoginService):
        self.loginService = loginService

    @pywss.openapi.docs(summary="登录", request={
        "loginType": "default",
        "username": "username",
        "password": "password",
    })
    def http_post(self, ctx: pywss.Context):
        req = HttpPostRequest(**ctx.json())
        if req.loginType != "default":
            raise StrException(f"暂不支持[{req.loginType}]登录方式")
        user = self.loginService.check_user(req)
        jwt: pywss.JWT = ctx.data.jwt
        resp = Response()
        resp.data = {
            "token": jwt.encrypt(
                uid=user.id,
                username=req.username,
                roles=[role.name for role in roleService.get_user_roles(user.id)],
            )
        }
        ctx.write(resp)
