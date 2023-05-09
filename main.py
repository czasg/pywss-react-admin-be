# coding: utf-8
import pywss

from middleware.recover import recoverHandler
from middleware.stat_api import statApiHandler


def main():
    app = pywss.App()
    app.use(
        pywss.NewCORSHandler(),
        pywss.NewJWTHandler(
            ignore_route=("/",),
            ignore_startswith=("/docs",),
            ignore_endswith=("user/login",),
            ignore_method_route=[
                ("POST", ["/api/system/user"]),
            ]
        ),
        statApiHandler
    )
    app.openapi()
    app.get("/", lambda ctx: ctx.redirect("/docs"))
    app.options("*", lambda ctx: ctx.set_status_code(pywss.StatusNoContent))
    app.view_modules("controller", recoverHandler, prefix=False)
    app.run()


if __name__ == '__main__':
    main()
