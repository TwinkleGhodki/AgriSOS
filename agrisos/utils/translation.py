def translate_recommendations(recommendations, language):
    if language == "English":
        return recommendations
    try:
        from deep_translator import GoogleTranslator

        lang_code = "ta" if "Tamil" in language else "hi"
        translator = GoogleTranslator(source="en", target=lang_code)
        return [translator.translate(rec) for rec in recommendations]
    except Exception:
        return recommendations
