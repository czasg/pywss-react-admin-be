# coding: utf-8
import pywss

from pydantic import BaseModel

from utils import verify
from utils.http import Response
from service import user as userService

__route__ = "/{uid}/basic"


class HttpPostRequest(BaseModel):
    alias: str
    username: str


class View:

    def http_post(self, ctx: pywss.Context):
        req = HttpPostRequest(**ctx.json())
        verify.letter_name(req.username)
        uid: int = int(ctx.route_params["uid"])
        userService.update_user_by_id(uid, **req.dict())
        ctx.write(Response())
