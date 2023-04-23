# coding: utf-8
import pywss

from utils.http import Response


class View:

    @pywss.openapi.docs(summary="获取角色列表")
    def http_get(self, ctx: pywss.Context):
        resp = Response()
        ctx.write(resp)

    @pywss.openapi.docs(summary="创建角色")
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        ctx.write(resp)
