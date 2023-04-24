# coding: utf-8
import pywss

from pydantic import BaseModel

from utils.http import Response, ParamsErrResponse, UnknownErrResponse
from utils.exception import StrException
from service import role as roleService

__route__ = "/{uid}/role"


class HttpPostRequest(BaseModel):
    roles: list


class View:

    @pywss.openapi.docs(summary="更新用户角色信息")
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        uid: int = int(ctx.route_params["uid"])
        try:
            req = HttpPostRequest(**ctx.json())
        except:
            ctx.write(ParamsErrResponse)
            return
        try:
            roleService.update_user_roles(uid, req.roles)
        except StrException as e:
            resp.code = 99999
            resp.message = f"{e}"
        except:
            resp = UnknownErrResponse
            ctx.log.traceback()
        ctx.write(resp)
