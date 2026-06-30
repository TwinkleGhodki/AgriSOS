from agrisos.ml.training import train_model


def main():
    _, metrics = train_model()
    print("Model trained!")
    print(f"Accuracy: {metrics['accuracy'] * 100:.1f}%")
    print(metrics["classification_report"])
    print("model.pkl saved!")


if __name__ == "__main__":
    main()
