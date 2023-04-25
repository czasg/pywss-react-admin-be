# coding: utf-8
import pywss

from pydantic import BaseModel

from utils.http import Response, ParamsErrResponse
from service import role as roleService

__route__ = "/{rid}/permission"


class HttpPostRequest(BaseModel):
    permission: list


class View:

    @pywss.openapi.docs(summary="更新角色信息")
    def http_post(self, ctx: pywss.Context):
        try:
            req = HttpPostRequest(**ctx.json())
        except:
            ctx.write(ParamsErrResponse)
            return
        rid: int = int(ctx.route_params["rid"])
        roleService.update_role_by_id(rid, permission=",".join(req.permission))
        ctx.write(Response())
