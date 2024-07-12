import mysql.connector
import pandas as pd

def store_flagged_transactions(file_path):
    conn = mysql.connector.connect(
        host='localhost',
        user='username',
        password='password',
        database='fraud_detection'
    )
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS flagged_transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        transaction_id VARCHAR(255),
        amount FLOAT,
        fraudulent BOOLEAN
    )''')

    data = pd.read_csv(file_path)
    flagged_transactions = data[data['fraudulent'] == 1]

    for _, row in flagged_transactions.iterrows():
        cursor.execute('''INSERT INTO flagged_transactions (transaction_id, amount, fraudulent)
                          VALUES (%s, %s, %s)''',
                       (row['transaction_id'], row['amount'], row['fraudulent']))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    store_flagged_transactions('synthetic_transaction_data.csv')
