from backend import app

import click as click
import aiohttp.web

from backend.producer import RabbitMQProducer


@click.group()
def main():
    pass


@main.command()
def start():
    web_app = app.create_app(RabbitMQProducer())
    aiohttp.web.run_app(web_app, port=8080)


if __name__ == "__main__":
    main()
