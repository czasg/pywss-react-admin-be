# coding: utf-8
import pywss

from pydantic import BaseModel

from utils.http import Response
from service import user as userService

__route__ = "/{uid}/enable"


class HttpPostRequest(BaseModel):
    enable: bool


class View:

    def http_post(self, ctx: pywss.Context):
        req = HttpPostRequest(**ctx.json())
        uid: int = int(ctx.route_params["uid"])
        userService.update_user_by_id(uid, **req.dict())
        ctx.write(Response())
