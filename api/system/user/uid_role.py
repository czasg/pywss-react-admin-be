# coding: utf-8
import pywss

from sqlalchemy import delete
from pydantic import BaseModel

from db import Session
from db.model import UserRole, UserRoleMid
from utils.http import Response, ParamsErrResponse, UnknownErrResponse
from utils.exception import StrException

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
            with Session() as session:
                mid = []
                for roleName in req.roles:
                    existRole = session.query(UserRole.id).where(UserRole.name == roleName).one()
                    if not existRole:
                        raise StrException(f"存在未知角色[{roleName}]")
                    mid.append(UserRoleMid(uid=uid, rid=existRole.id))
                delete_stmt = delete(UserRoleMid).where(UserRoleMid.uid == uid)
                session.execute(delete_stmt)
                session.bulk_save_objects(mid)
                session.commit()
        except StrException as e:
            resp.code = 99999
            resp.message = f"{e}"
        except:
            resp = UnknownErrResponse
            ctx.log.traceback()
        ctx.write(resp)
