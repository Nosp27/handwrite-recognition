import asyncio
import logging

import asyncpg
from aiohttp import ClientError
from asyncpg import PostgresError, InvalidPasswordError, UndefinedTableError

logger = logging.Logger(__name__, level=logging.INFO)


class UserExistsError(ValueError):
    pass


class Connector:
    credentials = dict(
        user="psql",
        database="postgres",
        password="somepassword",
        host="localhost",
        port=5432
    )

    def __init__(self):
        logger.info("Create connector")
        self.connection = None
        self._users = None

    async def connect(self, max_retries=5):
        tries = 0
        logger.info(f"Connect for {max_retries} retries")
        while True:
            try:
                self.connection = await asyncpg.connect(
                    **self.credentials
                )
                logger.info("Connected to psql")
                return
            except InvalidPasswordError:
                raise
            except (PostgresError, ClientError, OSError):
                if tries == max_retries:
                    logger.exception("Totally failed connecting to psql")
                    raise

                logger.info("Retry connecting to psql")
                tries += 1
                await asyncio.sleep(5)

    @property
    def users(self):
        if not self.connection:
            raise ValueError("No database connection")

        if not self._users:
            self._users = Users(self.connection)

        return self._users


class Users:
    def __init__(self, connection):
        self.connection: asyncpg.Connection = connection

    async def check_username_exists(self, username):
        return bool(
            await self.connection.fetch(
                "select * from users where username=$1", username
            )
        )

    async def check_credentials(self, username, auth_basic_token):
        return bool(
            await self.connection.fetch(
                "select * from users where auth_basic=$1 and username=$2",
                auth_basic_token,
                username,
            )
        )

    async def add_user(self, username, auth_basic_token):
        if await self.check_username_exists(username):
            raise UserExistsError(f"Username '{username}' already exists")
        await self.connection.execute(
            "insert into users (username, auth_basic) values ($1, $2)",
            username,
            auth_basic_token,
        )


def get_psql_connector_from_app(app):
    return app["PSQL_CONNECTOR"]


async def ensure_db_init(app):
    connection = get_psql_connector_from_app(app).connection

    # Check database init
    try:
        await connection.execute("select * from users limit 0")
    except UndefinedTableError:
        logger.warning("Users table not found. Creating")
        await connection.execute(
            """
        create table users (
            _id bigserial primary key,
            username text not null,
            auth_basic text not null
        )
        """
        )
        await connection.execute("select * from users limit 0")
