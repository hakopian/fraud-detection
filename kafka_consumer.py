from kafka import KafkaConsumer
import json
from pymongo import MongoClient
import mysql.connector
import time

def create_consumer():
    for _ in range(10):  # Retry 10 times
        try:
            consumer = KafkaConsumer(
                'your-topic',
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='my-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            return consumer
        except Exception as e:
            print("Kafka server not ready, retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Kafka server not ready after 10 attempts")

def create_mongo_client():
    for _ in range(10):  
        try:
            client = MongoClient('mongo', 27017)
            return client
        except Exception as e:
            print("MongoDB server not ready, retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("MongoDB server not ready after 10 attempts")

def create_mysql_connection():
    for _ in range(10):  
        try:
            connection = mysql.connector.connect(
                host='mysql',
                user='root',
                password='password',
                database='fraud_detection'
            )
            return connection
        except Exception as e:
            print("MySQL server not ready, retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("MySQL server not ready after 10 attempts")

consumer = create_consumer()
mongo_client = create_mongo_client()
mysql_connection = create_mysql_connection()
mysql_cursor = mysql_connection.cursor()


mysql_cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        transaction_id VARCHAR(255),
        transaction_date VARCHAR(255),
        amount DECIMAL(10, 2),
        customer_id VARCHAR(255),
        card_number VARCHAR(255),
        merchant VARCHAR(255),
        location VARCHAR(255),
        fraudulent INT
    )
""")

db = mongo_client.fraud_detection  
collection = db.transactions 

for message in consumer:
    data = message.value
    collection.insert_one(data)
    mysql_cursor.execute("""
        INSERT INTO transactions (transaction_id, transaction_date, amount, customer_id, card_number, merchant, location, fraudulent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (data['transaction_id'], data['transaction_date'], data['amount'], data['customer_id'], data['card_number'], data['merchant'], data['location'], data['fraudulent']))
    mysql_connection.commit()
    print(f"Inserted: {data}")

mysql_cursor.close()
mysql_connection.close()
