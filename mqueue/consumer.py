import aio_pika
import aiohttp
from aio_pika import connect, Channel
from . import MQ_ENDPOINT, QUEUE_NAME
import pickle


async def consumer_got_image(message: aio_pika.IncomingMessage):
    with message.process():
        image, request_id = pickle.loads(message)
        async with aiohttp.ClientSession() as session:
            predicted_text = await session.post("http://ml/predict", json={"image": image})
            await session.post(
                "http://backend/api/status", json={"request_id": request_id, "result": predicted_text}
            )


async def listen_queue():
    connection = await connect(MQ_ENDPOINT)
    channel: Channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME)

    await queue.consume(consumer_got_image)
