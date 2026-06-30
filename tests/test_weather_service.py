import requests

from agrisos.services import weather_service


class FakeWeatherResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_get_weather_risk_parses_open_meteo_response(monkeypatch):
    payload = {
        "daily": {
            "precipitation_sum": [5, 10, None, 0],
            "temperature_2m_max": [32, 35, None, 36],
            "temperature_2m_min": [24, 25, 26, 27],
        }
    }

    def fake_get(url, timeout):
        assert "latitude=" in url
        assert timeout == weather_service.WEATHER_TIMEOUT_SECONDS
        return FakeWeatherResponse(payload)

    monkeypatch.setattr(weather_service.requests, "get", fake_get)

    result = weather_service.get_weather_risk("Thanjavur")

    assert result["rainfall_deviation"] == 0.0
    assert result["temperature_stress"] == 2.3
    assert result["avg_rain_mm"] == 5.0
    assert result["avg_temp_c"] == 34.3
    assert result["forecast_summary"] == "Adequate rainfall expected"
    assert result["source"] == "Open-Meteo (Live)"


def test_get_weather_risk_uses_fallback_on_timeout(monkeypatch):
    def fake_get(url, timeout):
        raise requests.Timeout("network timeout")

    monkeypatch.setattr(weather_service.requests, "get", fake_get)

    result = weather_service.get_weather_risk("Thanjavur")

    assert result == {
        "rainfall_deviation": -22.0,
        "temperature_stress": 3.5,
        "avg_rain_mm": 3.9,
        "avg_temp_c": 35.5,
        "forecast_summary": "Data unavailable (using fallback)",
        "source": "Fallback",
    }


def test_get_weather_risk_uses_fallback_on_malformed_response(monkeypatch):
    monkeypatch.setattr(
        weather_service.requests,
        "get",
        lambda url, timeout: FakeWeatherResponse({"unexpected": {}}),
    )

    result = weather_service.get_weather_risk("Thanjavur")

    assert result["source"] == "Fallback"
