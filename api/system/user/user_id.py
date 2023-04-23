# coding: utf-8
import pywss
import hashlib

from sqlalchemy import update
from pydantic import BaseModel

from db import Session
from db.model import User
from utils.http import Response
from service import role as roleService
from service import user as userService

__route__ = "/user/{uid}"


def auth_verify(ctx: pywss.Context):
    uid: int = int(ctx.route_params["uid"])
    jwt_payload: dict = ctx.data.jwt_payload
    if not jwt_payload:
        ctx.set_status_code(pywss.StatusForbidden)
        return
    if "admin" not in jwt_payload["roles"] and uid != jwt_payload["uid"]:
        ctx.set_status_code(pywss.StatusForbidden)
        return
    ctx.next()


class HttpPostRequest(BaseModel):
    type: str  # info / password / enable
    alias: str = ""
    username: str = ""
    password_old: str = ""
    password_new: str = ""
    enable: bool = False

    def update_user(self, user: User):
        stmt = update(User).where(User.id == user.id)
        if self.type == "info":
            stmt.values(alias=self.alias, username=self.username)
        elif self.type == "pwd":
            sha256 = hashlib.sha256()
            sha256.update(self.password_old.encode())
            if sha256.hexdigest() != user.password:
                raise Exception("旧密码验证错误")
            sha256 = hashlib.sha256()
            sha256.update(self.password_new.encode())
            stmt.values(password=sha256.hexdigest())
        elif self.type == "enable":
            stmt.values(enable=self.enable)
        else:
            raise Exception(f"暂不支持[{self.type}]类型")
        if self.alias:
            stmt.values(alias=self.alias)
        if self.username:
            stmt.values(username=self.username)
        with Session() as session:
            session.execute(stmt)
            session.commit()


class UserService:

    def update_user(self, req: HttpPostRequest, user: User):
        stmt = update(User).where(User.id == user.id)
        if req.type == "info":
            stmt.values(alias=req.alias, username=req.username)
        elif req.type == "pwd":
            sha256 = hashlib.sha256()
            sha256.update(req.password_old.encode())
            if sha256.hexdigest() != user.password:
                raise Exception("旧密码验证错误")
            sha256 = hashlib.sha256()
            sha256.update(req.password_new.encode())
            stmt.values(password=sha256.hexdigest())
        elif req.type == "enable":
            stmt.values(enable=req.enable)
        else:
            raise Exception(f"暂不支持[{req.type}]类型")
        if req.alias:
            stmt.values(alias=req.alias)
        if req.username:
            stmt.values(username=req.username)
        with Session() as session:
            session.execute(stmt)
            session.commit()


class View(UserService):
    use = [auth_verify]

    @pywss.openapi.docs(summary="获取用户信息")
    def http_get(self, ctx: pywss.Context):
        resp = Response()
        uid: int = int(ctx.route_params["uid"])
        user = userService.get_user_by_id(uid)
        roles = roleService.get_user_roles(uid)
        resp.data = {
            "id": user.id,
            "alias": user.alias,
            "username": user.username,
            "roles": [role.name for role in roles] or ["guest"]
        }
        ctx.write(resp)

    @pywss.openapi.docs(summary="更新用户信息")
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        try:
            req = HttpPostRequest(**ctx.json())
        except:
            resp.code = 99999
            resp.message = "请求参数异常"
            ctx.write(resp)
            return
        uid: int = int(ctx.route_params["uid"])
        try:
            user = userService.get_user_by_id(uid)
            self.update_user(req, user)
        except Exception as e:
            resp.code = 99999
            resp.message = f"{e}"
        ctx.write(resp)
