import json
import pika
import os
import pymongo
from statistics import mean

# Verbindung zu RabbitMQ über Umgebungsvariablen herstellen
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE', 'stock_queue')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host)
)
channel = connection.channel()

# Die Warteschlange definieren, von der Nachrichten empfangen werden
channel.queue_declare(queue=rabbitmq_queue)

# Verbindung zu MongoDB ReplicaSet über Umgebungsvariablen herstellen
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://mongodb0:27017,mongodb1:27017,mongodb2:27017/?replicaSet=rs0')
mongodb_database = os.getenv('MONGODB_DATABASE', 'finance')
mongodb_collection = os.getenv('MONGODB_COLLECTION', 'averages')

client = pymongo.MongoClient(mongodb_uri)
db = client[mongodb_database]
collection = db[mongodb_collection]

batch_size = 1000
buffer = []

def process_batch(messages):
    # Extrahieren der Preise aus den Nachrichten und den Durchschnitt berechnen
    prices = [json.loads(message)['price'] for message in messages]
    average_price = mean(prices)

    # Das Ergebnis in die MongoDB speichern
    collection.insert_one({'average_price': average_price})
    print(f"Processed batch with average price: {average_price}")

def callback(ch, method, properties, body):
    global buffer
    buffer.append(body.decode('utf-8'))

    if len(buffer) >= batch_size:
        process_batch(buffer)
        buffer = []

# Nachrichten aus der Warteschlange konsumieren
channel.basic_consume(
    queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True
)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
