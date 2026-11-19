"""Compatibility interface for the established translation engine.

This module delegates to ``translator.py`` instead of maintaining a separate,
incomplete pipeline. The translation rules and dataset are not changed.
"""

from translator import YorubaEnglishTranslator
from yoruba_english_education_dataset import education_dataset


class YorubaMTPipeline:
    """Dictionary and rule-based translator compatible with earlier imports."""

    def __init__(self, polite=False):
        self.polite = polite
        self._translator = YorubaEnglishTranslator(education_dataset)

    def translate(self, english):
        """Translate English to Yorùbá using the existing engine."""
        result = self._translator.en_to_yo(english)
        return {
            "translation": result.translation,
            "source": result.match_type,
            "rules_applied": result.rules_applied,
        }

    def translate_yo_to_en(self, yoruba):
        """Translate Yorùbá to English using the existing engine."""
        result = self._translator.yo_to_en(yoruba)
        return {
            "translation": result.translation,
            "source": result.match_type,
            "rules_applied": result.rules_applied,
        }

    def lookup_word(self, word, lang="en"):
        direction = self._translator.en_to_yo if lang == "en" else self._translator.yo_to_en
        result = direction(word)
        return [{"source": result.source, "translation": result.translation}]
