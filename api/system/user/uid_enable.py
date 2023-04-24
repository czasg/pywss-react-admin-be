# coding: utf-8
import pywss

from pydantic import BaseModel

from utils.http import Response, ParamsErrResponse, UnknownErrResponse
from utils.exception import StrException
from service import user as userService

__route__ = "/{uid}/enable"


class HttpPostRequest(BaseModel):
    enable: bool


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
            userService.update_user_by_id(uid, **req.dict())
        except StrException as e:
            resp.code = 99999
            resp.message = f"{e}"
        except:
            resp = UnknownErrResponse
            ctx.log.traceback()
        ctx.write(resp)
