from agrisos.config.secrets import get_twilio_credentials
from agrisos.config.logging_config import get_logger
from agrisos.utils.validation import validate_sms_inputs

logger = get_logger(__name__)


def build_sms_message(farmer_name, risk_level, risk_score, crop, district):
    messages = {
        "High": (
            f" AgriSOS ALERT\n"
            f"Farmer: {farmer_name} | {district}\n"
            f"Crop: {crop} | Risk Score: {risk_score}/100 (HIGH)\n"
            f"Immediate action needed!\n"
            f"Helpline: 1800-180-1551 (KVK - Free)"
        ),
        "Medium": (
            f" AgriSOS WARNING\n"
            f"Farmer: {farmer_name} | {district}\n"
            f"Crop: {crop} | Risk Score: {risk_score}/100 (MEDIUM)\n"
            f"Monitor your crop closely this week."
        ),
        "Low": (
            f" AgriSOS Update\n"
            f"Farmer: {farmer_name} | {district}\n"
            f"Crop: {crop} | Risk Score: {risk_score}/100 (LOW)\n"
            f"Conditions look stable. Stay alert!"
        ),
    }
    return messages[risk_level]


def send_sms_alert(farmer_name, risk_level, risk_score, phone_number, crop, district):
    """
    Send SMS alert via Twilio.
    Sign up free at twilio.com -> get SID, Token, Phone number -> add to .env.
    """
    validation = validate_sms_inputs(
        farmer_name, risk_level, risk_score, phone_number, crop, district
    )
    if not validation.is_valid:
        return False, " ".join(validation.errors)

    try:
        from twilio.rest import Client
        from twilio.base.exceptions import TwilioRestException

        credentials = get_twilio_credentials()
        account_sid = credentials["account_sid"]
        auth_token = credentials["auth_token"]
        from_number = credentials["from_number"]

        if not all([account_sid, auth_token, from_number]):
            return False, "Twilio credentials not set in .env file"

        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            body=build_sms_message(farmer_name, risk_level, risk_score, crop, district),
            from_=from_number,
            to=validation.cleaned_data["phone_number"],
        )
        return True, f"SMS sent! SID: {msg.sid}"

    except ImportError as exc:
        logger.warning("Twilio package is not installed: %s", exc)
        return False, "Twilio not installed. Run: pip install twilio"
    except KeyError as exc:
        logger.error("Invalid SMS risk level: %s", exc)
        return False, "SMS could not be prepared because the risk level is invalid."
    except TwilioRestException as exc:
        logger.warning("Twilio rejected SMS request: status=%s code=%s", exc.status, exc.code)
        return False, "SMS could not be sent. Please check the phone number and Twilio setup."
    except ValueError as exc:
        logger.warning("Invalid SMS request data: %s", exc)
        return False, "SMS could not be sent because the alert details are invalid."
