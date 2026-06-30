import math
import re
from dataclasses import dataclass, field


ALLOWED_CROPS = ["Paddy", "Wheat", "Cotton", "Sugarcane", "Maize"]
ALLOWED_DISTRICTS = ["Thanjavur", "Nagpur", "Ludhiana", "Warangal", "Nashik"]
ALLOWED_LANGUAGES = ["English", "Tamil (தமிழ்)", "Hindi (हिंदी)"]
ALLOWED_CROP_STAGES = [1, 2, 3, 4]
ALLOWED_SOIL_TYPES = ["Black Cotton", "Red Loamy", "Alluvial", "Sandy Loam", "Clay"]

SOIL_MOISTURE_RANGE = (1, 10)
PRICE_CHANGE_RANGE = (-50, 20)
EXPENDITURE_RATIO_RANGE = (0.5, 3.0)
RISK_SCORE_RANGE = (0, 100)
PHONE_PLACEHOLDER = "+91XXXXXXXXXX"


@dataclass
class ValidationResult:
    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
    cleaned_data: dict = field(default_factory=dict)

    def add_error(self, message):
        self.is_valid = False
        self.errors.append(message)


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _validate_choice(result, field_label, value, allowed_values):
    if value not in allowed_values:
        result.add_error(f"{field_label} must be one of: {', '.join(map(str, allowed_values))}.")


def _validate_number_range(result, field_label, value, min_value, max_value):
    if not _is_number(value):
        result.add_error(f"{field_label} must be a valid number.")
        return
    if value < min_value or value > max_value:
        result.add_error(f"{field_label} must be between {min_value} and {max_value}.")


def validate_farmer_assessment_inputs(
    farmer_name,
    crop,
    district,
    language,
    crop_stage,
    soil_type,
    soil_moisture,
    price_change,
    expenditure_ratio,
):
    result = ValidationResult()
    cleaned_name = (farmer_name or "").strip()

    if not cleaned_name:
        result.add_error("Farmer name is required.")
    elif len(cleaned_name) > 80:
        result.add_error("Farmer name must be 80 characters or fewer.")

    _validate_choice(result, "Crop", crop, ALLOWED_CROPS)
    _validate_choice(result, "District", district, ALLOWED_DISTRICTS)
    _validate_choice(result, "Advisory language", language, ALLOWED_LANGUAGES)
    _validate_choice(result, "Crop growth stage", crop_stage, ALLOWED_CROP_STAGES)
    _validate_choice(result, "Soil type", soil_type, ALLOWED_SOIL_TYPES)
    _validate_number_range(result, "Soil moisture level", soil_moisture, *SOIL_MOISTURE_RANGE)
    _validate_number_range(result, "Market price change", price_change, *PRICE_CHANGE_RANGE)
    _validate_number_range(
        result, "Input cost vs normal", expenditure_ratio, *EXPENDITURE_RATIO_RANGE
    )

    result.cleaned_data = {
        "farmer_name": cleaned_name,
        "crop": crop,
        "district": district,
        "language": language,
        "crop_stage": crop_stage,
        "soil_type": soil_type,
        "soil_moisture": soil_moisture,
        "price_change": price_change,
        "expenditure_ratio": expenditure_ratio,
    }
    return result


def validate_prediction_inputs(
    rainfall_deviation,
    temperature_stress,
    price_change,
    crop_stage,
    soil_moisture,
    expenditure_ratio,
):
    result = ValidationResult()
    _validate_number_range(result, "Rainfall deviation", rainfall_deviation, -1000, 1000)
    _validate_number_range(result, "Temperature stress", temperature_stress, 0, 100)
    _validate_number_range(result, "Market price change", price_change, *PRICE_CHANGE_RANGE)
    _validate_choice(result, "Crop growth stage", crop_stage, ALLOWED_CROP_STAGES)
    _validate_number_range(result, "Soil moisture level", soil_moisture, *SOIL_MOISTURE_RANGE)
    _validate_number_range(
        result, "Input cost vs normal", expenditure_ratio, *EXPENDITURE_RATIO_RANGE
    )
    return result


def validate_market_crop(crop, allowed_crops):
    result = ValidationResult()
    _validate_choice(result, "Selected crop", crop, allowed_crops)
    return result


def validate_sms_inputs(farmer_name, risk_level, risk_score, phone_number, crop, district):
    result = ValidationResult()
    cleaned_phone = normalize_phone_number(phone_number)

    if not (farmer_name or "").strip():
        result.add_error("Farmer name is required before sending an SMS.")
    _validate_choice(result, "Risk level", risk_level, ["High", "Medium", "Low"])
    _validate_number_range(result, "Risk score", risk_score, *RISK_SCORE_RANGE)
    _validate_choice(result, "Crop", crop, ALLOWED_CROPS)
    _validate_choice(result, "District", district, ALLOWED_DISTRICTS)

    if not cleaned_phone or cleaned_phone == PHONE_PLACEHOLDER:
        result.add_error("Phone number is required.")
    elif not re.fullmatch(r"\+[1-9]\d{9,14}", cleaned_phone):
        result.add_error("Phone number must include country code, for example +919876543210.")

    result.cleaned_data = {"phone_number": cleaned_phone}
    return result


def validate_phone_number(phone_number):
    cleaned_phone = normalize_phone_number(phone_number)
    if not cleaned_phone or cleaned_phone == PHONE_PLACEHOLDER:
        return False, cleaned_phone, "Phone number is required."
    if not re.fullmatch(r"\+[1-9]\d{9,14}", cleaned_phone):
        return (
            False,
            cleaned_phone,
            "Phone number must include country code, for example +919876543210.",
        )
    return True, cleaned_phone, ""


def normalize_phone_number(phone_number):
    if phone_number is None:
        return ""
    return re.sub(r"[\s\-()]", "", str(phone_number).strip())


def has_entered_phone_number(phone_number):
    is_valid, _cleaned_phone, _message = validate_phone_number(phone_number)
    return is_valid
