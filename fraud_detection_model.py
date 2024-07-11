import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def train_model(file_path):
    data = pd.read_csv(file_path)
    X = data[['amount', 'merchant', 'location']]
    y = data['fraudulent']

    
    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))

if __name__ == "__main__":
    train_model('synthetic_transaction_data.csv')
