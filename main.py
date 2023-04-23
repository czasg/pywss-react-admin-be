# coding: utf-8
import pywss


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
        )
    )
    app.get("/", lambda ctx: ctx.redirect("/docs"))
    app.register_modules("api")
    app.openapi()
    app.run()


if __name__ == '__main__':
    main()
