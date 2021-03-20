import aiohttp
import aiohttp.web
import aiohttp.web_request
import logging

from backend import psql_connector
from backend.psql_connector import UserExistsError

logger = logging.getLogger()


async def parse_request(request):
    json_data = await request.json()
    username = json_data.get("username")
    auth_basic_token = request.headers.get(aiohttp.hdrs.AUTHORIZATION)
    if auth_basic_token is None:
        raise aiohttp.web.HTTPBadRequest()

    auth_basic_token = auth_basic_token.replace("Basic ", "")

    if not username or not auth_basic_token:
        raise aiohttp.web.HTTPBadRequest()

    return username, auth_basic_token


async def handler_login(request: aiohttp.web_request.Request):
    app = request.app

    logger.info("Serving /login")
    username, auth_basic_token = await parse_request(request)

    connector = psql_connector.get_psql_connector_from_app(app)

    if not await connector.users.check_credentials(username, auth_basic_token):
        raise aiohttp.web.HTTPUnauthorized()

    return aiohttp.web.json_response({"status": "access granted"})


async def handler_sign_up(request: aiohttp.web_request.Request):
    app = request.app

    logger.info("Serving /sign_up")

    username, auth_basic_token = await parse_request(request)

    connector = psql_connector.get_psql_connector_from_app(app)

    try:
        await connector.users.add_user(username, auth_basic_token)
    except UserExistsError as exc:
        raise aiohttp.web.HTTPConflict(reason="Username already exists")

    if len(auth_basic_token) != 64 and len(auth_basic_token):
        raise aiohttp.web.HTTPBadRequest(reason="Wrong hash format")

    return aiohttp.web.json_response({"status": "access granted"})
