from agrisos.config.secrets import get_twilio_credentials


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
    try:
        from twilio.rest import Client

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
            to=phone_number,
        )
        return True, f"SMS sent! SID: {msg.sid}"

    except ImportError:
        return False, "Twilio not installed. Run: pip install twilio"
    except Exception as e:
        return False, str(e)
