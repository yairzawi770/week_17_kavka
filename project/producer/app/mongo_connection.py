from pymongo import MongoClient
from confluent_kafka import Producer
import os


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "suspicious")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "suspicious_customers_orders")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC_NAME = "data"

producer = {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}
producer = Producer(producer)
