import os
import pika
import pymongo
import json

# MongoDB-Einstellungen
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
mongodb_database = os.getenv('MONGODB_DATABASE', 'stockmarket')
mongodb_collection = os.getenv('MONGODB_COLLECTION', 'stock')

# Verbindung zu MongoDB herstellen
client = pymongo.MongoClient(mongodb_uri)
db = client[mongodb_database]
collection = db[mongodb_collection]

# RabbitMQ-Einstellungen
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE', 'TSLA')
rabbitmq_user = os.getenv('RABBITMQ_USER', 'user')
rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'user')

# Verbindung zu RabbitMQ herstellen
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
channel = connection.channel()

# Warteschlange deklarieren
channel.queue_declare(queue=rabbitmq_queue)

# Batch-Größe und Puffer initialisieren
batch_size = 1000
buffer = []

# Funktion zur Verarbeitung eines Batches von Nachrichten
def process_batch(buffer):
    prices = [json.loads(message)['price'] for message in buffer]
    average_price = sum(prices) / len(prices)
    result = {
        "company": rabbitmq_queue,
        "avgPrice": average_price,
    }
    collection.update_one(
        {'company': rabbitmq_queue},
        {'$set': result},
        upsert=True
    )
    print(f"Processed {len(prices)} messages from {rabbitmq_queue}, average price: {average_price}")

# Callback-Funktion für den Nachrichtenkonsum
def callback(ch, method, properties, body):
    global buffer
    buffer.append(body.decode('utf-8'))  # Nachricht zum Puffer hinzufügen

    if len(buffer) >= batch_size:  # Wenn die Batch-Größe erreicht ist
        process_batch(buffer)  # Batch verarbeiten
        buffer.clear()  # Puffer leeren

    ch.basic_ack(delivery_tag=method.delivery_tag)  # Bestätigen, dass die Nachricht verarbeitet wurde

# Nachrichtenkonsum starten
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=False)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()  # Konsumieren starten
