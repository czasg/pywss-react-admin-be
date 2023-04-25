# coding: utf-8
import pywss

from pydantic import BaseModel

from utils.http import Response, ParamsErrResponse
from service import role as roleService

__route__ = "/{uid}/role"


class HttpPostRequest(BaseModel):
    roles: list


class View:

    @pywss.openapi.docs(summary="更新用户角色信息")
    def http_post(self, ctx: pywss.Context):
        try:
            req = HttpPostRequest(**ctx.json())
        except:
            ctx.write(ParamsErrResponse)
            return
        uid: int = int(ctx.route_params["uid"])
        roleService.update_user_roles(uid, req.roles)
        ctx.write(Response())
