import pandas as pd


DISTRICT_COORDS = {
    "Thanjavur": (10.7870, 79.1378),
    "Nagpur": (21.1458, 79.0882),
    "Ludhiana": (30.9010, 75.8573),
    "Warangal": (17.9784, 79.5941),
    "Nashik": (19.9975, 73.7898),
    "Pune": (18.5204, 73.8567),
    "Amravati": (20.9320, 77.7523),
    "Jalgaon": (21.0077, 75.5626),
    "Nanded": (19.1383, 77.3210),
    "Solapur": (17.6868, 75.9067),
}


def get_district_coordinates(district):
    return DISTRICT_COORDS.get(district, (20.5937, 78.9629))


def get_district_risk_data():
    districts_data = pd.DataFrame(
        {
            "District": [
                "Thanjavur",
                "Nagpur",
                "Ludhiana",
                "Warangal",
                "Nashik",
                "Pune",
                "Amravati",
                "Jalgaon",
                "Nanded",
                "Solapur",
            ],
            "Risk_Score": [72, 45, 28, 81, 55, 38, 68, 74, 61, 49],
            "Farmers_At_Risk": [1240, 890, 320, 1580, 670, 410, 1100, 1320, 950, 720],
            "Primary_Crop": [
                "Paddy",
                "Cotton",
                "Wheat",
                "Cotton",
                "Grapes",
                "Sugarcane",
                "Cotton",
                "Banana",
                "Cotton",
                "Sugarcane",
            ],
        }
    )
    districts_data["Risk_Level"] = districts_data["Risk_Score"].apply(
        lambda x: "🔴 High" if x > 60 else "🟡 Medium" if x > 35 else "🟢 Low"
    )
    return districts_data
