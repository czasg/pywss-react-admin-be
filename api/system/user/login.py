# coding: utf-8
import pywss
import hashlib

from pydantic import BaseModel

from db import Session
from db.model import User, UserRole, UserRoleMid
from utils.http import Response


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
                raise Exception("用户/密码错误")
            if user.password != pwd256Digest:
                raise Exception("用户/密码错误")
            return user


class View(LoginService):

    @pywss.openapi.docs(summary="登录", request={
        "loginType": "default",
        "username": "username",
        "password": "password",
    })
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        try:
            req = HttpPostRequest(**ctx.json())
        except:
            resp.code = 99999
            resp.message = "未指定有效的请求参数"
            ctx.write(resp)
            return
        if req.loginType != "default":
            resp.code = 99999
            resp.message = f"暂不支持[{req.loginType}]登录方式"
            ctx.write(resp)
            return
        try:
            user = self.check_user(req)
        except Exception as e:
            resp.code = 99999
            resp.message = f"{e}"
            ctx.write(resp)
            return

        with Session() as session:
            roles = []
            for name, in session.query(UserRole.name). \
                    join(UserRoleMid, UserRoleMid.rid == UserRole.id). \
                    filter(UserRoleMid.uid == user.id). \
                    all():
                roles.append(name)
            jwt: pywss.JWT = ctx.data.jwt
            resp.data = {
                "token": jwt.encrypt(
                    uid=user.id,
                    username=req.username,
                    roles=roles or ["guest"],
                )
            }
            ctx.write(resp)
