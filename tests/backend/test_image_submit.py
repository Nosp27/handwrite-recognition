from asyncio import Future
from unittest.mock import MagicMock

import pytest

from backend.app import create_app
from backend.producer import Producer


class DummyProducer(Producer):
    def __init__(self):
        super().__init__()
        self.fut = Future()

    async def send_image_to_mq(self, *args):
        return (await self.fut)(*args)


@pytest.fixture(scope="function")
def producer():
    return DummyProducer()


async def test_image_submit(aiohttp_client, producer):
    mock_send_image_to_mq = MagicMock()
    producer.fut.set_result(mock_send_image_to_mq)

    client = await aiohttp_client(create_app(producer))
    response = await client.post("/api/image_submit/", json={"image": "001010101010", "lang": "eng"})
    response.raise_for_status()
    json_data = await response.json()

    assert mock_send_image_to_mq.called
    args, kwargs = mock_send_image_to_mq.call_args
    assert args[0] == "001010101010"
    assert args[1] == json_data["request_id"]
    assert args[2] == "eng"


@pytest.mark.parametrize(
    "query_request_id, status_update_payload, status_check_result",
    [
        (
            "some_req_id",
            {"request_id": "some_req_id", "result": "some text"},
            {"status": "done", "result": "some text"}
        ),
        (
                "some_req_id",
                {"request_id": "another_req_id", "result": "some text"},
                {"status": "Not Found"}
        ),
        (
                "some_req_id",
                {"request_id": "some_req_id", "status": "custom"},
                {"status": "custom"}
        ),
    ]
)
async def test_update_status(aiohttp_client, producer, query_request_id, status_update_payload, status_check_result):
    client = await aiohttp_client(create_app(producer))
    response = await client.post("/api/status/", json=status_update_payload)
    response.raise_for_status()
    json_data = await response.json()
    assert json_data["status"] == "captured"

    response = await client.get("/api/status/", params={"request_id": query_request_id})
    json_data = await response.json()
    assert json_data == status_check_result
