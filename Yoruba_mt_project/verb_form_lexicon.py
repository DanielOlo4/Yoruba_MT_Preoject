"""Runtime index for the generated English-Yorùbá verb-form lexicon."""
from __future__ import annotations

import csv
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


def _key(value: str) -> str:
    value = unicodedata.normalize("NFC", value).lower().strip()
    return re.sub(r"\s+", " ", value)


@dataclass(frozen=True)
class VerbFormEntry:
    english_surface: str
    english_lemma: str
    english_morphology: str
    yoruba_surface: str
    yoruba_lemma: str
    yoruba_construction: str
    pos: str
    valency: str
    object_condition: str
    source: str

    @property
    def tam_marker(self) -> str:
        return {"perfective": "ti", "perfect": "ti", "progressive": "ń", "imperfective": "ń", "future": "yóò"}.get(self.yoruba_construction, "")


class VerbFormLexicon:
    """Indexes only validated VERB rows and resolves object-sensitive forms."""
    def __init__(self, path: str | Path | None = None) -> None:
        source = Path(path or Path(__file__).with_name("yoruba_english_verb_forms.csv"))
        self.by_english_surface: dict[str, list[VerbFormEntry]] = defaultdict(list)
        self.by_english_lemma: dict[str, list[VerbFormEntry]] = defaultdict(list)
        self.by_yoruba_lemma: dict[str, list[VerbFormEntry]] = defaultdict(list)
        self.entries: list[VerbFormEntry] = []
        if not source.exists():
            return
        with source.open(encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                if row.get("pos") != "VERB" or row.get("object_condition") == "review_needed":
                    continue
                entry = VerbFormEntry(**{field: row.get(field, "") for field in VerbFormEntry.__dataclass_fields__})
                self.entries.append(entry)
                self.by_english_surface[_key(entry.english_surface)].append(entry)
                self.by_english_lemma[_key(entry.english_lemma)].append(entry)
                self.by_yoruba_lemma[_key(entry.yoruba_lemma)].append(entry)

    @staticmethod
    def _select(candidates: list[VerbFormEntry], has_object: bool, morphology: str | None = None) -> VerbFormEntry | None:
        if morphology:
            candidates = [entry for entry in candidates if entry.english_morphology == morphology] or candidates
        desired = "with_object" if has_object else "without_object"
        return next((entry for entry in candidates if entry.object_condition == desired), None) or next((entry for entry in candidates if entry.object_condition == "with_object"), None) or (candidates[0] if candidates else None)

    def english(self, surface: str, *, lemma: str = "", morphology: str | None = None, has_object: bool = True) -> VerbFormEntry | None:
        candidates = self.by_english_surface.get(_key(surface), [])
        if not candidates and lemma:
            candidates = self.by_english_lemma.get(_key(lemma), [])
        return self._select(candidates, has_object, morphology)

    def yoruba(self, lemma: str, *, has_object: bool = True) -> VerbFormEntry | None:
        return self._select(self.by_yoruba_lemma.get(_key(lemma), []), has_object, "base")

    def stats(self) -> dict[str, int]:
        return {"verb_form_entries": len(self.entries), "english_surfaces": len(self.by_english_surface), "yoruba_lemmas": len(self.by_yoruba_lemma)}
