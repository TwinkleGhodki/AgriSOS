import numpy as np
import pandas as pd

from agrisos.ml.scoring import label_distress_level


def generate_farmer_dataset(n=600, random_seed=42):
    np.random.seed(random_seed)
    df = pd.DataFrame(
        {
            "rainfall_deviation": np.random.uniform(-60, 20, n),
            "temperature_stress": np.random.uniform(0, 10, n),
            "market_price_change": np.random.uniform(-40, 15, n),
            "crop_stage": np.random.randint(1, 5, n),
            "soil_moisture_score": np.random.uniform(1, 10, n),
            "input_expenditure_index": np.random.uniform(0.5, 2.5, n),
        }
    )
    df["distress_level"] = df.apply(label_distress_level, axis=1)
    return df
