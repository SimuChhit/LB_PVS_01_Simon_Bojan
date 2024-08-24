import os

import pika

# Verbindungsvariablen zu RabbitMQ
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE', 'stock_queue')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host)
)

channel = connection.channel()

# Die Warteschlange definieren, von der Nachrichten empfangen werden
channel.queue_declare(queue=rabbitmq_queue)
