import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns

# Function to plot the confusion matrix
def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=['Non-Fraudulent', 'Fraudulent'],
                yticklabels=['Non-Fraudulent', 'Fraudulent'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()

# Function to plot the ROC curve
def plot_roc_curve(y_true, y_pred):
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(6, 4))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()

# Main function to train the model and make predictions
def train_and_predict_model(train_file_path, test_file_path):
    # Load training data
    train_data = pd.read_csv(train_file_path)
    X = train_data[['amount', 'merchant', 'location']]  # Features
    y = train_data['fraudulent']  # Target variable

    # Add new feature for presence of "Ltd" in merchant
    X.loc[:, 'merchant_contains_ltd'] = X['merchant'].str.contains('Ltd', case=False).astype(int)

    # Split training data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Load testing data
    test_data = pd.read_csv(test_file_path)
    X_test = test_data[['amount', 'merchant', 'location']]

    # Add new feature for presence of "Ltd" in merchant in test data
    X_test.loc[:, 'merchant_contains_ltd'] = X_test['merchant'].str.contains('Ltd', case=False).astype(int)

    # One hot encoding for categorical features in datasets
    X_train = pd.get_dummies(X_train)
    X_val = pd.get_dummies(X_val)
    X_test = pd.get_dummies(X_test)

    # Align columns in validation and test sets to match training set
    X_val = X_val.reindex(columns=X_train.columns, fill_value=0)
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

    # Train the RandomForest model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Make predictions on validation set
    val_predictions = model.predict(X_val)

    # Evaluate the model's performance on the validation set
    print("Classification Report:\n", classification_report(y_val, val_predictions))
    print("Model Accuracy:", accuracy_score(y_val, val_predictions))
    print("ROC AUC Score:", roc_auc_score(y_val, val_predictions))
    print("Confusion Matrix:\n", confusion_matrix(y_val, val_predictions))

    # Plot Confusion Matrix
    plot_confusion_matrix(y_val, val_predictions)
    plt.show()

    # Plot ROC Curve
    plot_roc_curve(y_val, val_predictions)
    plt.show()

    # Make predictions on the test set
    test_predictions = model.predict(X_test)

    # Save the test predictions
    test_data['fraudulent'] = test_predictions
    test_data.to_csv('predicted_test_transaction_data.csv', index=False)

    print("Test predictions saved to 'predicted_test_transaction_data.csv'")

if __name__ == "__main__":
    train_and_predict_model('train_transaction_data.csv', 'test_transaction_data.csv')
