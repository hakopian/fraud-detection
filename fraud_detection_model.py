import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def train_and_predict_model(train_file_path, test_file_path):
    # Load training data
    train_data = pd.read_csv(train_file_path)
    X_train = train_data[['amount', 'merchant', 'location']]
    y_train = train_data['fraudulent']

    # Load testing data
    test_data = pd.read_csv(test_file_path)
    X_test = test_data[['amount', 'merchant', 'location']]
    
    # one hot Encoding for categorical features in datasets
    X_train = pd.get_dummies(X_train)
    X_test = pd.get_dummies(X_test)

    # aligning columns in test to match train
    X_test = X_test.reindex(columns = X_train.columns, fill_value=0)
    
    # train the model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # make predictions
    predictions = model.predict(X_test)
    
    # save the predictions
    test_data['fraudulent'] = predictions
    test_data.to_csv('predicted_test_transaction_data.csv', index=False)

if __name__ == "__main__":
    train_and_predict_model('train_transaction_data.csv', 'test_transaction_data.csv')
