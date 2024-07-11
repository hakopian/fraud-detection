from kafka import KafkaProducer
import pandas as pd
import json

def produce_data(file_path):
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    transaction_data = pd.read_csv(file_path)

    for index, row in transaction_data.iterrows():
        producer.send('transaction_topic', value=row.to_dict())
    producer.flush()

if __name__ == "__main__":
    produce_data('synthetic_transaction_data.csv')
