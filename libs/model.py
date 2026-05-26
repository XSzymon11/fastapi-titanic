import pickle
from pathlib import Path

import pandas as pd


FEATURE_COLUMNS = [
    "Pclass",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "male",
    "Q",
    "S"
]


def load_model(model_path: Path):
    with open(model_path, "rb") as file:
        return pickle.load(file)


def passenger_to_dataframe(data):
    male = 1 if data.sex == "male" else 0

    embarked_q = 1 if data.embarked == "Q" else 0
    embarked_s = 1 if data.embarked == "S" else 0

    df = pd.DataFrame([{
        "Pclass": data.pclass,
        "Age": data.age,
        "SibSp": data.sibsp,
        "Parch": data.parch,
        "Fare": data.fare,
        "male": male,
        "Q": embarked_q,
        "S": embarked_s
    }])

    return df[FEATURE_COLUMNS]


def predict_survival(data, model_path: Path):
    model = load_model(model_path)

    df = passenger_to_dataframe(data)

    prediction = model.predict(df)
    survived = int(prediction[0])

    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(df)[0][1])

    return survived, probability
