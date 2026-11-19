"""Flask web application for the Yorùbá–English translation system.

The translation engine remains in ``translator.py``. This module only
provides the web routes and a production-ready server entry point.
"""

import os
import time
import traceback

from flask import Flask, jsonify, render_template, request

from translator import YorubaEnglishTranslator
from yoruba_english_education_dataset import education_dataset

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

print("[SERVER] Initializing translation engine...")
translator = YorubaEnglishTranslator(education_dataset, verbose=True)
print("[SERVER] Translation engine ready.")

VALID_DIRECTIONS = {"en_to_yo", "yo_to_en"}


def json_error(message, status=400):
    """Return a consistent JSON error response."""
    return jsonify(success=False, error=message), status


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/translate")
def translate():
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return json_error("No JSON data received")

        text = str(data.get("text", "")).strip()
        direction = str(data.get("direction", "en_to_yo")).strip()
        if not text:
            return json_error("Please enter text to translate")
        if len(text) > 5000:
            return json_error("Text too long. Maximum 5000 characters.")
        if direction not in VALID_DIRECTIONS:
            return json_error("Invalid direction. Use 'en_to_yo' or 'yo_to_en'.")

        started = time.perf_counter()
        result = translator.en_to_yo(text) if direction == "en_to_yo" else translator.yo_to_en(text)
        return jsonify(
            success=True,
            source=result.source,
            translation=result.translation,
            direction=result.direction,
            match_type=result.match_type,
            confidence=round(result.confidence * 100, 1),
            section=result.section or "N/A",
            alternatives=result.alternatives[:5],
            tokens_processed=result.tokens_processed,
            rules_applied=result.rules_applied,
            processing_time=round(time.perf_counter() - started, 4),
        )
    except Exception as exc:
        traceback.print_exc()
        return json_error(f"Translation failed: {exc}", 500)


@app.post("/api/translate/batch")
def translate_batch():
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return json_error("No JSON data received")
        texts = data.get("texts")
        direction = str(data.get("direction", "en_to_yo")).strip()
        if not isinstance(texts, list) or not texts:
            return json_error("Provide a non-empty list of texts")
        if len(texts) > 50:
            return json_error("Maximum 50 sentences per batch")
        if direction not in VALID_DIRECTIONS:
            return json_error("Invalid direction. Use 'en_to_yo' or 'yo_to_en'.")
        if not all(isinstance(text, str) and text.strip() for text in texts):
            return json_error("Each batch item must be non-empty text")

        started = time.perf_counter()
        results = translator.batch_translate(texts, direction=direction)
        return jsonify(
            success=True,
            count=len(results),
            processing_time=round(time.perf_counter() - started, 4),
            translations=[{
                "source": result.source,
                "translation": result.translation,
                "match_type": result.match_type,
                "confidence": round(result.confidence * 100, 1),
            } for result in results],
        )
    except Exception as exc:
        traceback.print_exc()
        return json_error(str(exc), 500)


@app.get("/api/stats")
def stats():
    return jsonify(success=True, stats=translator.stats())


@app.post("/api/evaluate")
def evaluate():
    try:
        data = request.get_json(silent=True) or {}
        direction = str(data.get("direction", "en_to_yo")).strip()
        sample_size = data.get("sample_size", 50)
        if direction not in VALID_DIRECTIONS:
            return json_error("Invalid direction. Use 'en_to_yo' or 'yo_to_en'.")
        if not isinstance(sample_size, int) or not 1 <= sample_size <= 500:
            return json_error("sample_size must be an integer from 1 to 500.")
        started = time.perf_counter()
        metrics = translator.evaluate(direction=direction, sample_size=sample_size)
        return jsonify(success=True, processing_time=round(time.perf_counter() - started, 4), **metrics)
    except Exception as exc:
        traceback.print_exc()
        return json_error(str(exc), 500)


@app.get("/api/examples")
def examples():
    return jsonify(success=True, examples={
        "en_to_yo": [
            "Good morning, teacher.", "Stand up.", "Open your book.", "I understand.",
            "We are learning mathematics.", "The school is big.", "What is two plus three?",
            "Thank you, teacher.", "I have a question.", "May I go to the toilet?",
            "Read the passage.", "Today is Monday.", "I like mathematics.",
            "The library has many books.", "Be quiet.",
        ],
        "yo_to_en": [
            "E káàárọ̀, olùkọ́.", "E dìde.", "Mo yé mi.", "Kò yé mi.",
            "Ilé ẹ̀kọ́ tóbi.", "E ṣé, olùkọ́.", "Mo ní ìbéèrè kan.", "A ń kọ́ ìṣírò.",
            "Ṣí ìwé rẹ.", "E dákẹ́.", "Mo fẹ́ràn ìṣírò.", "Aago mẹ́jọ ni.",
            "Mo wà dáadáa.", "Ilé ẹ̀kọ́ lẹ́wà.", "E jókòó.",
        ],
    })


@app.get("/api/health")
def health():
    return jsonify(status="healthy", engine="YorubaEnglishTranslator", version=translator.VERSION)


if __name__ == "__main__":
    # Local terminal testing. Hosted services use the Procfile command.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
