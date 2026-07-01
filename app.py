import streamlit as st

from agrisos.config.logging_config import get_logger
from agrisos.ml.predictor import load_model
from agrisos.ui.dashboard import render_app
from agrisos.data.history_repository import initialize_database
initialize_database()

logger = get_logger(__name__)


def main():
    try:
        model = load_model()
        render_app(model)
    except (FileNotFoundError, OSError, EOFError) as exc:
        logger.exception("Model artifacts could not be loaded: %s", exc)
        st.error("AgriSOS could not load its model files. Please regenerate the data and model.")
    except (AttributeError, ImportError, ModuleNotFoundError) as exc:
        logger.exception("Model dependencies could not be loaded: %s", exc)
        st.error("AgriSOS could not start because a model dependency is missing.")
    except Exception as exc:
        logger.exception("Unexpected startup error: %s", exc)
        st.error("AgriSOS could not start. Please check the application logs.")


if __name__ == "__main__":
    main()
