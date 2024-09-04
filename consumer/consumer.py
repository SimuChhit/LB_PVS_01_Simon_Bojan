import os
import pika
import pymongo
import json
import time

# MongoDB-Einstellungen
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')  # MongoDB URI aus Umgebungsvariablen oder Standardwert
mongodb_database = os.getenv('MONGODB_DATABASE', 'stockmarket')  # Name der Datenbank aus Umgebungsvariablen oder Standardwert
mongodb_collection = os.getenv('MONGODB_COLLECTION', 'stocks')  # Name der Sammlung aus Umgebungsvariablen oder Standardwert

# Verbindung zu MongoDB herstellen
client = pymongo.MongoClient(mongodb_uri)
db = client[mongodb_database]
collection = db[mongodb_collection]

# RabbitMQ-Einstellungen
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')  # RabbitMQ Host aus Umgebungsvariablen oder Standardwert
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE', 'MSFT')  # RabbitMQ Warteschlange aus Umgebungsvariablen oder Standardwert
rabbitmq_user = os.getenv('RABBITMQ_USER', 'user')  # RabbitMQ Benutzername aus Umgebungsvariablen oder Standardwert
rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'user')  # RabbitMQ Passwort aus Umgebungsvariablen oder Standardwert

# Verbindung zu RabbitMQ herstellen
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)  # Anmeldeinformationen für RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))  # Verbindung zu RabbitMQ
channel = connection.channel()  # Kanal erstellen

# Warteschlange deklarieren
channel.queue_declare(queue=rabbitmq_queue)

# Batch-Größe und Puffer initialisieren
batch_size = 1000
buffer = []

# Funktion zur Verarbeitung eines Batches von Nachrichten
def process_batch(buffer):
    prices = [json.loads(message)['price'] for message in buffer]  # Preise aus den Nachrichten extrahieren
    average_price = sum(prices) / len(prices)  # Durchschnittspreis berechnen
    result = {
        "company": rabbitmq_queue,
        "avgPrice": average_price,  # Feldname gemäß Schema 'avgPrice'
    }
    collection.insert_one(result)  # Ergebnis in MongoDB einfügen
    print(f"Processed {len(prices)} messages from {rabbitmq_queue}, average price: {average_price}")

# Callback-Funktion für den Nachrichtenkonsum
def callback(ch, method, properties, body):
    global buffer
    buffer.append(body.decode('utf-8'))  # Nachricht zum Puffer hinzufügen

    if len(buffer) >= batch_size:  # Wenn die Batch-Größe erreicht ist
        process_batch(buffer)  # Batch verarbeiten
        buffer = []  # Puffer leeren

# Nachrichtenkonsum starten
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()  # Konsumieren starten