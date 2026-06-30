import requests

from agrisos.config.settings import (
    OPEN_METEO_URL,
    WEATHER_TIMEOUT_SECONDS,
    WEATHER_TIMEZONE,
)
from agrisos.data.district_repository import get_district_coordinates


def get_weather_risk(district):
    """Fetch real weather data from Open-Meteo API (no API key required)."""
    lat, lon = get_district_coordinates(district)
    url = (
        f"{OPEN_METEO_URL}"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=precipitation_sum,temperature_2m_max,temperature_2m_min"
        f"&past_days=14&forecast_days=7&timezone={WEATHER_TIMEZONE}"
    )
    try:
        resp = requests.get(url, timeout=WEATHER_TIMEOUT_SECONDS)
        data = resp.json()
        daily = data["daily"]

        rain_vals = [r for r in daily["precipitation_sum"] if r is not None]
        temp_vals = [t for t in daily["temperature_2m_max"] if t is not None]

        avg_rain = sum(rain_vals) / len(rain_vals) if rain_vals else 4.0
        avg_temp = sum(temp_vals) / len(temp_vals) if temp_vals else 32.0

        rainfall_deviation = round(((avg_rain - 5.0) / 5.0) * 100, 1)
        temperature_stress = round(max(0, avg_temp - 32.0), 1)

        forecast_rain = daily["precipitation_sum"][-7:]
        forecast_rain = [r if r is not None else 0 for r in forecast_rain]
        forecast_summary = (
            "Dry spell forecast"
            if sum(forecast_rain) < 10
            else "Adequate rainfall expected"
        )

        return {
            "rainfall_deviation": rainfall_deviation,
            "temperature_stress": temperature_stress,
            "avg_rain_mm": round(avg_rain, 2),
            "avg_temp_c": round(avg_temp, 1),
            "forecast_summary": forecast_summary,
            "source": "Open-Meteo (Live)",
        }
    except Exception:
        return {
            "rainfall_deviation": -22.0,
            "temperature_stress": 3.5,
            "avg_rain_mm": 3.9,
            "avg_temp_c": 35.5,
            "forecast_summary": "Data unavailable (using fallback)",
            "source": "Fallback",
        }
