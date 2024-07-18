# Fraud Detection Data Pipeline

## Project Overview

This project is designed to detect and process fraud related data. Using a Docker Compose setup it integrates multiple components (Kafka for messaging, Python scripts for data processing, MySQL for storage, and MongoDB for additional data management).

## Components

### Docker Compose
Docker Compose is used to orchestrate the multi-container application. It defines the services, networks, and volumes required for the project.

### Kafka
Kafka is a distributed messaging system used to stream data between the producer and consumer scripts. It ensures reliable data transfer and processing.

- **kafka_producer.py**: This script generates and sends messages to a Kafka topic.
- **kafka_consumer.py**: This script consumes messages from a Kafka topic and stores them in MongoDB and MySQL.

### Python Scripts
- **data_generator.py**: Generates synthetic data for testing and development purposes.
- **fraud_detection_model.py**: Trains a model on historical data to predict fraudulent activities in future data.
- **mysql_storage.py**: Handles the storage of processed data into a MySQL database.

### MySQL
A relational database used to store the processed data. It ensures structured storage and efficient querying.

### MongoDB
A NoSQL database used for storing unstructured data and additional metadata required for the project.

## Interaction

1. **Data Generation**: The `data_generator.py` script creates synthetic data.
2. **Data Production**: The `kafka_producer.py` script sends this data to a Kafka topic.
3. **Data Consumption**: The `kafka_consumer.py` script retrieves data from the Kafka topic and stores it in MongoDB and MySQL.
4. **Fraud Detection**: The `fraud_detection_model.py` processes historical data to train a model that predicts fraudulent activities.

## Running the Project

## Getting Started

### Build and Start the Services

To start the services and see logs in real-time:

```bash
docker-compose up
```

### Stopping the Services

To stop all services:

```bash
docker-compose down
```

## Accessing the Services

### MongoDB

To access MongoDB:

```bash
docker exec -it fraud-detection-mongo-1 mongosh
```

Within the MongoDB shell:

```sql
use fraud_detection;
show collections;
db.transactions.find().pretty();
db.transactions.find({ fraudulent: 1 }).pretty();
```

### MySQL

To access MySQL:

```bash
docker exec -it fraud-detection-mysql-1 mysql -u root -p
```

Enter the MySQL root password (default is \`password\`).

Within the MySQL shell:

```sql
USE fraud_detection;
SHOW TABLES;
SELECT * FROM transactions;
SELECT * FROM transactions WHERE fraudulent = 1;
```

## Cleaning Data

### Delete Data in MongoDB

To delete all documents in the \`transactions\` collection:

```sql
db.transactions.deleteMany({});
```

### Delete Data in MySQL

To delete all records in the \`transactions\` table:

```sql
DELETE FROM transactions;
```

