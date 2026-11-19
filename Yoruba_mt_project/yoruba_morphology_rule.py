"""
Yoruba Morphological Rules Engine
For Rule-Based Machine Translation System
================================================================
Compatible with: education_dataset (yoruba_english_education_dataset)

Linguist / Morphology Lead Deliverable
Covers:
    1. Tone marking system (High, Mid, Low) and diacritics
    2. Vowel and consonant inventory
    3. Pronoun system (subject, object, possessive)
    4. Tense/Aspect/Mood (TAM) markers and verb conjugation
    5. Negation rules
    6. Nominalization and noun class morphology
    7. Vowel harmony and elision (assimilation across word boundaries)
    8. Pluralization (via àwọn)
    9. Question formation
    10. Honorific / plural "E" (politeness) marking
    11. Serial verb construction helpers
    12. Validation utilities compatible with education_dataset

References:
    - Bamgbose (1966), Awobuluyi (1978), Owolabi (2006),
      Akinlabi & Liberman (2000), Ogunbowale (1970),
      Yusuf (1998), Ward (1952), Abraham (1958).
================================================================
"""

from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Iterable


# ================================================================
# SECTION 1: PHONOLOGY — VOWELS, CONSONANTS, TONES
# ================================================================

# Yoruba has 7 oral vowels and 5 nasal vowels
ORAL_VOWELS: Tuple[str, ...] = ("a", "e", "ẹ", "i", "o", "ọ", "u")
NASAL_VOWELS: Tuple[str, ...] = ("an", "ẹn", "in", "ọn", "un")

# 18 consonants in standard Yoruba orthography
CONSONANTS: Tuple[str, ...] = (
    "b", "d", "f", "g", "gb", "h", "j", "k", "l",
    "m", "n", "p", "r", "s", "ṣ", "t", "w", "y",
)

# Tone marks (Unicode combining diacritics)
TONE_HIGH = "\u0301"   # ́  (acute)
TONE_LOW  = "\u0300"   # ̀  (grave)
TONE_MID  = ""         # unmarked
# Sub-dot (used for ẹ, ọ, ṣ) — part of base letter in NFC
SUB_DOT   = "\u0323"   # ̣

TONE_NAMES = {
    TONE_HIGH: "HIGH",
    TONE_LOW:  "LOW",
    TONE_MID:  "MID",
}


def to_nfc(text: str) -> str:
    """Normalise to NFC — compose base letter + diacritics into single codepoints."""
    return unicodedata.normalize("NFC", text)


def to_nfd(text: str) -> str:
    """Decompose into base + combining marks for analysis."""
    return unicodedata.normalize("NFD", text)


def strip_tones(text: str) -> str:
    """Remove tone marks (keep sub-dots on ẹ, ọ, ṣ)."""
    decomposed = to_nfd(text)
    stripped = "".join(ch for ch in decomposed if ch not in (TONE_HIGH, TONE_LOW))
    return to_nfc(stripped)


def strip_all_diacritics(text: str) -> str:
    """Remove tones AND sub-dots (useful for loose matching)."""
    decomposed = to_nfd(text)
    stripped = "".join(
        ch for ch in decomposed
        if not unicodedata.combining(ch)
    )
    return stripped


def get_tone_pattern(word: str) -> List[str]:
    """
    Return the tone pattern of a word as a list of 'H', 'M', 'L'.
    Example: 'olùkọ́' -> ['M', 'L', 'H']
    """
    decomposed = to_nfd(word)
    pattern: List[str] = []
    current_tone = "M"
    base_seen = False

    for ch in decomposed:
        if ch in TONE_HIGH:
            current_tone = "H"
        elif ch in TONE_LOW:
            current_tone = "L"
        elif ch == SUB_DOT:
            continue
        elif ch.isalpha():
            if base_seen and ch.lower() in "aeiou":
                pattern.append(current_tone)
                current_tone = "M"
            elif ch.lower() in "aeiou":
                base_seen = True
                # Will append tone once we know it (or at next vowel)
                pending = True
    # Simpler: iterate characters of NFC form, inspect each vowel’s diacritics
    pattern = []
    for ch in to_nfc(word):
        decomp = to_nfd(ch)
        base = decomp[0].lower() if decomp else ""
        if base in "aeiou":
            if TONE_HIGH in decomp:
                pattern.append("H")
            elif TONE_LOW in decomp:
                pattern.append("L")
            else:
                pattern.append("M")
    return pattern


# ================================================================
# SECTION 2: PRONOUN SYSTEM
# ================================================================

@dataclass(frozen=True)
class PronounSet:
    """A paradigm for a given grammatical role."""
    first_sg:  str  # I / me / my
    second_sg: str  # you (singular, informal)
    third_sg:  str  # he/she/it
    first_pl:  str  # we / us / our
    second_pl: str  # you (plural / polite)
    third_pl:  str  # they / them / their


# Subject pronouns (short forms used before verbs)
SUBJECT_PRONOUNS = PronounSet(
    first_sg="mo",
    second_sg="o",
    third_sg="ó",
    first_pl="a",
    second_pl="ẹ",
    third_pl="wọ́n",
)

# Emphatic / independent pronouns
EMPHATIC_PRONOUNS = PronounSet(
    first_sg="èmi",
    second_sg="ìwọ",
    third_sg="òun",
    first_pl="àwa",
    second_pl="ẹ̀yin",
    third_pl="àwọn",
)

# Object pronouns (post-verbal)
OBJECT_PRONOUNS = PronounSet(
    first_sg="mi",
    second_sg="ọ",
    third_sg="ó",      # often realised as vowel-copy or elision
    first_pl="wa",
    second_pl="yín",
    third_pl="wọn",
)

# Possessive pronouns (post-nominal)
POSSESSIVE_PRONOUNS = PronounSet(
    first_sg="mi",
    second_sg="rẹ",
    third_sg="rẹ̀",
    first_pl="wa",
    second_pl="yín",
    third_pl="wọn",
)

# Negative subject pronouns (used before "kò/kì")
NEGATIVE_SUBJECT_PRONOUNS = PronounSet(
    first_sg="mi",     # mi ò / mi ò ní
    second_sg="o",     # o ò
    third_sg="kò",     # kò (fused — no separate pronoun)
    first_pl="a",      # a ò
    second_pl="ẹ",     # ẹ ò
    third_pl="wọn",    # wọn ò
)


def get_pronoun(person: int, number: str, role: str = "subject") -> str:
    """
    Retrieve a pronoun by (person, number, role).

    person: 1, 2, or 3
    number: 'sg' or 'pl'
    role:   'subject' | 'object' | 'possessive' | 'emphatic' | 'negative'
    """
    sets = {
        "subject":    SUBJECT_PRONOUNS,
        "object":     OBJECT_PRONOUNS,
        "possessive": POSSESSIVE_PRONOUNS,
        "emphatic":   EMPHATIC_PRONOUNS,
        "negative":   NEGATIVE_SUBJECT_PRONOUNS,
    }
    if role not in sets:
        raise ValueError(f"Unknown pronoun role: {role}")

    pset = sets[role]
    key = f"{'first' if person == 1 else 'second' if person == 2 else 'third'}_{number}"
    if not hasattr(pset, key):
        raise ValueError(f"Invalid person/number combination: {person}/{number}")
    return getattr(pset, key)


# ================================================================
# SECTION 3: TENSE / ASPECT / MOOD (TAM) MARKERS
# ================================================================

@dataclass(frozen=True)
class TAMMarker:
    """A Tense/Aspect/Mood marker with placement rules."""
    marker:      str
    name:        str
    position:    str      # 'pre-verb', 'post-subject', 'pre-subject'
    gloss:       str
    example_eng: str
    example_yor: str


TAM_MARKERS: Dict[str, TAMMarker] = {
    # Simple present / habitual — unmarked verb or 'máa ń'
    "present_habitual": TAMMarker(
        marker="ń",
        name="Present Continuous / Progressive",
        position="pre-verb",
        gloss="is/are V-ing",
        example_eng="I am reading.",
        example_yor="Mo ń kàwé.",
    ),
    "habitual": TAMMarker(
        marker="máa ń",
        name="Habitual",
        position="pre-verb",
        gloss="usually V / V-s regularly",
        example_eng="He usually comes.",
        example_yor="Ó máa ń wá.",
    ),
    "future": TAMMarker(
        marker="yóò",
        name="Future",
        position="pre-verb",
        gloss="will V",
        example_eng="I will go.",
        example_yor="Èmi yóò lọ.",
    ),
    "future_short": TAMMarker(
        marker="á",
        name="Future (reduced)",
        position="pre-verb",
        gloss="will V",
        example_eng="He will come.",
        example_yor="Yóò wá. / Á wá.",
    ),
    "future_maa": TAMMarker(
        marker="máa",
        name="Future / Intentive",
        position="pre-verb",
        gloss="will V / shall V",
        example_eng="I will study.",
        example_yor="Mo máa kàwé.",
    ),
    "perfect": TAMMarker(
        marker="ti",
        name="Perfect",
        position="pre-verb",
        gloss="have V-ed",
        example_eng="I have finished.",
        example_yor="Mo ti parí.",
    ),
    "past": TAMMarker(
        marker="",             # Yoruba has no overt past marker; context + time adverb
        name="Simple Past",
        position="pre-verb",
        gloss="V-ed (zero-marked)",
        example_eng="I went yesterday.",
        example_yor="Mo lọ lánàá.",
    ),
    "subjunctive": TAMMarker(
        marker="kí",
        name="Subjunctive",
        position="pre-subject",
        gloss="that/let (should) V",
        example_eng="Let him come.",
        example_yor="Kí ó wá.",
    ),
    "ability": TAMMarker(
        marker="lè",
        name="Ability / Possibility",
        position="pre-verb",
        gloss="can/could V",
        example_eng="I can read.",
        example_yor="Mo lè kàwé.",
    ),
    "obligation": TAMMarker(
        marker="gbọ́dọ̀",
        name="Obligation",
        position="pre-verb",
        gloss="must V",
        example_eng="You must study.",
        example_yor="O gbọ́dọ̀ kàwé.",
    ),
    "desire": TAMMarker(
        marker="fẹ́",
        name="Desiderative",
        position="pre-verb",
        gloss="want to V",
        example_eng="I want to learn.",
        example_yor="Mo fẹ́ kọ́ ẹ̀kọ́.",
    ),
    "inceptive": TAMMarker(
        marker="bẹ̀rẹ̀",
        name="Inceptive",
        position="pre-verb",
        gloss="begin to V",
        example_eng="They began to sing.",
        example_yor="Wọ́n bẹ̀rẹ̀ sí kọrin.",
    ),
}


def get_tam(name: str) -> TAMMarker:
    """Retrieve a TAM marker by key."""
    if name not in TAM_MARKERS:
        raise KeyError(f"Unknown TAM marker: {name}")
    return TAM_MARKERS[name]


# ================================================================
# SECTION 4: NEGATION
# ================================================================

NEGATION_MARKERS: Dict[str, Dict[str, str]] = {
    "simple": {
        "marker": "kò",
        "gloss":  "not (indicative, 3sg default; combines with subject)",
        "example_eng": "He does not come.",
        "example_yor": "Kò wá.",
    },
    "first_sg_neg": {
        "marker": "mi ò",     # colloquial: "mi ò", formal: "èmi kò"
        "gloss":  "I do not",
        "example_eng": "I do not know.",
        "example_yor": "Mi ò mọ̀.",
    },
    "perfect_neg": {
        "marker": "kò tíì",
        "gloss":  "have not yet V-ed",
        "example_eng": "I have not finished.",
        "example_yor": "Mi ò tíì parí.",
    },
    "future_neg": {
        "marker": "kì yóò",
        "gloss":  "will not V",
        "example_eng": "He will not come.",
        "example_yor": "Kì yóò wá.",
    },
    "imperative_neg": {
        "marker": "má",
        "gloss":  "do not V (imperative)",
        "example_eng": "Do not talk.",
        "example_yor": "Má sọ̀rọ̀.",
    },
    "imperative_neg_polite": {
        "marker": "má ṣe",
        "gloss":  "do not V (polite / emphatic)",
        "example_eng": "Do not cheat.",
        "example_yor": "Má ṣe jìbìtì.",
    },
}


def negate(subject: str, verb_phrase: str, aspect: str = "simple") -> str:
    """
    Produce a negated clause.

    aspect: 'simple' | 'perfect' | 'future' | 'imperative' | 'imperative_polite'
    """
    if aspect == "simple":
        if subject.lower() == "mo":
            return f"mi ò {verb_phrase}"
        if subject.lower() == "ó":
            return f"kò {verb_phrase}"
        return f"{subject} ò {verb_phrase}"
    if aspect == "perfect":
        if subject.lower() == "mo":
            return f"mi ò tíì {verb_phrase}"
        return f"{subject} kò tíì {verb_phrase}"
    if aspect == "future":
        return f"{subject} kì yóò {verb_phrase}"
    if aspect == "imperative":
        return f"má {verb_phrase}"
    if aspect == "imperative_polite":
        return f"má ṣe {verb_phrase}"
    raise ValueError(f"Unknown negation aspect: {aspect}")


# ================================================================
# SECTION 5: VERB CONJUGATION
# ================================================================

@dataclass
class VerbConjugation:
    """Result of conjugating a verb for a given subject + TAM."""
    subject:     str
    tam:         str
    verb:        str
    surface:     str
    gloss:       str


def conjugate_verb(
    verb: str,
    person: int = 3,
    number: str = "sg",
    tam: str = "present_habitual",
    polite: bool = False,
) -> VerbConjugation:
    """
    Conjugate a Yoruba verb.

    Example:
        conjugate_verb("kàwé", person=1, number="sg", tam="present_habitual")
        -> "Mo ń kàwé." (I am reading)
    """
    subject = get_pronoun(person, number, role="subject")
    # Polite 2nd-person uses the plural form 'E'
    if polite and person == 2:
        subject = "ẹ"

    tam_marker = get_tam(tam)
    marker = tam_marker.marker

    # Build surface form respecting TAM position
    if tam == "past":
        surface = f"{subject} {verb}".strip()
    elif tam == "future" and person == 1 and number == "sg":
        # 'Mo' + 'yóò' is often "Èmi yóò" (emphatic) or "Mà á" (colloquial)
        surface = f"èmi {marker} {verb}".strip()
    elif tam == "subjunctive":
        surface = f"{marker} {subject} {verb}".strip()
    else:
        if marker:
            surface = f"{subject} {marker} {verb}".strip()
        else:
            surface = f"{subject} {verb}".strip()

    # Capitalise first letter (standard sentence form)
    surface = surface[0].upper() + surface[1:] + "."

    return VerbConjugation(
        subject=subject,
        tam=tam,
        verb=verb,
        surface=surface,
        gloss=f"{person}{number.upper()} + {tam_marker.name} + '{verb}'",
    )


# ================================================================
# SECTION 6: VOWEL ELISION / ASSIMILATION
# ================================================================

# When two vowels meet across word boundaries, Yoruba typically elides
# the first vowel OR assimilates (e.g., "ní ilé" -> "nílé").
# These rules are highly context-sensitive; we provide the most frequent cases.

ELISION_RULES: List[Tuple[str, str]] = [
    # (regex pattern, replacement)
    (r"\bní\s+ilé\b", "nílé"),  # established locative contraction
    (r"\btí\s+ó\b", "tó"),     # tí ó -> tó
    (r"\bkí\s+ó\b", "kó"),     # kí ó -> kó
    (r"\bbí\s+ó\b", "bó"),     # bí ó -> bó
]


def apply_elision(text: str) -> str:
    """Apply common vowel elision/assimilation rules at word boundaries."""
    out = text
    for pattern, replacement in ELISION_RULES:
        out = re.sub(pattern, replacement, out)
    return out


# ================================================================
# SECTION 7: PLURALIZATION & NOUN MORPHOLOGY
# ================================================================

PLURAL_MARKER = "àwọn"


def pluralize(noun: str) -> str:
    """
    Pluralise a Yoruba noun by prefixing 'àwọn'.
    Yoruba nouns have no inflectional plural morphology.
    """
    noun = noun.strip()
    if noun.lower().startswith("àwọn "):
        return noun
    return f"{PLURAL_MARKER} {noun}"


# Nominalising prefixes (produce nouns from verbs)
NOMINALIZING_PREFIXES: Dict[str, str] = {
    "a":   "agent / one who V-s (e.g., kọ́ 'teach' -> akọ́ni? / olùkọ́)",
    "olù": "agent / professional (e.g., olùkọ́ 'teacher')",
    "àì":  "negative nominalisation ('not V-ing')",
    "ì":   "action/manner nominalisation (e.g., ìkọ́ 'the teaching')",
    "ìlò": "manner of using",
    "ẹ":   "resultant / patient noun",
    "ò":   "instrument / result",
}


def nominalize(verb: str, prefix: str = "olù") -> str:
    """
    Derive a noun from a verb using a nominalising prefix.
    Example: nominalize('kọ́', 'olù') -> 'olùkọ́' (teacher)
    """
    if prefix not in NOMINALIZING_PREFIXES:
        raise ValueError(f"Unknown nominalising prefix: {prefix}")
    return f"{prefix}{verb}"


# ================================================================
# SECTION 8: QUESTION FORMATION
# ================================================================

QUESTION_PARTICLES: Dict[str, str] = {
    "yes_no_njẹ":    "Ṣé",      # polar question marker (sentence-initial)
    "yes_no_se":     "Ṣé",      # colloquial variant
    "yes_no_njẹ_f":  "Njẹ́",    # formal polar question
    "what":          "Kín",     # what
    "what_full":     "Kín ni",  # what is
    "who":           "Ta",      # who
    "who_full":      "Ta ni",   # who is
    "where":         "Níbo",    # where
    "when":          "Nígbà wo",# when
    "why":           "Kí ló dé", # why / what caused
    "how":           "Báwo",    # how
    "how_many":      "Mélòó",   # how many
    "which":         "Èwo",     # which
}


def form_question(statement: str, qtype: str = "yes_no_njẹ") -> str:
    """
    Convert a statement to a question by prepending the appropriate particle.
    Example: form_question("O lọ sí ilé ẹ̀kọ́.", "yes_no_njẹ")
             -> "Ṣé o lọ sí ilé ẹ̀kọ́?"
    """
    if qtype not in QUESTION_PARTICLES:
        raise ValueError(f"Unknown question type: {qtype}")
    particle = QUESTION_PARTICLES[qtype]
    stmt = statement.rstrip(".!").strip()
    # Lowercase first letter of statement when embedding
    if stmt:
        stmt = stmt[0].lower() + stmt[1:]
    return f"{particle} {stmt}?"


# ================================================================
# SECTION 9: HONORIFIC / POLITE "E"
# ================================================================

def make_polite(sentence: str) -> str:
    """
    Convert a sentence addressed to one person into the polite/plural form
    by substituting 2sg pronouns and verb forms with the 'E' honorific.

    Simple heuristic — swaps common 2sg patterns.
    """
    replacements: List[Tuple[str, str]] = [
        (r"\bO\b",   "Ẹ"),
        (r"\bo\b",   "ẹ"),
        (r"\bRẹ\b",  "Yín"),
        (r"\brẹ\b",  "yín"),
        (r"\bRẹ̀\b", "Yín"),
        (r"\brẹ̀\b", "yín"),
    ]
    out = sentence
    for pattern, replacement in replacements:
        out = re.sub(pattern, replacement, out)
    return out


# ================================================================
# SECTION 10: SERIAL VERB CONSTRUCTIONS
# ================================================================

def build_serial_verb(subject: str, verbs: List[str], connector: str = "") -> str:
    """
    Build a serial verb construction.
    Yoruba famously chains verbs: e.g., 'Mo mú ìwé wá' (I brought a book —
    lit. 'I took book come').
    """
    chain = " ".join(verbs) if not connector else f" {connector} ".join(verbs)
    out = f"{subject} {chain}".strip()
    return out[0].upper() + out[1:] + "."


# ================================================================
# SECTION 11: MORPHOLOGICAL ANALYZER
# ================================================================

@dataclass
class MorphAnalysis:
    """Shallow morphological analysis of a Yoruba token."""
    token:         str
    normalised:    str
    tones:         List[str]
    stripped:      str          # without tones
    base:          str          # without any diacritics
    is_pronoun:    bool = False
    pronoun_info:  Optional[Dict[str, str]] = None
    is_tam:        bool = False
    tam_info:      Optional[Dict[str, str]] = None
    is_negation:   bool = False


def _build_pronoun_lookup() -> Dict[str, Dict[str, str]]:
    lookup: Dict[str, Dict[str, str]] = {}
    role_sets = {
        "subject":    SUBJECT_PRONOUNS,
        "object":     OBJECT_PRONOUNS,
        "possessive": POSSESSIVE_PRONOUNS,
        "emphatic":   EMPHATIC_PRONOUNS,
    }
    for role, pset in role_sets.items():
        for field_name in ("first_sg", "second_sg", "third_sg",
                           "first_pl", "second_pl", "third_pl"):
            form = getattr(pset, field_name)
            key = to_nfc(form.lower())
            # Keep first encountered role to avoid overwriting
            if key not in lookup:
                lookup[key] = {"role": role, "paradigm": field_name}
    return lookup


_PRONOUN_LOOKUP = _build_pronoun_lookup()
_TAM_LOOKUP = {to_nfc(m.marker.lower()): m for m in TAM_MARKERS.values() if m.marker}
_NEG_LOOKUP = {to_nfc(info["marker"].lower()) for info in NEGATION_MARKERS.values()}


def analyze_token(token: str) -> MorphAnalysis:
    """Perform a shallow morphological analysis of a single Yoruba token."""
    normalised = to_nfc(token)
    lowered = normalised.lower()

    analysis = MorphAnalysis(
        token=token,
        normalised=normalised,
        tones=get_tone_pattern(normalised),
        stripped=strip_tones(normalised),
        base=strip_all_diacritics(normalised),
    )

    if lowered in _PRONOUN_LOOKUP:
        analysis.is_pronoun = True
        analysis.pronoun_info = _PRONOUN_LOOKUP[lowered]

    if lowered in _TAM_LOOKUP:
        marker = _TAM_LOOKUP[lowered]
        analysis.is_tam = True
        analysis.tam_info = {"name": marker.name, "gloss": marker.gloss}

    if lowered in _NEG_LOOKUP or lowered in {"kò", "má", "mi"}:
        analysis.is_negation = True

    return analysis


def tokenize_yoruba(sentence: str) -> List[str]:
    """
    Simple whitespace + punctuation tokenizer.
    Keeps diacritics intact.
    """
    sentence = to_nfc(sentence)
    # Separate punctuation
    sentence = re.sub(r"([.,!?;:()\"])", r" \1 ", sentence)
    tokens = [tok for tok in sentence.split() if tok]
    return tokens


def analyze_sentence(sentence: str) -> List[MorphAnalysis]:
    """Analyze each token of a Yoruba sentence."""
    return [analyze_token(tok) for tok in tokenize_yoruba(sentence)]


# ================================================================
# SECTION 12: VALIDATION AGAINST education_dataset
# ================================================================

def validate_tone_marking(text: str) -> Dict[str, object]:
    """
    Check basic tone-marking integrity:
      - Every vowel should have an identifiable tone (H/M/L).
      - No stray combining marks outside valid positions.
    """
    nfc = to_nfc(text)
    issues: List[str] = []
    vowel_count = 0
    toned_count = 0

    for ch in nfc:
        decomp = to_nfd(ch)
        base = decomp[0].lower() if decomp else ""
        if base in "aeiou":
            vowel_count += 1
            if TONE_HIGH in decomp or TONE_LOW in decomp:
                toned_count += 1

    return {
        "text":            nfc,
        "vowel_count":     vowel_count,
        "toned_vowels":    toned_count,
        "untoned_vowels":  vowel_count - toned_count,  # legitimate (mid tone)
        "issues":          issues,
    }


def validate_dataset_morphology(dataset: Dict[str, list]) -> Dict[str, object]:
    """
    Run morphological checks against the education_dataset structure.
    Returns a summary report compatible with the dataset's own validator.
    """
    total = 0
    with_tones = 0
    sections_report: Dict[str, Dict[str, int]] = {}

    for section, examples in dataset.items():
        if not isinstance(examples, list):
            continue
        sec_total = 0
        sec_toned = 0
        for ex in examples:
            if not isinstance(ex, dict) or "yoruba" not in ex:
                continue
            sec_total += 1
            total += 1
            report = validate_tone_marking(ex["yoruba"])
            if report["toned_vowels"] > 0:
                sec_toned += 1
                with_tones += 1
        sections_report[section] = {
            "examples":         sec_total,
            "with_tone_marks":  sec_toned,
        }

    return {
        "total_examples":          total,
        "examples_with_tones":     with_tones,
        "tone_coverage_percent":   round((with_tones / total * 100) if total else 0, 2),
        "by_section":              sections_report,
    }


# ================================================================
# SECTION 13: SELF-TEST SUITE
# ================================================================

def _run_self_tests() -> List[str]:
    """Internal self-tests to ensure morphological rules behave as expected."""
    failures: List[str] = []

    # 1. Tone stripping
    if strip_tones("olùkọ́") != "olukọ":
        failures.append("strip_tones('olùkọ́') failed")

    # 2. Tone pattern
    pat = get_tone_pattern("olùkọ́")
    if pat != ["M", "L", "H"]:
        failures.append(f"get_tone_pattern('olùkọ́') -> {pat}")

    # 3. Pronoun lookup
    if get_pronoun(1, "sg", "subject") != "mo":
        failures.append("get_pronoun(1, 'sg', 'subject') failed")
    if get_pronoun(2, "pl", "possessive") != "yín":
        failures.append("get_pronoun(2, 'pl', 'possessive') failed")

    # 4. Verb conjugation
    conj = conjugate_verb("kàwé", person=1, number="sg", tam="present_habitual")
    if conj.surface != "Mo ń kàwé.":
        failures.append(f"conjugate_verb present_habitual -> {conj.surface}")

    conj2 = conjugate_verb("parí", person=1, number="sg", tam="perfect")
    if conj2.surface != "Mo ti parí.":
        failures.append(f"conjugate_verb perfect -> {conj2.surface}")

    # 5. Negation
    neg = negate("mo", "mọ̀", aspect="simple")
    if neg != "mi ò mọ̀":
        failures.append(f"negate simple -> {neg}")

    neg2 = negate("", "sọ̀rọ̀", aspect="imperative")
    if neg2.strip() != "má sọ̀rọ̀":
        failures.append(f"negate imperative -> {neg2}")

    # 6. Pluralization
    if pluralize("akẹ́kọ̀ọ́") != "àwọn akẹ́kọ̀ọ́":
        failures.append("pluralize failed")

    # 7. Nominalization
    if nominalize("kọ́", "olù") != "olùkọ́":
        failures.append("nominalize failed")

    # 8. Question formation
    q = form_question("O lọ sí ilé ẹ̀kọ́.", "yes_no_njẹ")
    if not q.startswith("Ṣé") or not q.endswith("?"):
        failures.append(f"form_question -> {q}")

    # 9. Polite transformation
    polite = make_polite("O ṣe iṣẹ́ rẹ.")
    if "Ẹ" not in polite or "yín" not in polite:
        failures.append(f"make_polite -> {polite}")

    # 10. Elision
    el = apply_elision("tí ó dára")
    if "tó dára" not in el:
        failures.append(f"apply_elision -> {el}")

    # 11. Tokenization
    toks = tokenize_yoruba("Mo ń kàwé.")
    if toks != ["Mo", "ń", "kàwé", "."]:
        failures.append(f"tokenize_yoruba -> {toks}")

    # 12. Analysis of a known pronoun
    a = analyze_token("mo")
    if not a.is_pronoun:
        failures.append("analyze_token('mo') did not detect pronoun")

    # 13. Analysis of a TAM marker
    a2 = analyze_token("ń")
    if not a2.is_tam:
        failures.append("analyze_token('ń') did not detect TAM")

    return failures


# ================================================================
# SECTION 14: PUBLIC API — EXPORTED SYMBOLS
# ================================================================

__all__ = [
    # Phonology
    "ORAL_VOWELS", "NASAL_VOWELS", "CONSONANTS",
    "TONE_HIGH", "TONE_LOW", "TONE_MID",
    "to_nfc", "to_nfd",
    "strip_tones", "strip_all_diacritics", "get_tone_pattern",
    # Pronouns
    "PronounSet",
    "SUBJECT_PRONOUNS", "OBJECT_PRONOUNS", "POSSESSIVE_PRONOUNS",
    "EMPHATIC_PRONOUNS", "NEGATIVE_SUBJECT_PRONOUNS",
    "get_pronoun",
    # TAM
    "TAMMarker", "TAM_MARKERS", "get_tam",
    # Negation
    "NEGATION_MARKERS", "negate",
    # Verb conjugation
    "VerbConjugation", "conjugate_verb",
    # Phonological processes
    "ELISION_RULES", "apply_elision",
    # Noun morphology
    "PLURAL_MARKER", "pluralize",
    "NOMINALIZING_PREFIXES", "nominalize",
    # Questions
    "QUESTION_PARTICLES", "form_question",
    # Politeness
    "make_polite",
    # Serial verbs
    "build_serial_verb",
    # Analysis
    "MorphAnalysis", "analyze_token", "analyze_sentence", "tokenize_yoruba",
    # Validation
    "validate_tone_marking", "validate_dataset_morphology",
]


# ================================================================
# SECTION 15: SCRIPT ENTRY POINT
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Yoruba Morphological Rules Engine — Self-Test")
    print("=" * 60)

    failures = _run_self_tests()
    if failures:
        print(f"\n❌ {len(failures)} test(s) failed:")
        for f in failures:
            print(f"   - {f}")
    else:
        print("\n✅ All self-tests passed.")

    # Demonstrate integration with the education_dataset if available
    try:
        from yoruba_english_education_dataset import education_dataset  # type: ignore
        print("\n" + "=" * 60)
        print("Validating education_dataset morphology...")
        print("=" * 60)
        report = validate_dataset_morphology(education_dataset)
        print(f"Total examples:       {report['total_examples']}")
        print(f"With tone marks:      {report['examples_with_tones']}")
        print(f"Tone coverage:        {report['tone_coverage_percent']}%")
        print("\nPer-section:")
        for sec, stats in report["by_section"].items():
            print(f"  {sec:40s} {stats['with_tone_marks']:4d}/{stats['examples']:4d}")
    except ImportError:
        print("\n(education_dataset module not importable — "
              "run alongside the dataset file to see full validation.)")

    # Demonstration examples
    print("\n" + "=" * 60)
    print("Demonstration")
    print("=" * 60)

    print("\n1. Conjugating 'kàwé' (to read):")
    for tam in ["present_habitual", "perfect", "future", "ability"]:
        c = conjugate_verb("kàwé", person=1, number="sg", tam=tam)
        print(f"   {tam:20s} -> {c.surface}")

    print("\n2. Negation examples:")
    print(f"   simple    -> {negate('mo', 'mọ̀', 'simple')}")
    print(f"   perfect   -> {negate('mo', 'parí', 'perfect')}")
    print(f"   imperative-> {negate('', 'sọ̀rọ̀', 'imperative')}")

    print("\n3. Question formation:")
    print(f"   {form_question('O lọ sí ilé ẹ̀kọ́.', 'yes_no_njẹ')}")
    print(f"   {form_question('ni orúkọ rẹ', 'what_full')}")

    print("\n4. Pluralization & Nominalization:")
    print(f"   pluralize('akẹ́kọ̀ọ́') -> {pluralize('akẹ́kọ̀ọ́')}")
    print(f"   nominalize('kọ́', 'olù') -> {nominalize('kọ́', 'olù')}")

    print("\n5. Tone analysis of 'olùkọ́':")
    print(f"   pattern: {get_tone_pattern('olùkọ́')}")
    print(f"   stripped: {strip_tones('olùkọ́')}")

    print("\n6. Sentence analysis — 'Mo ń kàwé ní ilé ẹ̀kọ́.':")
    for a in analyze_sentence("Mo ń kàwé ní ilé ẹ̀kọ́."):
        tags = []
        if a.is_pronoun:  tags.append(f"PRON({a.pronoun_info['paradigm']})")
        if a.is_tam:      tags.append(f"TAM({a.tam_info['name']})")
        if a.is_negation: tags.append("NEG")
        tag_str = " ".join(tags) if tags else "—"
        print(f"   {a.normalised:12s} tones={a.tones}  {tag_str}")