import pickle

import numpy as np

from agrisos.config.settings import FARMER_DATA_PATH, MODEL_PATH
from agrisos.data.synthetic_data import generate_farmer_dataset
from agrisos.ml.features import FEATURE_COLUMNS
from agrisos.ml.scoring import calculate_risk_score
from agrisos.ml.training import train_model


def ensure_model_artifacts():
    if MODEL_PATH.exists() and FARMER_DATA_PATH.exists():
        return

    df = generate_farmer_dataset()
    df.to_csv(FARMER_DATA_PATH, index=False)
    train_model()


def load_model():
    ensure_model_artifacts()
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def build_feature_array(
    rainfall_deviation,
    temperature_stress,
    price_change,
    crop_stage,
    soil_moisture,
    expenditure_ratio,
):
    return np.array(
        [
            [
                rainfall_deviation,
                temperature_stress,
                price_change,
                crop_stage,
                soil_moisture,
                expenditure_ratio,
            ]
        ]
    )


def predict_distress(
    model,
    rainfall_deviation,
    temperature_stress,
    price_change,
    crop_stage,
    soil_moisture,
    expenditure_ratio,
):
    features = build_feature_array(
        rainfall_deviation,
        temperature_stress,
        price_change,
        crop_stage,
        soil_moisture,
        expenditure_ratio,
    )
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    risk_score = calculate_risk_score(
        rainfall_deviation,
        temperature_stress,
        price_change,
        crop_stage,
        soil_moisture,
        expenditure_ratio,
    )
    return prediction, probabilities, risk_score
