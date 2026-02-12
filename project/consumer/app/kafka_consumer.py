import os
import json
from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient


kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
kafka_topic = os.getenv("KAFKA_TOPIC")
mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")
mongo_collection = os.getenv("MONGO_COLLECTION")

consumer = Consumer(
    {
        "bootstrap.servers": kafka_bootstrap_servers,
        "group.id": "customer-consumer-group",
        "auto.offset.reset": "earliest",
    }
)

consumer.subscribe([kafka_topic])

mongo_client = MongoClient(mongo_uri)
db = mongo_client[mongo_db]
collection = db[mongo_collection]

print(f"Consumer started. Listening to topic: {kafka_topic}")

while True:
    msg = consumer.poll(timeout=1.0)

    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(f"Error: {msg.error()}")
            continue

    message_value = msg.value().decode("utf-8")
    customer_data = json.loads(message_value)

    required_fields = [
        "type",
        "customerNumber",
        "customerName",
        "contactLastName",
        "contactFirstName",
        "phone",
        "addressLine1",
        "addressLine2",
        "city",
        "state",
        "postalCode",
        "country",
        "salesRepEmployeeNumber",
        "creditLimit",
    ]
    if not all(field in customer_data for field in required_fields):
        print(f"Invalid message: missing required fields")
        continue

    customer_data = customer_data["phone"]
    existing_customer = collection.find_one({"phone": phone})

    if existing_customer:
        print(f"customer with phone {phone} already exists. Skipping.")
        continue

    collection.insert_one(customer_data)
    print(f"Inserted user: {customer_data['phone']}")
