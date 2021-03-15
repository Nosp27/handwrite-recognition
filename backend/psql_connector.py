import asyncpg


class Connector:
    def __init__(self):
        self.connection = None
        self._users = None

    async def connect(self):
        self.connection = await asyncpg.connect(
            user="postgres", password="somepassword",
            database="postgres", host="psql"
        )

    async def ensure_connection(self):
        if not self.connection:
            await self.connect()

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
        return bool(await self.connection.fetch("select * from users where username=%s", username))

    async def check_credentials(self, auth_basic_token):
        return bool(await self.connection.fetch("select * from users where auth_basic=%s", auth_basic_token))

    async def add_user(self, username, auth_basic_token):
        if self.check_username_exists(username):
            raise ValueError(f"Username '{username}' already exists")
        await self.connection.execute(
            "insert into users (username, auth_basic) values (%s, %s)", username, auth_basic_token
        )


def get_psql_connector_from_app(app):
    return app["PSQL_CONNECTOR"]


