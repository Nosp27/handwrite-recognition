import hashlib

import aiohttp
import pytest

from backend import psql_connector
from backend.app import create_app


test_app_creds = "test_username", hashlib.sha256("test_username:test_password".encode()).hexdigest()


@pytest.fixture(scope="function")
async def fake_user(psql_port, psql_creds, aiohttp_client):
    app = create_app(None)
    await aiohttp_client(app)
    connector = psql_connector.get_psql_connector_from_app(app)
    try:
        await connector.users.add_user(*test_app_creds)
    except psql_connector.UserExistsError:
        pass
    await app.shutdown()


@pytest.mark.parametrize(
    "login, abt, status",
    [
        (None, "shorthash", 400),
        ("some_user", None, 400),
        (*test_app_creds, 200),
        (test_app_creds[0], "0" * 64, 401),
        ("another_user", test_app_creds[1], 401),
    ]
)
async def test_login(aiohttp_client, login, abt, status, psql_port, psql_creds, fake_user):
    app = create_app(None)
    client = await aiohttp_client(app)
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
        (test_app_creds[0], "F" * 64, 409),
        ("non_existing_test_user", "F" * 64, 200),
        (*test_app_creds, 409),
    ]
)
async def test_sign_up_validation(
        aiohttp_client, login, abt, status, psql_port, psql_creds, fake_user
):
    app = create_app(None)
    client = await aiohttp_client(app)
    resp = await client.post(
        "/api/sign_up/", json={"username": login} if login else {},
        headers={aiohttp.hdrs.AUTHORIZATION: f"Basic {abt}"} if abt else {}
    )
    assert resp.status == status


async def test_with_db(aiohttp_client, psql_port, psql_creds):
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
