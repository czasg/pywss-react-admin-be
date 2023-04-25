# coding: utf-8
import pywss

from utils.http import Response
from service import role as roleService
from service import user as userService

__route__ = "/{uid}"


def auth_verify(ctx: pywss.Context):
    uid: int = int(ctx.route_params["uid"])
    jwt_payload: dict = ctx.data.jwt_payload
    if not jwt_payload:
        ctx.set_status_code(pywss.StatusForbidden)
        return
    if "admin" not in jwt_payload["roles"] and uid != jwt_payload["uid"]:
        ctx.set_status_code(pywss.StatusForbidden)
        return
    ctx.next()


class View:
    use = [auth_verify]

    @pywss.openapi.docs(summary="获取用户信息")
    def http_get(self, ctx: pywss.Context):
        resp = Response()
        uid: int = int(ctx.route_params["uid"])
        user = userService.get_user_by_id(uid)
        resp.data = {
            "id": user.id,
            "alias": user.alias,
            "username": user.username,
            "roles": [
                {
                    'name': role.name,
                    'alias': role.alias,
                }
                for role in roleService.get_user_roles(user.id)
            ],
            "created_by": user.created_by,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        ctx.write(resp)
