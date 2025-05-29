import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

def train_churn_model():
    data = pd.read_csv("data/Churn_Modelling.csv")
    data = data.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)
    for col in ['Geography', 'Gender']:
        data[col] = LabelEncoder().fit_transform(data[col])
    features = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance',
                'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
    X = data[features]
    y = data['Exited']
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    with open("app/bank_churn_model.pkl", "wb") as f:
        pickle.dump(clf, f)

if __name__ == "__main__":
    train_churn_model()
