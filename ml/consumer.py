import time

import pika
import pika.exceptions
from . import MQ_ENDPOINT, QUEUE_NAME
import pickle
from . import model
import requests
import logging

logger = logging.getLogger("consumer")


def consumer_got_image(message):
    image, request_id = pickle.loads(message)
    predicted_text = model.predict(image)
    logger.debug(f"Sending status update for {request_id}...")
    requests.post(
        "http://backend:8080/api/status/", json={"request_id": request_id, "predicted_text": predicted_text}
    )
    logger.debug(f"Status updated for {request_id}")


def connect_to_mq(max_retries=5):
    retry_num = 0
    while True:
        retry_num += 1
        try:
            if max_retries == 0 or retry_num > max_retries:
                break
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_ENDPOINT))
            print("Connected to message queue")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"Failed to connect to message queue. (Round {retry_num})")
            time.sleep(5)
    raise Exception(f"Couldn't connect to message queue after {max_retries} retry(ies).")


def listen_queue():
    connection = connect_to_mq(max_retries=5)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, auto_delete=True)
    try:
        logger.debug("Listening queue")
        for method_frame, properties, body in channel.consume(QUEUE_NAME):
            try:
                consumer_got_image(body)
                channel.basic_ack(method_frame.delivery_tag)
                logger.debug("Processed message from queue")
            except Exception as exc:
                logger.exception("Could not process queue message", exc_info=(type(exc), exc, None))
    finally:
        logger.warning("Closing connection to queue. exit.")
        connection.close()
