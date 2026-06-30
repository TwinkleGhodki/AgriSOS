import numpy as np
import pandas as pd


def get_market_prices():
    """Simulated market price trends (replace with Agmarknet API in production)."""
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    crops = {
        "Paddy": 2100 + np.cumsum(np.random.normal(-2, 25, 30)),
        "Wheat": 2200 + np.cumsum(np.random.normal(-1, 20, 30)),
        "Cotton": 6500 + np.cumsum(np.random.normal(-5, 80, 30)),
        "Sugarcane": 3200 + np.cumsum(np.random.normal(1, 30, 30)),
        "Maize": 1900 + np.cumsum(np.random.normal(-3, 18, 30)),
    }
    return dates, crops


def get_dashboard_market_prices():
    np.random.seed(42)
    days = pd.date_range(end=pd.Timestamp.today(), periods=30)
    crops_prices = {
        "Paddy": 2100 + np.cumsum(np.random.normal(0, 8, 30)),
        "Cotton": 6500 + np.cumsum(np.random.normal(0, 20, 30)),
        "Wheat": 2200 + np.cumsum(np.random.normal(0, 6, 30)),
        "Sugarcane": 3200 + np.cumsum(np.random.normal(0, 10, 30)),
        "Maize": 1900 + np.cumsum(np.random.normal(0, 7, 30)),
    }
    return days, crops_prices
