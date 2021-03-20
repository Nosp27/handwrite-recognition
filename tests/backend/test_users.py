import os
from aiohttp.test_utils import unused_port
from unittest.mock import patch, Mock

import aiohttp
import pytest

from backend import psql_connector
from backend.app import create_app


@pytest.fixture(scope="session")
def psql_port():
    return unused_port()


@pytest.fixture(scope="session")
def psql_creds(psql_port):
    return dict(
        user="test_user",
        database="postgres",
        password="test_pass",
        host="localhost",
        port=psql_port
    )


@pytest.fixture(scope="session")
def create_psql_container(psql_port, psql_creds):
    port = psql_port
    assert os.system(
        f"docker run --rm -d --name=test_psql  -p {port}:5432 "
        f"-e POSTGRES_PASSWORD={psql_creds['password']} -e POSTGRES_USER={psql_creds['user']} postgres"
    ) == 0, "Could not create postgres container"
    yield
    assert os.system("docker stop test_psql") == 0, "Could not stop container"


@pytest.mark.parametrize(
    "login, abt, status",
    [
        (None, "shorthash", 400),
        ("some_user", None, 400),
        ("test_user", "0" * 64, 200),
        ("asd", "0" * 64, 401),
    ]
)
async def test_login(aiohttp_client, login, abt, status):
    app = create_app(None)
    client = await aiohttp_client(app)

    def _check_creds(login, token):
        return login == "test_user" and token == "0" * 64

    with patch.dict(app, {"PSQL_CONNECTOR": Mock()}):
        app["PSQL_CONNECTOR"].users.check_credentials.side_effect = _check_creds
        resp = await client.post(
            "/api/login/", json={"username": login} if login else {},
            headers={aiohttp.hdrs.AUTHORIZATION: f"Basic {abt}"} if abt else {}
        )
        assert resp.status == status


@pytest.mark.parametrize(
    "login, abt, status",
    [
        (None, "shorthash", 400),
        ("some_user", None, 400),
        ("test_user", "0" * 64, 409),
        ("asd", "F" * 64, 200),
    ]
)
async def test_sign_up_validation(aiohttp_client, login, abt, status):
    app = create_app(None)
    client = await aiohttp_client(app)

    def _check_creds(login, token):
        return login == "test_user" and token == "0" * 64

    def _check_username_exists(login):
        return login == "test_user"

    with patch.dict(app, {"PSQL_CONNECTOR": Mock()}):
        app["PSQL_CONNECTOR"].users.check_credentials.side_effect = _check_creds
        app["PSQL_CONNECTOR"].users.check_username_exists.side_effect = _check_username_exists
        resp = await client.post(
            "/api/sign_up/", json={"username": login} if login else {},
            headers={aiohttp.hdrs.AUTHORIZATION: f"Basic {abt}"} if abt else {}
        )
        assert resp.status == status


async def test_with_db(aiohttp_client, create_psql_container, psql_port, psql_creds):
    with patch.object(psql_connector.Connector, "credentials", psql_creds):
        app = create_app(None)
        client = await aiohttp_client(app)

        headers = {aiohttp.hdrs.AUTHORIZATION: f"Basic {'0' * 64}"}
        resp = await client.post("/api/login/", json={"username": "test_user"}, headers=headers)
        assert resp.status == 401

        resp = await client.post("/api/sign_up/", json={"username": "test_user"}, headers=headers)
        assert resp.status == 200

        resp = await client.post("/api/login/", json={"username": "test_user"}, headers=headers)
        assert resp.status == 200

        resp = await client.post("/api/sign_up/", json={"username": "test_user"}, headers=headers)
        assert resp.status == 409
