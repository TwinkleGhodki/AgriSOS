import requests

from agrisos.config.logging_config import get_logger

logger = get_logger(__name__)


def translate_recommendations(recommendations, language):
    if language == "English":
        return recommendations
    try:
        from deep_translator import GoogleTranslator

        lang_code = "ta" if "Tamil" in language else "hi"
        translator = GoogleTranslator(source="en", target=lang_code)
        return [translator.translate(rec) for rec in recommendations]
    except ImportError as exc:
        logger.warning("Translation package is not installed: %s", exc)
        return recommendations
    except requests.RequestException as exc:
        logger.warning("Translation request failed for language=%s error=%s", language, exc)
        return recommendations
    except (TypeError, ValueError, RuntimeError) as exc:
        logger.warning("Translation failed for language=%s error=%s", language, exc)
        return recommendations
