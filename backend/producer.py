import pickle
from abc import ABC, abstractmethod

from aio_pika import Message, Channel, connect

from . import QUEUE_NAME, MQ_ENDPOINT


class Producer(ABC):
    @abstractmethod
    async def send_image_to_mq(self, image_bytes: bytes, request_id):
        pass


class RabbitMQProducer(Producer):
    async def send_image_to_mq(self, image_bytes: bytes, request_id):
        connection = await connect(MQ_ENDPOINT)
        channel: Channel = await connection.channel()
        message = Message(pickle.dumps((image_bytes, request_id)))
        await channel.default_exchange.publish(message, QUEUE_NAME)
