import time
import socket
import pika
import pika.exceptions
from . import MQ_ENDPOINT, QUEUE_NAME
import pickle
from . import models
import requests
import logging


logger = logging.getLogger("consumer")


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

    def consumer_got_image(self, message):
        print("Got image")
        message_data = pickle.loads(message)
        image = message_data["image"]
        request_id = message_data["request_id"]
        lang = message_data["lang"]
        requests.post(
            "http://backend:8080/api/status/", json={"request_id": request_id, "status": "processing"}
        )
        predicted_text = self.model.predict(image, lang)
        logger.debug(f"Sending status update for {request_id}...")
        response = requests.post(
            "http://backend:8080/api/status/", json={"request_id": request_id, "result": predicted_text}
        )
        response.raise_for_status()
        assert response.json()["status"] == "captured"
        logger.debug(f"Status updated for {request_id}")

    def connect_to_mq(self, max_retries=5):
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
                time.sleep(5)
        raise Exception(f"Couldn't connect to message queue after {max_retries} retry(ies).")

    def listen_queue(self):
        connection = self.connect_to_mq(max_retries=5)
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, auto_delete=True)
        try:
            logger.debug("Listening queue")
            for method_frame, properties, body in channel.consume(QUEUE_NAME):
                try:
                    self.consumer_got_image(body)
                    channel.basic_ack(method_frame.delivery_tag)
                    logger.debug("Processed message from queue")
                except Exception as exc:
                    logger.exception("Could not process queue message", exc_info=(type(exc), exc, None))
        finally:
            logger.warning("Closing connection to queue. exit.")
            connection.close()
