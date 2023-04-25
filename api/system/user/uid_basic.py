# coding: utf-8
import pywss

from pydantic import BaseModel

from utils import verify
from utils.http import Response, ParamsErrResponse
from service import user as userService

__route__ = "/{uid}/basic"


class HttpPostRequest(BaseModel):
    alias: str
    username: str


class View:

    def http_post(self, ctx: pywss.Context):
        try:
            req = HttpPostRequest(**ctx.json())
            verify.letter_name(req.username)
        except:
            ctx.write(ParamsErrResponse)
            return
        uid: int = int(ctx.route_params["uid"])
        userService.update_user_by_id(uid, **req.dict())
        ctx.write(Response())
