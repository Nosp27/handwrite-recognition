from ml import handlers

import click as click


@click.group()
def main():
    pass


@main.command()
def start():
    handlers.app.run(port=1234)


if __name__ == '__main__':
    main()
