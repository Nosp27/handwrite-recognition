import os

import pytest
from aiohttp.test_utils import unused_port
from unittest.mock import patch

from backend.psql_connector import Connector


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


@pytest.fixture(scope="session", autouse=True)
def create_psql_container(psql_port, psql_creds):
    port = psql_port
    assert os.system(
        f"docker run --rm -d --name=test_psql  -p {port}:5432 "
        f"-e POSTGRES_PASSWORD={psql_creds['password']} -e POSTGRES_USER={psql_creds['user']} postgres"
    ) == 0, "Could not create postgres container"
    yield
    assert os.system("docker stop test_psql") == 0, "Could not stop container"


@pytest.fixture(scope="session", autouse=True)
def mock_connector(psql_creds):
    with patch.object(Connector, "credentials", psql_creds):
        yield