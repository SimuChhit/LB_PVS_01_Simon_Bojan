import pika

# Verbindung zu RabbitMQ herstellen
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq')
)
channel = connection.channel()

# Die Warteschlange definieren, von der Nachrichten empfangen werden
channel.queue_declare(queue='stock_queue')

def callback(ch, method, properties, body):
    print(f"Received {body}")

# Nachrichten aus der Warteschlange konsumieren
channel.basic_consume(
    queue='stock_queue', on_message_callback=callback, auto_ack=True
)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()