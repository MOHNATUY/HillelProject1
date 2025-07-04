import sentry_sdk
from applications.auth.router import router_auth
from applications.products.router import cart_router, products_router
from applications.purchases.pay import pay_router
from applications.purchases.router import purchases_router
from applications.users.router import router_users
from fastapi import FastAPI
from settings import settings

sentry_sdk.init(
    dsn=settings.SENTRY,
    send_default_pii=True,
)


def get_application() -> FastAPI:
    app = FastAPI(root_path="/api", root_path_in_servers=True, debug=settings.DEBUG)
    app.include_router(router_users, prefix="/users", tags=["Users"])
    app.include_router(router_auth, prefix="/auth", tags=["Auth"])
    app.include_router(products_router, prefix="/products", tags=["Products"])
    app.include_router(cart_router, prefix="/carts", tags=["Cart"])
    app.include_router(purchases_router, prefix="/purchases", tags=["Purchase"])
    app.include_router(pay_router, prefix="/pay", tags=["Pay"])

    return app
