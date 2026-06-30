def calculate_risk_score(
    rainfall_deviation,
    temperature_stress,
    price_change,
    crop_stage,
    soil_moisture,
    expenditure,
):
    score = 0
    if rainfall_deviation < -30:
        score += 35
    elif rainfall_deviation < -15:
        score += 20
    if temperature_stress > 6:
        score += 20
    elif temperature_stress > 3:
        score += 10
    if price_change < -20:
        score += 25
    elif price_change < -10:
        score += 15
    if crop_stage == 3:
        score += 10
    if soil_moisture < 3:
        score += 10
    if expenditure > 2:
        score += 10
    return min(score, 100)


def label_distress_level(row):
    score = calculate_risk_score(
        row["rainfall_deviation"],
        row["temperature_stress"],
        row["market_price_change"],
        row["crop_stage"],
        row["soil_moisture_score"],
        row["input_expenditure_index"],
    )
    if score >= 60:
        return "High"
    if score >= 35:
        return "Medium"
    return "Low"
