import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='image_queue', auto_delete=True)

channel.basic_publish(exchange='', routing_key='image_queue', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
