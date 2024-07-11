
# Fraud Detection Data Pipeline

## Overview

This project implements a data pipeline for fraud detection. It generates synthetic transaction data, streams it using Apache Kafka, and stores it in MongoDB and MySQL. A fraud detection model processes the data to identify fraudulent transactions. The entire pipeline is containerized using Docker and managed with Docker Compose.

## Components

### Data Generation

- **Faker Library:** Generates synthetic transaction data.
- **Python Script (`kafka_producer.py`):** Runs the Faker library and sends data to the Kafka producer.

### Data Streaming

- **Kafka Producer:** Sends data to Kafka topics.
- **Apache Kafka:** Acts as the message broker.
- **Kafka Consumer (`kafka_consumer.py`):** Consumes data from Kafka topics.

### Data Storage

- **MongoDB:** Stores raw transaction data.
- **MySQL:** Stores processed and flagged transactions.

### Data Processing

- **Python Script (`fraud_detection_model.py`):** Runs the fraud detection model to identify fraudulent transactions.
- **Fraud Detection Model:** Uses machine learning libraries like Scikit-learn or TensorFlow.

### Containers and Orchestration

- **Docker Containers:** Each component runs in its own Docker container.
- **Docker Compose:** Manages multi-container Docker applications.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Build and Start the Services

To start the services and see logs in real-time:

```bash
docker-compose up
```

To start the services in detached mode:

```bash
docker-compose up -d
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
docker exec -it fraud-detection-mongo-1 mongo
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

