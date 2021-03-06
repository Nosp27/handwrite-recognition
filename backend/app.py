import aiohttp.web

from backend import handlers


def create_app(producer):
    app = aiohttp.web.Application()
    app["PRODUCER"] = producer
    app["STATUSES"] = {}  # TODO: replace with KV Store
    app.add_routes(
        [
            aiohttp.web.get("/api/", handlers.welcome_request),
            aiohttp.web.post("/api/image_submit/", handlers.handle_image_submit),
            aiohttp.web.get("/api/status/", handlers.status),
            aiohttp.web.post("/api/status/", handlers.update_status),
        ]
    )
    return app
