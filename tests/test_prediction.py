import numpy as np

from agrisos.ml.predictor import build_feature_array, predict_distress
from agrisos.ml.scoring import calculate_risk_score, label_distress_level


class DummyModel:
    def __init__(self):
        self.seen_features = None

    def predict(self, features):
        self.seen_features = features
        return np.array(["High"])

    def predict_proba(self, features):
        self.seen_features = features
        return np.array([[0.1, 0.2, 0.7]])


def test_build_feature_array_preserves_feature_order_and_shape():
    features = build_feature_array(-22.0, 3.5, -10, 3, 5, 1.2)

    assert features.shape == (1, 6)
    assert features.tolist() == [[-22.0, 3.5, -10, 3, 5, 1.2]]


def test_calculate_risk_score_matches_existing_threshold_rules():
    assert calculate_risk_score(-31, 7, -21, 3, 2, 2.1) == 100
    assert calculate_risk_score(-16, 4, -11, 1, 5, 1.0) == 45
    assert calculate_risk_score(0, 0, 0, 1, 5, 1.0) == 0


def test_label_distress_level_uses_existing_score_thresholds():
    high = {
        "rainfall_deviation": -31,
        "temperature_stress": 7,
        "market_price_change": -21,
        "crop_stage": 3,
        "soil_moisture_score": 2,
        "input_expenditure_index": 2.1,
    }
    medium = {
        "rainfall_deviation": -16,
        "temperature_stress": 4,
        "market_price_change": -11,
        "crop_stage": 1,
        "soil_moisture_score": 5,
        "input_expenditure_index": 1.0,
    }
    low = {
        "rainfall_deviation": 0,
        "temperature_stress": 0,
        "market_price_change": 0,
        "crop_stage": 1,
        "soil_moisture_score": 5,
        "input_expenditure_index": 1.0,
    }

    assert label_distress_level(high) == "High"
    assert label_distress_level(medium) == "Medium"
    assert label_distress_level(low) == "Low"


def test_predict_distress_calls_model_and_returns_prediction_probabilities_and_score():
    model = DummyModel()

    prediction, probabilities, risk_score = predict_distress(
        model, -22.0, 3.5, -10, 3, 5, 1.2
    )

    assert prediction == "High"
    assert probabilities.tolist() == [0.1, 0.2, 0.7]
    assert risk_score == 40
    assert model.seen_features.tolist() == [[-22.0, 3.5, -10, 3, 5, 1.2]]
