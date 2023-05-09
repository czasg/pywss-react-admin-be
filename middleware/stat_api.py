# coding: utf-8
import pywss

from db import model
from service import db as dbService


def statApiHandler(ctx: pywss.Context):
    ctx.next()
    payload = ctx.data.jwt_payload
    if not payload:
        return
    stat = model.StatApi(
        api=ctx.route,
        method=ctx.method,
        code=ctx.response_status_code,
        created_by=payload["username"],
    )
    dbService.add_model(stat)
