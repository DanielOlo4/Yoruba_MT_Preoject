"""Supplemental MT Model data in the live project's Python format.

This module is deliberately data-only.  It is not imported by ``app.py``,
``translator.py`` or ``mt_pipeline.py``.  The established live translation
pipeline therefore continues to use ``education_dataset`` unchanged.

The entries below were transcribed from the supplied MT Model notebooks and
normalised to NFC Unicode.  They are available for controlled future research,
testing, or a separately approved merge into a new dataset version.
"""

from __future__ import annotations

import unicodedata
from typing import Dict, List, Tuple


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


# (English lemma, part of speech, Yorùbá form)
SUPPLEMENTAL_LEXICON: List[Tuple[str, str, str]] = [
    ("person", "N", "ẹni"), ("child", "N", "ọmọ"),
    ("king", "N", "ọba"), ("father", "N", "bàbá"),
    ("mother", "N", "ìyá"), ("brother", "N", "arákùnrin"),
    ("sister", "N", "arábìnrin"), ("friend", "N", "ọ̀rẹ́"),
    ("teacher", "N", "olùkọ́"), ("student", "N", "akẹ́kọ̀ọ́"),
    ("house", "N", "ilé"), ("school", "N", "ilé-ẹ̀kọ́"),
    ("market", "N", "ọjà"), ("vehicle", "N", "ọkọ̀"),
    ("car", "N", "ọkọ̀ ayọ́kẹ́lẹ́"), ("train", "N", "ọkọ̀ ojú irin"),
    ("water", "N", "omi"), ("food", "N", "oúnjẹ"),
    ("bread", "N", "bùrẹ́dì"), ("pounded yam", "N", "iyán"),
    ("meat", "N", "ẹran"), ("fish", "N", "ẹja"),
    ("salt", "N", "iyọ̀"), ("money", "N", "owó"),
    ("cloth", "N", "aṣọ"), ("shoe", "N", "bàtà"),
    ("book", "N", "ìwé"), ("pencil", "N", "pẹ́ǹsù"),
    ("table", "N", "tábìlì"), ("chair", "N", "àga"),
    ("door", "N", "ilẹ̀kùn"), ("window", "N", "fèrèsé"),
    ("rice", "N", "ìrẹsì"), ("eye", "N", "ojú"),
    ("hand", "N", "ọwọ́"), ("head", "N", "orí"),
    ("day", "N", "ọjọ́"), ("night", "N", "alẹ́"),
    ("morning", "N", "òwúrọ̀"), ("evening", "N", "ìrọ̀lẹ́"),
    ("today", "ADV", "òní"), ("tomorrow", "ADV", "ọ̀la"),
    ("yesterday", "ADV", "àná"), ("there", "ADV", "nibẹ̀"),
    ("big", "ADJ", "ńlá"), ("small", "ADJ", "kéré"),
    ("good", "ADJ", "dára"), ("bad", "ADJ", "búburú"),
    ("new", "ADJ", "tuntun"), ("old", "ADJ", "àtijọ́"),
    ("red", "ADJ", "pupa"), ("white", "ADJ", "funfun"),
    ("black", "ADJ", "dúdú"), ("green", "ADJ", "aláwọ̀ ewé"),
    ("blue", "ADJ", "búlúù"), ("yellow", "ADJ", "ofeefee"),
    ("want", "V", "fẹ́"), ("eat", "V", "jẹ"),
    ("drink", "V", "mu"), ("go", "V", "lọ"),
    ("come", "V", "wá"), ("see", "V", "rí"),
    ("hear", "V", "gbọ́"), ("say", "V", "sọ"),
    ("read", "V", "ka"), ("write", "V", "kọ"),
    ("sleep", "V", "sùn"), ("stand", "V", "dúró"),
    ("sit", "V", "jókòó"), ("buy", "V", "ra"),
    ("sell", "V", "tà"), ("receive", "V", "gbà"),
    ("do", "V", "ṣe"), ("know", "V", "mọ̀"),
    ("learn", "V", "kọ́"), ("teach", "V", "kọ́ni"),
    ("help", "V", "rànlọ́wọ́"), ("play", "V", "ṣeré"),
    ("not", "NEG", "kò"), ("to", "PREP", "sí"),
    ("in", "PREP", "ní"), ("at", "PREP", "ní"),
    ("with", "PREP", "pẹ̀lú"), ("from", "PREP", "láti"),
    ("and", "CONJ", "àti"), ("but", "CONJ", "ṣùgbọ́n"),
    ("because", "CONJ", "nítorí"), ("the", "DET", "náà"),
    ("a", "DET", "kan"), ("my", "POSS", "mi"),
    ("or", "CONJ", "tàbí"), ("that", "REL", "tí"),
    ("who", "REL", "tí"), ("which", "REL", "tí"),
    ("when", "SUB", "nígbà tí"), ("if", "SUB", "bí"),
    ("although", "SUB", "bí ó tilẹ̀ jẹ́ pé"),
    ("after", "SUB", "lẹ́yìn tí"),
]

SUPPLEMENTAL_PRONOUNS: Dict[str, Dict[str, str | None]] = {
    "i": {"pos": "PRON", "subj": "mo", "obj": "mi"},
    "you": {"pos": "PRON", "subj": "o", "obj": "ẹ"},
    "he": {"pos": "PRON", "subj": "ó", "obj": None},
    "she": {"pos": "PRON", "subj": "ó", "obj": None},
    "it": {"pos": "PRON", "subj": "ó", "obj": None},
    "we": {"pos": "PRON", "subj": "a", "obj": "wa"},
    "you all": {"pos": "PRON", "subj": "ẹ", "obj": "yín"},
    "they": {"pos": "PRON", "subj": "wọ́n", "obj": "wọn"},
}

SUPPLEMENTAL_MARKERS = {
    "PROG": "ń", "PERF": "ti", "FUT": "máa", "FUT_2": "yóò",
    "FUT_3": "á", "QM": "ṣé", "QM_2": "ǹjẹ́", "HAB": "máa ń",
    "HAB_NEG": "kí ń",
}

# A descriptive inventory only.  The functions remain in the original
# notebooks, preserved under mt_model_resources/source_notebooks/.
SUPPLEMENTAL_RULES = {
    "analysis": ["contraction expansion", "verb-form recovery", "plural recovery",
                 "multiword matching", "pronoun-role assignment"],
    "transfer": ["habitual aspect", "predicate adjective", "aspect insertion",
                 "negation", "possessive ordering", "noun-phrase ordering",
                 "relative clauses", "conjunctions", "question marking"],
}


def build_supplemental_lexicon() -> Dict[str, Dict[str, str | None]]:
    """Return a fresh, NFC-normalised copy of the MT Model lexical data."""
    lexicon = {
        english: {"pos": pos, "yo": _nfc(yoruba)}
        for english, pos, yoruba in SUPPLEMENTAL_LEXICON
    }
    for english, forms in SUPPLEMENTAL_PRONOUNS.items():
        lexicon[english] = {
            "pos": forms["pos"],
            "subj": _nfc(forms["subj"]),
            "obj": _nfc(forms["obj"]) if forms["obj"] else None,
        }
    return lexicon


if __name__ == "__main__":
    print(f"{len(build_supplemental_lexicon())} supplemental MT entries loaded.")
