"""Linguistically structured English-Yorùbá transfer rules.

This module is data driven and safe to import from ``unified_pipeline.py``.
It does not invent lexical translations: lexical items must come from the
unified lexicon.  Its task is analysis, grammatical transfer and surface form.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class GrammarRule:
    identifier: str
    layer: str
    source_pattern: str
    target_structure: str
    condition: str
    example_en: str
    example_yo: str
    priority: int


# English analysis rules.  These identify structure before lexical transfer.
ENGLISH_STRUCTURED_RULES = (
    GrammarRule("EN.AUX.PROG", "english_morphosyntax", "SUBJ be V-ing", "SUBJ PROG V", "progressive event", "The children are playing.", "Àwọn ọmọdé ń ṣeré.", 10),
    GrammarRule("EN.AUX.PERF", "english_morphosyntax", "SUBJ have V-en", "SUBJ PERF V", "completed event", "I have finished.", "Mo ti parí.", 11),
    GrammarRule("EN.AUX.FUT", "english_morphosyntax", "SUBJ will V", "SUBJ FUT V", "future or intention", "I will study.", "Èmi yóò kàwé.", 12),
    GrammarRule("EN.NEG.DO", "english_morphosyntax", "do not V", "NEG.IMP V or SUBJ NEG V", "imperative versus declarative", "Do not cheat.", "Má ṣe jìbìtì.", 13),
    GrammarRule("EN.NP.ART", "english_np", "DET N", "N", "indefinite article has no direct Yorùbá counterpart", "a book", "ìwé", 20),
    GrammarRule("EN.NP.ADJ", "english_np", "ADJ N", "N ADJ", "adjective precedes noun in English", "new book", "ìwé tuntun", 21),
    GrammarRule("EN.NP.POSS", "english_np", "POSS N", "N POSS", "possessive pronoun is postnominal", "my book", "ìwé mi", 22),
    GrammarRule("EN.NP.DEM", "english_np", "DEM N", "N DEM", "demonstrative is postnominal", "this book", "ìwé yìí", 23),
    GrammarRule("EN.Q.WH", "english_clause", "WH AUX SUBJ VP", "WH + predicate", "content question", "Where is my bag?", "Níbo ni àpò mi wà?", 30),
    GrammarRule("EN.Q.POLAR", "english_clause", "AUX SUBJ VP?", "Ṣé + SUBJ VP?", "yes/no question", "Can you repeat that?", "Ṣé e lè tún sọ ọ́?", 31),
)

# Yorùbá analysis and generation rules.  Tags use UD-like names where useful.
YORUBA_STRUCTURED_RULES = (
    GrammarRule("YO.PHON.NFC", "phonology", "Unicode input", "NFC tone marked output", "always normalise before lookup", "ile eko", "ilé ẹ̀kọ́", 1),
    GrammarRule("YO.PHON.TONE", "phonology", "CV syllable", "H/M/L lexical tone", "never strip tone for final output", "ọkọ", "ọkọ́ / ọ̀kọ̀", 2),
    GrammarRule("YO.PHON.ELISION", "phonology", "V V across word boundary", "licensed contracted form", "apply only attested mappings", "tí ó", "tó", 3),
    GrammarRule("YO.MORPH.PROG", "morphology", "SUBJ + ń + V", "imperfective/progressive", "ongoing event", "We are learning.", "A ń kọ́ ẹ̀kọ́.", 10),
    GrammarRule("YO.MORPH.PERF", "morphology", "SUBJ + ti + V", "perfect/completed", "completed event", "I have finished.", "Mo ti parí.", 11),
    GrammarRule("YO.MORPH.FUT", "morphology", "SUBJ + yóò/máa + V", "future/intentive", "use lexical/register choice", "She will come.", "Ó yóò wá.", 12),
    GrammarRule("YO.MORPH.HAB", "morphology", "SUBJ + máa ń + V", "habitual", "recurrent event", "He reads every day.", "Ó máa ń kàwé lójoojúmọ́.", 13),
    GrammarRule("YO.MORPH.NEG", "morphology", "SUBJ + negation + V", "negative predicate", "select by aspect and person", "I do not know.", "Mi ò mọ̀.", 14),
    GrammarRule("YO.MORPH.PL", "morphology", "àwọn + N", "plural NP", "human and count-noun plural when required", "students", "àwọn akẹ́kọ̀ọ́", 15),
    GrammarRule("YO.NP.ADJ", "syntax", "N + ADJ", "postnominal adjective", "English adjective must be reordered", "clean classroom", "kíláàsì mọ́", 20),
    GrammarRule("YO.NP.POSS", "syntax", "N + POSS", "postnominal possessive", "possessor pronoun follows head", "your hand", "ọwọ́ rẹ", 21),
    GrammarRule("YO.NP.DEM", "syntax", "N + yìí/ìyẹn/náà", "postnominal demonstrative/definite", "do not place before noun", "that pen", "kálámù ìyẹn", 22),
    GrammarRule("YO.NP.ASSOC", "syntax", "N1 + N2", "associative/genitive compound", "head precedes modifier", "school book", "ìwé ilé ẹ̀kọ́", 23),
    GrammarRule("YO.CLAUSE.SVO", "syntax", "SUBJ V OBJ", "SVO", "default finite clause", "The teacher reads the book.", "Olùkọ́ ka ìwé náà.", 30),
    GrammarRule("YO.CLAUSE.PRED_ADJ", "syntax", "SUBJ ADJ", "adjectival predicate", "do not force a copula", "The school is big.", "Ilé ẹ̀kọ́ tóbi.", 31),
    GrammarRule("YO.CLAUSE.IDENT", "syntax", "NP1 ni NP2", "identificational clause", "classification/identity", "This is a book.", "Èyí ni ìwé.", 32),
    GrammarRule("YO.CLAUSE.LOC", "syntax", "SUBJ wà LOC", "locative/existential", "location or presence", "My bag is on the desk.", "Àpò mi wà lórí tébùrù.", 33),
    GrammarRule("YO.CLAUSE.SVC", "syntax", "SUBJ TAM V1 OBJ V2", "serial verb construction", "one TAM scope across the series", "Bring my book.", "Mú ìwé mi wá.", 34),
    GrammarRule("YO.CLAUSE.IMP", "syntax", "E + V", "polite/plural imperative", "classroom command", "Open your book.", "E ṣí ìwé yín.", 35),
    GrammarRule("YO.CLAUSE.QPOL", "syntax", "Ṣé + clause ?", "polar interrogative", "optional formal marker", "May I go?", "Ṣé mo lè lọ?", 40),
    GrammarRule("YO.CLAUSE.QWH", "syntax", "WH + ni + clause", "content interrogative", "select human/nonhuman question word", "What is this?", "Kín ni èyí?", 41),
    GrammarRule("YO.CLAUSE.REL", "syntax", "N + tí + clause", "relative clause", "relative marker follows antecedent", "the student who reads", "akẹ́kọ̀ọ́ tí ó ń kàwé", 42),
)


PRONOUNS = {"i": "mo", "you": "o", "he": "ó", "she": "ó", "it": "ó", "we": "a", "they": "wọ́n"}
POSSESSIVES = {"my": "mi", "your": "rẹ", "his": "rẹ̀", "her": "rẹ̀", "our": "wa", "their": "wọn"}
TAM = {"progressive": "ń", "perfect": "ti", "future": "yóò", "habitual": "máa ń", "ability": "lè", "obligation": "gbọ́dọ̀"}
QUESTION_WORDS = {"what": "kín", "who": "ta", "where": "níbo", "when": "nígbà wo", "why": "kí ló dé", "how": "báwo", "which": "èwo"}
ELISION = ((r"\btí\s+ó\b", "tó"), (r"\bkí\s+ó\b", "kó"), (r"\bbí\s+ó\b", "bó"), (r"\bní\s+ilé\b", "nílé"))


@dataclass
class ClausePlan:
    tokens: list[str]
    sentence_type: str = "declarative"
    aspect: str = "simple"
    polarity: str = "affirmative"
    rules: list[str] = field(default_factory=list)


def normalise_yoruba(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def apply_phonology(text: str) -> str:
    """Conservative surface cleanup. It never predicts missing lexical tones."""
    output = normalise_yoruba(re.sub(r"\s+", " ", text).strip())
    for pattern, replacement in ELISION:
        output = re.sub(pattern, replacement, output)
    return output


def analyse_english_clause(text: str) -> ClausePlan:
    words = re.findall(r"[A-Za-z']+|[?.!]", text.lower())
    plan = ClausePlan(words)
    if text.strip().endswith("?"):
        plan.sentence_type = "interrogative"
    elif words and words[0] in {"open", "close", "read", "write", "stand", "sit", "come", "go", "do", "stop", "bring", "take", "help"}:
        plan.sentence_type = "imperative"
    if any(word in {"am", "is", "are", "was", "were"} for word in words) and any(word.endswith("ing") for word in words):
        plan.aspect = "progressive"; plan.rules.append("EN.AUX.PROG")
    elif any(word in {"have", "has", "had"} for word in words):
        plan.aspect = "perfect"; plan.rules.append("EN.AUX.PERF")
    elif "will" in words:
        plan.aspect = "future"; plan.rules.append("EN.AUX.FUT")
    if "not" in words or "don't" in words or "cannot" in words:
        plan.polarity = "negative"; plan.rules.append("EN.NEG.DO")
    if plan.sentence_type == "interrogative":
        plan.rules.append("EN.Q.WH" if words and words[0] in QUESTION_WORDS else "EN.Q.POLAR")
    return plan


def build_yoruba_predicate(subject: str, verb: str, plan: ClausePlan, *, polite: bool = False) -> str:
    """Build a grammatical predicate from lexically translated subject and verb."""
    if plan.sentence_type == "imperative":
        return f"{'E ' if polite else ''}{'má ṣe ' if plan.polarity == 'negative' else ''}{verb}".strip()
    if plan.polarity == "negative":
        if subject == "mo": return f"mi ò {verb}"
        if plan.aspect == "perfect": return f"{subject} kò tíì {verb}"
        if plan.aspect == "future": return f"{subject} kì yóò {verb}"
        return f"{subject} kò {verb}"
    marker = TAM.get(plan.aspect, "")
    return " ".join(part for part in (subject, marker, verb) if part)


def rule_catalogue() -> list[dict[str, object]]:
    """Pipeline friendly serialization for diagnostics or a future rules API."""
    return [rule.__dict__.copy() for rule in sorted(ENGLISH_STRUCTURED_RULES + YORUBA_STRUCTURED_RULES, key=lambda item: (item.priority, item.identifier))]


def validate_rule_system() -> list[str]:
    """Fast non lexical regression checks for the rule layer."""
    failures = []
    if build_yoruba_predicate("mo", "kọ́", analyse_english_clause("I will learn.")) != "mo yóò kọ́": failures.append("future")
    if build_yoruba_predicate("mo", "mọ̀", ClausePlan([], polarity="negative")) != "mi ò mọ̀": failures.append("negative")
    if apply_phonology("tí ó wá") != "tó wá": failures.append("elision")
    return failures
