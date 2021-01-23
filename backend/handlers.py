import aiohttp
import aiohttp.web
import aiohttp.web_request
from uuid import uuid4

from .producer import send_image_to_mq

statuses = {}  # replace with KV Store


async def handle_image_submit(request: aiohttp.web_request.Request):
    data = (await request.json())["image"]
    request_id = uuid4().hex

    await send_image_to_mq(data, request_id)

    return aiohttp.web.json_response({"request_id": request_id})


async def status(request: aiohttp.web_request.Request):
    try:
        request_id = request.query["request_id"]
    except KeyError as err:
        return aiohttp.web.json_response({"error": type(err), "reason": str(err)}, status=400)
    result = statuses.get(request_id)
    if result:
        return aiohttp.web.json_response({"status": "fine", "result": result})
    return aiohttp.web.json_response({"status": "processing"}, status=204)


async def update_status(request: aiohttp.web_request.Request):
    data = await request.json()
    request_id = data.get("request_id")
    predicted_text = data.get("predicted_text")
    statuses[request_id] = predicted_text
