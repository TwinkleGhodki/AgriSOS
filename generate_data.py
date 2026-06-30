from agrisos.config.settings import FARMER_DATA_PATH
from agrisos.data.synthetic_data import generate_farmer_dataset


def main():
    df = generate_farmer_dataset()
    df.to_csv(FARMER_DATA_PATH, index=False)
    print("Dataset created!")
    print(df["distress_level"].value_counts())


if __name__ == "__main__":
    main()
