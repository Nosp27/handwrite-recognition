import pickle
from abc import ABC, abstractmethod

from aio_pika import Message, Channel, connect

from . import QUEUE_NAME, MQ_ENDPOINT


class Producer(ABC):
    @abstractmethod
    async def send_image_to_mq(self, image_bytes: bytes, request_id, lang: str):
        pass


class RabbitMQProducer(Producer):
    async def send_image_to_mq(self, image_bytes: bytes, request_id, lang: str):
        print("LOG: Sending image")
        connection = await connect(host=MQ_ENDPOINT)
        print("Connected to q")
        channel: Channel = await connection.channel()
        print("Resolved channel")
        message = Message(
            pickle.dumps({"image": image_bytes, "request_id": request_id, "lang": lang})
        )
        print("Composed message")
        await channel.default_exchange.publish(message, QUEUE_NAME)
        print("Sent.")
