from datetime import datetime

from agrisos.data.history_repository import (
    save_prediction,
    get_prediction_history,
    delete_history,
)


def save_prediction_history(
    farmer_name,
    crop,
    district,
    risk_level,
    risk_score,
    weather,
    recommendation,
):
    """
    Preparing a prediction record and saving it to the database.
    """

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_prediction(
        farmer_name=farmer_name,
        crop=crop,
        district=district,
        risk_level=risk_level,
        risk_score=round(float(risk_score), 2),
        weather=weather,
        recommendation=recommendation,
        created_at=created_at,
    )


def get_history():
    """
    Returning all saved predictions.
    """
    return get_prediction_history()


def get_history_statistics():
    """
    Returns summary statistics for prediction history.
    """

    history = get_history()

    total_predictions = len(history)

    if total_predictions == 0:
        return {
            "total": 0,
            "high_risk": 0,
            "average_score": 0,
        }

    high_risk = (history["Risk Level"] == "High").sum()

    average_score = (
        history["Risk Score"]
        .str.replace("%", "", regex=False)
        .astype(float)
        .mean()
    )

    return {
        "total": total_predictions,
        "high_risk": int(high_risk),
        "average_score": round(average_score, 1),
    }

def clear_history():
    """
    Deleting all prediction history.
    """
    delete_history()