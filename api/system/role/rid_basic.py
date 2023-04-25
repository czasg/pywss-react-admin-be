# coding: utf-8
import pywss

from pydantic import BaseModel

from utils import verify
from utils.http import Response, ParamsErrResponse
from service import role as roleService

__route__ = "/{rid}/basic"


class HttpPostRequest(BaseModel):
    alias: str
    name: str


class View:

    @pywss.openapi.docs(summary="更新角色信息")
    def http_post(self, ctx: pywss.Context):
        try:
            req = HttpPostRequest(**ctx.json())
            verify.letter_name(req.name)
        except:
            ctx.write(ParamsErrResponse)
            return
        rid: int = int(ctx.route_params["rid"])
        roleService.update_role_by_id(rid, **req.dict())
        ctx.write(Response())
