import time
import json
from confluent_kafka import Producer
from mongo_connection import get_mongo_client


kafka_config = {"bootstrap.servers": "kafka:29092"}
producer = Producer(kafka_config)
collection = get_mongo_client()
cursor = collection.find().skip(0).limit(50)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()}")





            


