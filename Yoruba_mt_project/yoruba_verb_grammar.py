"""Verb lexeme forms, English auxiliary analysis, TAM and negation selection.

This is a constrained generation layer for Standard Yorùbá.  It separates
English auxiliary meanings from lexical verbs and records valency dependent
lexeme forms before phrase ordering occurs in the main pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class Valency(str, Enum):
    INTRANSITIVE = "intransitive"
    TRANSITIVE = "transitive"
    DITRANSITIVE = "ditransitive"
    AMBITRANSITIVE = "ambitransitive"
    SERIAL = "serial"
    SPLITTING = "splitting"


@dataclass(frozen=True)
class VerbForm:
    english_lemma: str
    yoruba_lemma: str
    valency: Valency
    object_required: bool = False
    objectless_form: str | None = None
    serial_tail: str | None = None
    notes: str = ""

    def surface(self, has_object: bool) -> str:
        """Select the lexical form only. TAM and negation are added elsewhere."""
        if not has_object and self.objectless_form:
            return self.objectless_form
        return self.yoruba_lemma


# The initial inventory prioritises verbs present in the education corpus.
# Additional entries can be added without changing the transfer engine.
VERB_LEXICON: dict[str, VerbForm] = {
    "eat": VerbForm("eat", "jẹ", Valency.AMBITRANSITIVE, objectless_form="jẹun", notes="jẹ takes a food object; jẹun is the conventional objectless 'eat/have a meal' form."),
    "drink": VerbForm("drink", "mu", Valency.AMBITRANSITIVE, notes="mu may occur with or without an overt object."),
    "read": VerbForm("read", "ka", Valency.TRANSITIVE, object_required=True),
    "study": VerbForm("study", "kàwé", Valency.INTRANSITIVE, notes="kàwé is a lexicalised study/read form; use kọ́ ẹ̀kọ́ where the object is a taught subject."),
    "learn": VerbForm("learn", "kọ́", Valency.TRANSITIVE, object_required=True),
    "teach": VerbForm("teach", "kọ́", Valency.DITRANSITIVE, object_required=True),
    "write": VerbForm("write", "kọ", Valency.TRANSITIVE, object_required=True),
    "go": VerbForm("go", "lọ", Valency.INTRANSITIVE),
    "come": VerbForm("come", "wá", Valency.INTRANSITIVE),
    "bring": VerbForm("bring", "mú", Valency.SERIAL, object_required=True, serial_tail="wá", notes="mú X wá, literally take X come."),
    "take": VerbForm("take", "mú", Valency.TRANSITIVE, object_required=True),
    "give": VerbForm("give", "fún", Valency.DITRANSITIVE, object_required=True),
    "help": VerbForm("help", "ràn", Valency.SERIAL, object_required=True, serial_tail="lọ́wọ́", notes="ràn NP lọ́wọ́."),
    "look": VerbForm("look", "wo", Valency.AMBITRANSITIVE),
    "see": VerbForm("see", "rí", Valency.TRANSITIVE, object_required=True),
    "know": VerbForm("know", "mọ̀", Valency.TRANSITIVE, object_required=True),
    "understand": VerbForm("understand", "yé", Valency.SPLITTING, notes="yé NP; idiomatic comprehension may use ó yé mi."),
    "finish": VerbForm("finish", "parí", Valency.AMBITRANSITIVE),
    "open": VerbForm("open", "ṣí", Valency.TRANSITIVE, object_required=True),
    "close": VerbForm("close", "pa", Valency.TRANSITIVE, object_required=True),
    "play": VerbForm("play", "ṣeré", Valency.INTRANSITIVE),
    "sleep": VerbForm("sleep", "sùn", Valency.INTRANSITIVE),
    "work": VerbForm("work", "ṣiṣẹ́", Valency.INTRANSITIVE),
    "speak": VerbForm("speak", "sọ̀rọ̀", Valency.INTRANSITIVE),
    "say": VerbForm("say", "sọ", Valency.TRANSITIVE, object_required=True),
    "have_possession": VerbForm("have_possession", "ní", Valency.TRANSITIVE, object_required=True, notes="lexical have/possess, not the English perfect auxiliary."),
}


@dataclass(frozen=True)
class AuxiliaryAnalysis:
    english_form: str
    function: str
    yoruba_strategy: str
    example_en: str
    example_yo: str


ENGLISH_AUXILIARIES = (
    AuxiliaryAnalysis("am/is/are/be", "copula", "choose predicate type: ni for identification, wà for location/existence, zero with many adjectival predicates", "The school is big.", "Ilé ẹ̀kọ́ tóbi."),
    AuxiliaryAnalysis("am/is/are + V-ing", "progressive", "SUBJ + ń + V", "She is reading.", "Ó ń ka ìwé."),
    AuxiliaryAnalysis("was/were", "past copula", "usually zero-marked with time context or a lexical predicate; do not mechanically add jẹ́", "The teacher was here yesterday.", "Olùkọ́ wà níbí lánàá."),
    AuxiliaryAnalysis("have/has/had + V-en", "perfect", "SUBJ + ti + V", "I have finished.", "Mo ti parí."),
    AuxiliaryAnalysis("have/has", "possession", "SUBJ + ní + OBJ", "She has a pen.", "Ó ní kálámù."),
    AuxiliaryAnalysis("will/shall", "future", "SUBJ + yóò or máa + V", "They will come.", "Wọ́n yóò wá."),
    AuxiliaryAnalysis("can/may", "ability or permission", "SUBJ + lè + V", "May I go?", "Ṣé mo lè lọ?"),
    AuxiliaryAnalysis("must", "obligation", "SUBJ + gbọ́dọ̀ + V", "You must study.", "O gbọ́dọ̀ kàwé."),
    AuxiliaryAnalysis("do/does/did", "do support", "no lexical counterpart in affirmative clauses; choose negation or emphasis construction", "Do not copy.", "Má ṣe dá iṣẹ́ ẹlòmíràn kọ."),
)


@dataclass(frozen=True)
class NegativeRule:
    key: str
    marker: str
    environment: str
    example_en: str
    example_yo: str


# These forms deliberately distinguish Standard Yorùbá grammatical contexts.
NEGATION_RULES = (
    NegativeRule("indicative", "kò", "general non-habitual negative, especially 3sg or subjectless context", "He did not come.", "Kò wá."),
    NegativeRule("pronoun_contracted", "ò", "after overt pronouns in common speech and writing: mi ò, o ò, a ò, ẹ ò, wọ́n ò", "I do not know.", "Mi ò mọ̀."),
    NegativeRule("progressive", "kì í", "negative continuous construction in the selected Standard Yorùbá analysis", "She is not reading.", "Kì í kàwé."),
    NegativeRule("habitual", "kì í", "negative habitual or general disposition", "He does not usually eat meat.", "Kì í jẹ ẹran."),
    NegativeRule("perfect_not_yet", "kò tíì / ò tíì", "perfect negative meaning 'has/have not yet'", "I have not finished yet.", "Mi ò tíì parí."),
    NegativeRule("future", "kì yóò", "future negative", "She will not come.", "Kì yóò wá."),
    NegativeRule("imperative", "má", "negative command with a simple verb", "Do not go.", "Má lọ."),
    NegativeRule("imperative_serial", "má ṣe", "negative command, especially complex or serial predicate", "Do not cheat.", "Má ṣe jìbìtì."),
)


def resolve_verb(english_lemma: str, *, has_object: bool = False) -> tuple[str, str | None]:
    """Return selected Yorùbá lexical verb and optional serial tail."""
    record = VERB_LEXICON.get(english_lemma.lower())
    if not record:
        return "", None
    return record.surface(has_object), record.serial_tail


def choose_negator(*, subject: str = "", aspect: str = "simple", sentence_type: str = "declarative", complex_predicate: bool = False) -> str:
    """Select a negative marker without collapsing distinct constructions."""
    if sentence_type == "imperative":
        return "má ṣe" if complex_predicate else "má"
    if aspect in {"habitual", "progressive"}:
        return "kì í"
    if aspect == "perfect":
        return "ò tíì" if subject in {"mo", "o", "a", "ẹ", "wọ́n"} else "kò tíì"
    if aspect == "future":
        return "kì yóò"
    return "ò" if subject in {"mo", "o", "a", "ẹ", "wọ́n"} else "kò"


def realise_predicate(subject: str, verb: str, *, aspect: str = "simple", negative: bool = False, sentence_type: str = "declarative", complex_predicate: bool = False) -> str:
    """Realise a predicate after lexical transfer and before surface phonology."""
    if negative:
        negator = choose_negator(subject=subject, aspect=aspect, sentence_type=sentence_type, complex_predicate=complex_predicate)
        if sentence_type == "imperative":
            return f"{negator} {verb}"
        if negator == "ò":
            return f"{'mi' if subject == 'mo' else subject} ò {verb}".strip()
        negative_subject = "" if subject == "ó" else subject
        if subject == "mo" and negator.startswith("ò"):
            negative_subject = "mi"
        return " ".join(filter(None, (negative_subject, negator, verb)))
    markers = {"progressive": "ń", "perfect": "ti", "future": "yóò", "habitual": "máa ń", "ability": "lè", "obligation": "gbọ́dọ̀"}
    return " ".join(part for part in (subject, markers.get(aspect, ""), verb) if part)


def validate_verb_grammar() -> list[str]:
    failures = []
    if resolve_verb("eat", has_object=True)[0] != "jẹ": failures.append("transitive_jẹ")
    if resolve_verb("eat", has_object=False)[0] != "jẹun": failures.append("intransitive_jẹun")
    if choose_negator(subject="mo", aspect="perfect") != "ò tíì": failures.append("perfect_negative")
    if choose_negator(aspect="habitual") != "kì í": failures.append("habitual_negative")
    if realise_predicate("mo", "parí", aspect="perfect", negative=True) != "mi ò tíì parí": failures.append("predicate_realisation")
    return failures
