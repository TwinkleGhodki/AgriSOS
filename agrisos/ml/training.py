import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from agrisos.config.settings import FARMER_DATA_PATH, MODEL_PATH
from agrisos.ml.features import FEATURE_COLUMNS


def train_model(data_path=FARMER_DATA_PATH, model_path=MODEL_PATH):
    df = pd.read_csv(data_path)
    x = df[FEATURE_COLUMNS]
    y = df["distress_level"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(x_train, y_train)

    preds = model.predict(x_test)
    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "classification_report": classification_report(y_test, preds),
    }

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    return model, metrics
