import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_transaction_data(num_records, labeled=True):
    data = []
    for _ in range(num_records):
        amount = round(np.random.uniform(1.0, 1000.0), 2)
        merchant = fake.company()
        location = fake.address()
        
        transaction = {
            'transaction_id': fake.uuid4(),
            'transaction_date': fake.date_time_this_year(),
            'amount': amount,
            'customer_id': fake.uuid4(),
            'card_number': fake.credit_card_number(),
            'merchant': merchant,
            'location': location,
        }
        
        if labeled:
            # fraud determination rule (can be changed)
            fraudulent = 0
            if amount > 500 or "Ltd" in merchant or "Street" in location:
                fraudulent = 1
            transaction['fraudulent'] = fraudulent
        
        data.append(transaction)
    return pd.DataFrame(data)

if __name__ == "__main__":
    # gen. labeled training data
    train_transaction_data = generate_transaction_data(800, labeled=True)
    train_transaction_data.to_csv('train_transaction_data.csv', index=False)

    # gen. unlabeled testing data
    test_transaction_data = generate_transaction_data(200, labeled=False)
    test_transaction_data.to_csv('test_transaction_data.csv', index=False)
