import logging

QUEUE_NAME = "image_queue"
MQ_ENDPOINT = "queue:5672"
ML_HOST = "ml"


logging.basicConfig(filename="/logs/backend.log", level=logging.DEBUG)