import os


def get_twilio_credentials():
    return {
        "account_sid": os.getenv("TWILIO_SID"),
        "auth_token": os.getenv("TWILIO_TOKEN"),
        "from_number": os.getenv("TWILIO_PHONE"),
    }
