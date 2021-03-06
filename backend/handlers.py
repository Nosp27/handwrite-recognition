import aiohttp
import aiohttp.web
import aiohttp.web_request
from uuid import uuid4
import logging


logger = logging.getLogger()


async def welcome_request(request):
    return aiohttp.web.json_response({"status": "healthy"})


async def handle_image_submit(request: aiohttp.web_request.Request):
    data = (await request.json())["image"]
    request_id = uuid4().hex

    await request.app["PRODUCER"].send_image_to_mq(data, request_id)
    logger.debug(f"Sent image from {request_id} to message queue")

    return aiohttp.web.json_response({"request_id": request_id})


async def status(request: aiohttp.web_request.Request):
    try:
        request_id = request.query["request_id"]
    except KeyError as err:
        return aiohttp.web.json_response({"error": type(err).__name__, "reason": str(err)}, status=400)

    statuses = request.app["STATUSES"]

    if request_id not in statuses:
        return aiohttp.web.json_response({"status": "Not Found"}, status=404)
    result = statuses[request_id]
    logger.debug(f"Checking status for {request_id}. Result: {result}")
    if result:
        return aiohttp.web.json_response({"status": "done", "result": result})
    return aiohttp.web.json_response({"status": "processing"}, status=200)


async def update_status(request: aiohttp.web_request.Request):
    data = await request.json()
    request_id = data.get("request_id")
    predicted_text = data.get("result")
    logger.debug(f"Updating status for {request_id}. Result: {predicted_text}")
    request.app["STATUSES"][request_id] = predicted_text
    return aiohttp.web.json_response({"status": "captured"})
