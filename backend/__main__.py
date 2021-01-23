from backend import handlers

import click as click
import aiohttp.web


@click.group()
def main():
    pass


@main.command()
def start():
    app = aiohttp.web.Application()
    app.add_routes(
        [
            aiohttp.web.post("/image_submit", handlers.handle_image_submit),
            aiohttp.web.get("/status", handlers.status),
            aiohttp.web.post("/status", handlers.update_status),
        ]
    )

    print("Start")
    aiohttp.web.run_app(app, port=8080)
    print("Done")


if __name__ == '__main__':
    main()
