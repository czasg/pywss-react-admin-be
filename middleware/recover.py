# coding: utf-8
import pywss

from utils.http import Response, UnknownErrResponse
from utils.exception import StrException


def recoverHandler(ctx: pywss.Context):
    try:
        return ctx.next()
    except StrException as e:
        resp = Response(99999, f"{e}")
    except:
        resp = UnknownErrResponse
        ctx.log.traceback()
    if not ctx.response_body:
        ctx.write(resp)
