# coding: utf-8
import pywss


def admin_middleware(ctx: pywss.Context):
    jwt_payload = ctx.data.jwt_payload
    if not jwt_payload:
        ctx.set_status_code(pywss.StatusForbidden)
        return
    if "admin" not in jwt_payload["roles"]:
        ctx.set_status_code(pywss.StatusForbidden)
        return
    ctx.next()
