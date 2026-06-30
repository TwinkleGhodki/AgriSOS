import math

from agrisos.utils.validation import (
    PHONE_PLACEHOLDER,
    has_entered_phone_number,
    normalize_phone_number,
    validate_farmer_assessment_inputs,
    validate_market_crop,
    validate_phone_number,
    validate_prediction_inputs,
    validate_sms_inputs,
)


def test_farmer_assessment_accepts_valid_inputs_and_trims_name():
    result = validate_farmer_assessment_inputs(
        "  Ravi Kumar  ",
        "Paddy",
        "Thanjavur",
        "English",
        3,
        "Black Cotton",
        5,
        -10,
        1.2,
    )

    assert result.is_valid
    assert result.errors == []
    assert result.cleaned_data["farmer_name"] == "Ravi Kumar"


def test_farmer_assessment_rejects_missing_name_invalid_choices_and_ranges():
    result = validate_farmer_assessment_inputs(
        "",
        "Rice",
        "Unknown",
        "Marathi",
        5,
        "Peaty",
        0,
        -51,
        3.1,
    )

    assert not result.is_valid
    assert "Farmer name is required." in result.errors
    assert any(error.startswith("Crop must be one of") for error in result.errors)
    assert any(error.startswith("District must be one of") for error in result.errors)
    assert "Soil moisture level must be between 1 and 10." in result.errors
    assert "Market price change must be between -50 and 20." in result.errors
    assert "Input cost vs normal must be between 0.5 and 3.0." in result.errors


def test_farmer_assessment_rejects_non_numeric_values():
    result = validate_farmer_assessment_inputs(
        "Ravi",
        "Paddy",
        "Thanjavur",
        "English",
        1,
        "Black Cotton",
        math.nan,
        "bad",
        True,
    )

    assert not result.is_valid
    assert "Soil moisture level must be a valid number." in result.errors
    assert "Market price change must be a valid number." in result.errors
    assert "Input cost vs normal must be a valid number." in result.errors


def test_prediction_input_validation_checks_weather_and_model_feature_ranges():
    valid = validate_prediction_inputs(-22.0, 3.5, -10, 3, 5, 1.2)
    invalid = validate_prediction_inputs(-1001, -1, -99, 9, 99, 9)

    assert valid.is_valid
    assert not invalid.is_valid
    assert "Rainfall deviation must be between -1000 and 1000." in invalid.errors
    assert "Temperature stress must be between 0 and 100." in invalid.errors


def test_phone_normalization_and_validation():
    assert normalize_phone_number(" +91 98765-43210 ") == "+919876543210"

    is_valid, cleaned, message = validate_phone_number(" +91 98765-43210 ")
    assert is_valid
    assert cleaned == "+919876543210"
    assert message == ""
    assert has_entered_phone_number("+919876543210")


def test_phone_validation_rejects_placeholder_missing_and_local_number():
    assert validate_phone_number(PHONE_PLACEHOLDER)[0] is False
    assert validate_phone_number("")[0] is False
    is_valid, _cleaned, message = validate_phone_number("9876543210")

    assert not is_valid
    assert "country code" in message
    assert not has_entered_phone_number("9876543210")


def test_sms_validation_checks_required_fields_and_phone_format():
    result = validate_sms_inputs("", "Critical", 101, "9876543210", "Rice", "Unknown")

    assert not result.is_valid
    assert "Farmer name is required before sending an SMS." in result.errors
    assert any(error.startswith("Risk level must be one of") for error in result.errors)
    assert "Risk score must be between 0 and 100." in result.errors
    assert "Phone number must include country code, for example +919876543210." in result.errors


def test_market_crop_validation():
    assert validate_market_crop("Paddy", ["Paddy", "Wheat"]).is_valid
    invalid = validate_market_crop("Cotton", ["Paddy", "Wheat"])

    assert not invalid.is_valid
    assert invalid.errors == ["Selected crop must be one of: Paddy, Wheat."]
