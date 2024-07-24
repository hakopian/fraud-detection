import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, confusion_matrix,roc_curve, auc
# import matplotlib.pyplot as plt
# import seaborn as sns                                                                                                                                                                         
# Model Report classification, accuract, ROC AUC, confusion matrix

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



    # print("Classification Report:\n", classification_report(test_data['fraudulent'], predictions))
    # print(" Model Accuracy:", accuracy_score(test_data['fraudulent'], predictions))
    # print("ROC AUC Score:", roc_auc_score(test_data['fraudulent'], predictions))
    # print("Confusion Matrix:\n", confusion_matrix(test_data['fraudulent'], predictions))


    # # Plot Confusion Matrix
    # plot_confusion_matrix(test_data['fraudulent'], predictions)
    # plt.show()

    # # Plot ROC Curve
    # plot_roc_curve(test_data['fraudulent'], predictions)
    # plt.show()

    # def plot_confusion_matrix(y_true, y_pred):
    #     cm = confusion_matrix(y_true, y_pred)
    #     plt.figure(figsize=(6, 4))
    #     sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
    #                 xticklabels=['Non-Fraudulent', 'Fraudulent'],
    #                 yticklabels=['Non-Fraudulent', 'Fraudulent'])
    #     plt.xlabel('Predicted')
    #     plt.ylabel('Actual')
    #     plt.title('Confusion Matrix')
    #     plt.show()


    # def plot_roc_curve(y_true, y_pred):
    #     fpr, tpr, _ = roc_curve(y_true, y_pred)
    #     roc_auc = auc(fpr, tpr)
        
    #     plt.figure(figsize=(6, 4))
    #     plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    #     plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    #     plt.xlim([0.0, 1.0])
    #     plt.ylim([0.0, 1.05])
    #     plt.xlabel('False Positive Rate')
    #     plt.ylabel('True Positive Rate')
    #     plt.title('Receiver Operating Characteristic (ROC) Curve')
    #     plt.legend(loc="lower right")
    #     plt.show()


if __name__ == "__main__":
    train_and_predict_model('train_transaction_data.csv', 'test_transaction_data.csv')
