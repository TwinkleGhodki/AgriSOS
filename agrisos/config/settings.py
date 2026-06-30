from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "model.pkl"
FARMER_DATA_PATH = BASE_DIR / "farmer_data.csv"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "agrisos.log"

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_TIMEOUT_SECONDS = 10
WEATHER_TIMEZONE = "Asia/Kolkata"

load_dotenv(BASE_DIR / ".env")
