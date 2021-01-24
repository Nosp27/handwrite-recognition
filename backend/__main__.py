import logging

from backend import handlers

import click as click
import aiohttp.web


@click.group()
def main():
    pass


@main.command()
def start():
    app = aiohttp.web.Application()
    app["STATUSES"] = {}  # replace with KV Store
    app.add_routes(
        [
            aiohttp.web.get("/api/", handlers.welcome_request),
            aiohttp.web.post("/api/image_submit/", handlers.handle_image_submit),
            aiohttp.web.get("/api/status/", handlers.status),
            aiohttp.web.post("/api/status/", handlers.update_status),
        ]
    )
    aiohttp.web.run_app(app, port=8080)


if __name__ == '__main__':
    main()
