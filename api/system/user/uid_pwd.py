# coding: utf-8
import pywss
import hashlib

from pydantic import BaseModel

from utils.http import Response, ParamsErrResponse, UnknownErrResponse
from utils.exception import StrException
from service import user as userService

__route__ = "/{uid}/pwd"


class HttpPostRequest(BaseModel):
    password_old: str
    password_new: str


class View:

    def http_post(self, ctx: pywss.Context):
        resp = Response()
        uid: int = int(ctx.route_params["uid"])
        try:
            req = HttpPostRequest(**ctx.json())
        except:
            ctx.write(ParamsErrResponse)
            return
        try:
            user = userService.get_user_by_id(uid)
            sha256 = hashlib.sha256()
            sha256.update(req.password_old.encode())
            if sha256.hexdigest() != user.password:
                raise StrException("旧密码验证错误")
            sha256 = hashlib.sha256()
            sha256.update(req.password_new.encode())
            userService.update_user_by_id(uid, password=sha256.hexdigest())
        except StrException as e:
            resp.code = 99999
            resp.message = f"{e}"
        except:
            resp = UnknownErrResponse
            ctx.log.traceback()
        ctx.write(resp)
