import aiohttp.web

from backend import psql_connector
from backend.handlers import image_handlers, login_handlers


def create_app(producer):
    app = aiohttp.web.Application(middlewares=[
        aiohttp.web.normalize_path_middleware()
    ])

    app["PRODUCER"] = producer
    app["STATUSES"] = {}  # TODO: replace with KV Store

    app.add_routes(
        [
            aiohttp.web.get("/api/", image_handlers.welcome_request),
            aiohttp.web.post("/api/image_submit/", image_handlers.handle_image_submit),
            aiohttp.web.get("/api/status/", image_handlers.status),
            aiohttp.web.post("/api/status/", image_handlers.update_status),
            aiohttp.web.post("/api/login/", login_handlers.handler_login),
            aiohttp.web.post("/api/sign_up/", login_handlers.handler_sign_up),
        ]
    )
    app.on_startup.append(configure)
    return app


async def configure(app):
    # Connect to DB
    app["PSQL_CONNECTOR"] = psql_connector.Connector()
    connector = psql_connector.get_psql_connector_from_app(app)
    await connector.connect()
    await psql_connector.ensure_db_init(app)
