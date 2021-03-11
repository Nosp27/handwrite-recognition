import logging

QUEUE_NAME = "image_queue"
MQ_ENDPOINT = "queue"
ML_HOST = "ml"

try:
    logging.basicConfig(filename="/logs/ml.log", level=logging.DEBUG)
except:
    logging.basicConfig(filename="/tmp/ml.log", level=logging.DEBUG)
