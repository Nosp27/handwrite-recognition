import aiohttp
import aiohttp.web
import aiohttp.web_request
from uuid import uuid4
import logging


logger = logging.getLogger()


async def welcome_request(request):
    return aiohttp.web.json_response({"status": "healthy"})


async def handle_image_submit(request: aiohttp.web_request.Request):
    logger.info("Serving /image_submit")
    json_data = await request.json()
    data = json_data["image"]
    lang = json_data["lang"]
    request_id = uuid4().hex

    await request.app["PRODUCER"].send_image_to_mq(data, request_id, lang)
    logger.debug(f"Sent image from {request_id} to message queue")
    request.app["STATUSES"][request_id] = {"status": "queued"}
    return aiohttp.web.json_response({"request_id": request_id})


async def status(request: aiohttp.web_request.Request):
    try:
        request_id = request.query["request_id"]
    except KeyError as err:
        return aiohttp.web.json_response(
            {"error": type(err).__name__, "reason": str(err)}, status=400
        )

    statuses = request.app["STATUSES"]

    if request_id not in statuses:
        return aiohttp.web.json_response({"status": "Not Found"}, status=404)
    current_status = statuses[request_id]
    result = current_status.get("result")
    logger.debug(f"Checked status for {request_id}. Result: {current_status['status']}")
    if result:
        return aiohttp.web.json_response(
            {"status": current_status["status"], "result": result}
        )
    return aiohttp.web.json_response({"status": current_status["status"]}, status=200)


async def update_status(request: aiohttp.web_request.Request):
    data = await request.json()
    request_id = data.get("request_id")
    if not request_id:
        return aiohttp.web.json_response({"error": "No request_id found"}, status=404)
    if "result" in data:
        new_status = "done"
        predicted_text = data.get("result")
        request.app["STATUSES"][request_id] = {
            "status": "done",
            "result": predicted_text,
        }
        logger.debug(
            f"Updating status for {request_id}. Status: {new_status}. Result: {predicted_text}"
        )
    else:
        new_status = data.get("status", "unknown")
        request.app["STATUSES"][request_id] = {"status": new_status}
        logger.debug(f"Updating status for {request_id}. Status: {new_status}")
    return aiohttp.web.json_response({"status": "captured"})
