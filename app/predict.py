import pickle
import numpy as np

with open("app/bank_churn_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_churn(features):
    X = np.array(features).reshape(1, -1)
    return int(model.predict(X)[0])
