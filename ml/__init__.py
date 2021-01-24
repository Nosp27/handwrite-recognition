import logging

QUEUE_NAME = "image_queue"
MQ_ENDPOINT = "queue"
ML_HOST = "ml"

logging.basicConfig(filename="/logs/ml.log", level=logging.DEBUG)