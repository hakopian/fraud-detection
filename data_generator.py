import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_transaction_data(num_records):
    data = []
    for _ in range(num_records):
        transaction = {
            'transaction_id': fake.uuid4(),
            'transaction_date': fake.date_time_this_year(),
            'amount': round(np.random.uniform(1.0, 1000.0), 2),
            'customer_id': fake.uuid4(),
            'card_number': fake.credit_card_number(),
            'merchant': fake.company(),
            'location': fake.address(),
            'fraudulent': np.random.choice([0, 1], p=[0.95, 0.05])  # 5% fraud cases
        }
        data.append(transaction)
    return pd.DataFrame(data)

if __name__ == "__main__":
    transaction_data = generate_transaction_data(1000)
    transaction_data.to_csv('synthetic_transaction_data.csv', index=False)
