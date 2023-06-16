# coding: utf-8
import pywss

from utils.http import Response


def View(app: pywss.App):
    app.view("/", MemoView)


class MemoView:

    @pywss.openapi.docs("备忘录列表")
    def http_get(self, ctx: pywss.Context):
        resp = Response()
        ctx.write(resp)

    @pywss.openapi.docs("新建备忘录")
    def http_post(self, ctx: pywss.Context):
        resp = Response()
        ctx.write(resp)
