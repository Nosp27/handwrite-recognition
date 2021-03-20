import logging

QUEUE_NAME = "image_queue"
MQ_ENDPOINT = "queue"
ML_HOST = "ml"

try:
    logging.basicConfig(filename="/tmp/backend.log", level=logging.DEBUG)
except:
    pass
