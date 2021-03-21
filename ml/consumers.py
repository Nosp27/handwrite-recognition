import time
import socket
import pika
import pika.exceptions
from . import MQ_ENDPOINT, QUEUE_NAME
import pickle
from . import models
import requests
import logging
import random


logger = logging.getLogger("consumer")
random_number = random.randint(0, 1000)


class Consumer:
    def __init__(self, model_classname, config):
        model_base_cls = models.BaseModel
        try:
            model_cls, *_ = [cls for cls in model_base_cls.__subclasses__() if cls.__name__ == model_classname]
        except ValueError as exc:
            raise ValueError(f"Cannot find model class '{model_classname}'") from exc
        if model_cls == models.BaseModel:
            raise ValueError("Cannot work with abstract BaseModel class")
        config = config or {}
        self.model = model_cls(**config)

    def parse_message(self, message):
        print("Got image")
        return pickle.loads(message)

    def consumer_got_image(self, message_data):
        image = message_data["image"]
        request_id = message_data["request_id"]
        lang = message_data["lang"]
        self.notify_backend(request_id=request_id, status="processing")
        predicted_text = self.model.predict(image, lang)
        logger.debug(f"Sending status update for {request_id}...")
        self.notify_backend(request_id=request_id, status="done", result=predicted_text)
        logger.debug(f"Status updated for {request_id}")

    def connect_to_mq(self, *, max_retries, delay):
        retry_num = 0
        while True:
            retry_num += 1
            try:
                if max_retries == 0 or retry_num > max_retries:
                    break
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_ENDPOINT))
                print("Connected to message queue")
                return connection
            except (pika.exceptions.AMQPConnectionError, socket.gaierror):
                print(f"Failed to connect to message queue. (Round {retry_num})")
                time.sleep(delay)
        raise Exception(f"Couldn't connect to message queue after {max_retries} retry(ies).")

    def listen_queue(self):
        connection = self.connect_to_mq(max_retries=5, delay=10)
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, auto_delete=True)
        try:
            logger.debug("Listening queue")
            for method_frame, properties, body in channel.consume(QUEUE_NAME):
                message_data = {}
                try:
                    message_data = self.parse_message(body)
                    self.consumer_got_image(message_data)
                    channel.basic_ack(method_frame.delivery_tag)
                    logger.debug("Processed message from queue")
                except Exception as exc:
                    logger.exception("Could not process queue message", exc_info=(type(exc), exc, None))
                    self.notify_backend(
                        request_id=message_data.get("request_id", "unknown"),
                        status=f"ML error: {type(exc)} {str(exc)}",
                    )
        finally:
            logger.warning("Closing connection to queue. exit.")
            connection.close()

    def notify_backend(self, request_id, status, **kwargs):
        with open("/tmp/x.log", "a") as f:
            f.write(f"{time.time()} executor #{random_number}\n")
        response = requests.post(
            "http://backend:8080/api/status/", json={"request_id": request_id, "status": status, **kwargs}
        )
        response.raise_for_status()
        assert response.json()["status"] == "captured"
