import click as click
from mqueue import consumer


@click.group()
def main():
    pass


@main.command()
def start():
    consumer.listen_queue()


if __name__ == '__main__':
    main()
