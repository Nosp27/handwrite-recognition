import pickle

from aio_pika import Message, Channel, connect

from mqueue import QUEUE_NAME, MQ_ENDPOINT


async def send_image_to_mq(image_bytes: bytes, request_id):
    connection = await connect(MQ_ENDPOINT)
    channel: Channel = await connection.channel()
    message = Message(pickle.dumps((image_bytes, request_id)))
    await channel.default_exchange.publish(message, QUEUE_NAME)