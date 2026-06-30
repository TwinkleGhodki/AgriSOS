from agrisos.ml.predictor import load_model
from agrisos.ui.dashboard import render_app


def main():
    model = load_model()
    render_app(model)


if __name__ == "__main__":
    main()
