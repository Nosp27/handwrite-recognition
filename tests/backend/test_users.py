from unittest.mock import patch, Mock

import aiohttp
import pytest

from backend.app import create_app


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
