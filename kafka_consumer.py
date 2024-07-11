from kafka import KafkaConsumer
from pymongo import MongoClient
import json

def consume_data():
    consumer = KafkaConsumer(
        'transaction_topic',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    client = MongoClient('localhost', 27017)
    db = client['transaction_db']
    collection = db['transactions']

    for message in consumer:
        collection.insert_one(message.value)

if __name__ == "__main__":
    consume_data()
