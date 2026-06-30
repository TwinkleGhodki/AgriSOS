import sys
import types

from agrisos.services import alerts_service


class FakeMessage:
    sid = "SM123"


class FakeMessages:
    last_request = None

    def create(self, **kwargs):
        FakeMessages.last_request = kwargs
        return FakeMessage()


class FakeClient:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.messages = FakeMessages()


def install_fake_twilio(monkeypatch):
    twilio_module = types.ModuleType("twilio")
    rest_module = types.ModuleType("twilio.rest")
    base_module = types.ModuleType("twilio.base")
    exceptions_module = types.ModuleType("twilio.base.exceptions")

    class FakeTwilioRestException(Exception):
        def __init__(self, status=400, uri="", msg="", code=123):
            super().__init__(msg)
            self.status = status
            self.code = code

    rest_module.Client = FakeClient
    exceptions_module.TwilioRestException = FakeTwilioRestException
    monkeypatch.setitem(sys.modules, "twilio", twilio_module)
    monkeypatch.setitem(sys.modules, "twilio.rest", rest_module)
    monkeypatch.setitem(sys.modules, "twilio.base", base_module)
    monkeypatch.setitem(sys.modules, "twilio.base.exceptions", exceptions_module)
    return FakeTwilioRestException


def test_build_sms_message_uses_existing_high_risk_content():
    message = alerts_service.build_sms_message("Ravi", "High", 72, "Paddy", "Thanjavur")

    assert "AgriSOS ALERT" in message
    assert "Farmer: Ravi | Thanjavur" in message
    assert "Crop: Paddy | Risk Score: 72/100 (HIGH)" in message


def test_send_sms_alert_validates_before_twilio_import():
    success, message = alerts_service.send_sms_alert(
        "", "High", 72, "9876543210", "Paddy", "Thanjavur"
    )

    assert not success
    assert "Farmer name is required" in message
    assert "country code" in message


def test_send_sms_alert_returns_missing_credentials_message(monkeypatch):
    install_fake_twilio(monkeypatch)
    monkeypatch.setattr(
        alerts_service,
        "get_twilio_credentials",
        lambda: {"account_sid": None, "auth_token": None, "from_number": None},
    )

    success, message = alerts_service.send_sms_alert(
        "Ravi", "High", 72, "+919876543210", "Paddy", "Thanjavur"
    )

    assert not success
    assert message == "Twilio credentials not set in .env file"


def test_send_sms_alert_uses_twilio_client_with_normalized_phone(monkeypatch):
    install_fake_twilio(monkeypatch)
    FakeMessages.last_request = None
    monkeypatch.setattr(
        alerts_service,
        "get_twilio_credentials",
        lambda: {
            "account_sid": "AC123",
            "auth_token": "token",
            "from_number": "+10000000000",
        },
    )

    success, message = alerts_service.send_sms_alert(
        "Ravi", "High", 72, "+91 98765-43210", "Paddy", "Thanjavur"
    )

    assert success
    assert message == "SMS sent! SID: SM123"
    assert FakeMessages.last_request["from_"] == "+10000000000"
    assert FakeMessages.last_request["to"] == "+919876543210"
    assert "AgriSOS ALERT" in FakeMessages.last_request["body"]
