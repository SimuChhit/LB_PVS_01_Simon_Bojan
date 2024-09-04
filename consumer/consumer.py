import os
import pika
import pymongo
import json
import time

# MongoDB-Einstellungen
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
mongodb_database = os.getenv('MONGODB_DATABASE', 'stockmarket')  # Name der Datenbank ist 'stockmarket'
mongodb_collection = os.getenv('MONGODB_COLLECTION', 'stocks')  # Collection heißt 'stocks'

client = pymongo.MongoClient(mongodb_uri)
db = client[mongodb_database]
collection = db[mongodb_collection]

# RabbitMQ-Einstellungen
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE', 'MSFT')

# Verbindung zu RabbitMQ herstellen
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

channel.queue_declare(queue=rabbitmq_queue)

batch_size = 1000
buffer = []

def process_batch(buffer):
    prices = [json.loads(message)['price'] for message in buffer]
    average_price = sum(prices) / len(prices)
    result = {
        "company": rabbitmq_queue,
        "avgPrice": average_price,  # Feldname gemäß Schema 'avgPrice'
    }
    collection.insert_one(result)
    print(f"Processed {len(prices)} messages from {rabbitmq_queue}, average price: {average_price}")

def callback(ch, method, properties, body):
    global buffer
    buffer.append(body.decode('utf-8'))

    if len(buffer) >= batch_size:
        process_batch(buffer)
        buffer = []

channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()