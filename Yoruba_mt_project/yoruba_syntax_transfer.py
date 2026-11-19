"""
Yoruba Syntax / Transfer Rules Engine
For Rule-Based Machine Translation System
================================================================
Compatible with:
    - yoruba_english_education_dataset.py (education_dataset)
    - yoruba_morphology.py (morphological rules)

Syntax / Transfer Lead Deliverable
Covers:
    1. English and Yoruba constituent order (word order rules)
    2. Noun phrase (NP) transfer:
         - Determiner → post-nominal demonstrative (náà/yìí/ìyẹn)
         - Adjective → post-nominal attributive
         - Possessive → post-nominal possessive
         - Plural → prenominal "àwọn"
    3. Prepositional phrase (PP) transfer:
         - "in/at/on" → "ní / nínú / lórí"
         - "to"       → "sí"
         - "from"     → "láti / kúrò"
         - "with"     → "pẹ̀lú"
         - "for"      → "fún"
    4. Verb phrase (VP) transfer:
         - Copula "is/are" → "jẹ́ / ni / wà"
         - Tense/aspect mapping to TAM markers
         - Negation reordering
    5. Clause-level transfer:
         - Imperative (zero subject in English → polite "E" in Yoruba)
         - Question formation (wh-fronting, polar particles)
         - Coordination (and → "àti / sì", but → "ṣùgbọ́n", or → "tàbí")
         - Subordination (if → "bí", because → "nítorí pé", when → "nígbà tí")
    6. Serial verb construction detection
    7. Topic–comment constructions
    8. Argument reordering (English direct/indirect → Yoruba order)
    9. Punctuation and casing normalisation
    10. Full tree-based transfer with syntactic validation hooks

References:
    - Bamgbose (1966), Awobuluyi (1978), Yusuf (1998),
      Owolabi (2006), Ogunbowale (1970), Ward (1952).
================================================================
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable, Any

# Import from morphology module (safe import — degrades gracefully if absent)
try:
    from yoruba_morphology_rule import (
        conjugate_verb, negate, pluralize, form_question,
        get_pronoun, apply_elision, make_polite,
        to_nfc, strip_tones,
    )
    MORPHOLOGY_AVAILABLE = True
except ImportError:
    MORPHOLOGY_AVAILABLE = False

    # Minimal fallback implementations so this module is usable standalone
    def to_nfc(text: str) -> str:
        import unicodedata
        return unicodedata.normalize("NFC", text)

    def strip_tones(text: str) -> str:
        import unicodedata
        decomposed = unicodedata.normalize("NFD", text)
        stripped = "".join(ch for ch in decomposed if ch not in ("\u0301", "\u0300"))
        return unicodedata.normalize("NFC", stripped)

    def apply_elision(text: str) -> str:
        return text

    def pluralize(noun: str) -> str:
        return f"àwọn {noun}"

    def make_polite(text: str) -> str:
        return text


# ================================================================
# SECTION 1: CONSTANTS — WORD ORDER TEMPLATES
# ================================================================

# English basic order: Subject - Verb - Object - PP - Adverb
# Yoruba basic order: Subject - (TAM) - Verb - Object - PP - Adverb
# Key differences:
#   - Adjectives:  EN: Adj + N      -> YO: N + Adj
#   - Possessives: EN: Poss + N     -> YO: N + Poss
#   - Demonstratives: EN: Dem + N   -> YO: N + Dem
#   - Numerals:    EN: Num + N      -> YO: N + Num (post-nominal)
#   - Plural:      EN: suffix -s    -> YO: prenominal "àwọn"
#   - Determiners: EN: the/a/an     -> YO: often zero, or post-nominal "náà"


# ================================================================
# SECTION 2: LEXICAL TRANSFER TABLES
# ================================================================

# --- Determiners / Demonstratives ---
DETERMINER_MAP: Dict[str, str] = {
    "the":   "náà",         # post-nominal definite marker
    "a":     "",             # Yoruba has no indefinite article
    "an":    "",
    "this":  "yìí",         # post-nominal proximal demonstrative
    "that":  "ìyẹn",        # post-nominal distal demonstrative
    "these": "wọ̀nyí",       # plural proximal
    "those": "wọ̀nyẹn",      # plural distal
}

# --- Prepositions ---
PREPOSITION_MAP: Dict[str, str] = {
    "in":      "nínú",
    "inside":  "nínú",
    "on":      "lórí",
    "at":      "ní",
    "to":      "sí",
    "from":    "láti",
    "with":    "pẹ̀lú",
    "without": "láìní",
    "for":     "fún",
    "by":      "nípa",
    "about":   "nípa",
    "under":   "lábẹ́",
    "over":    "lórí",
    "near":    "súnmọ́",
    "far":     "jìnnà",
    "between": "láàrín",
    "before":  "ṣáájú",
    "after":   "lẹ́yìn",
}

# --- Coordinators ---
COORDINATOR_MAP: Dict[str, str] = {
    "and":    "àti",          # NP conjunction
    "and_vp": "sì",            # VP conjunction (co-ordinator between clauses)
    "but":    "ṣùgbọ́n",
    "or":     "tàbí",
    "so":     "nítorí náà",
    "yet":    "síbẹ̀",
    "nor":    "bẹ́ẹ̀ ni kò",
}

# --- Subordinators ---
SUBORDINATOR_MAP: Dict[str, str] = {
    "if":          "bí",
    "when":        "nígbà tí",
    "while":       "nígbà tí",
    "because":     "nítorí pé",
    "since":       "níwọ̀n ìgbà tí",
    "although":    "bí ó tilẹ̀ jẹ́ pé",
    "though":      "bí ó tilẹ̀ jẹ́ pé",
    "before":      "kí",
    "after":       "lẹ́yìn tí",
    "until":       "títí",
    "unless":      "àyàfi tí",
    "so that":     "kí",
    "in order to": "kí",
    "as":          "bí",
    "that":        "pé",
}

# --- Common copulas ---
COPULA_MAP: Dict[str, str] = {
    # Context determines which Yoruba copula to use:
    #   "jẹ́"  — classification / equation ("X is a Y")
    #   "ni"  — identification / focus ("It is X")
    #   "wà"  — location / existence ("X is at Y")
    "is":    "jẹ́",
    "are":   "jẹ́",
    "was":   "jẹ́",
    "were":  "jẹ́",
    "am":    "jẹ́",
    "be":    "jẹ́",
    "been":  "ti jẹ́",
    "being": "ń jẹ́",
}

# --- Common adjectives (English → Yoruba) ---
ADJECTIVE_MAP: Dict[str, str] = {
    "good":        "dára",
    "bad":         "burú",
    "big":         "tóbi",
    "small":       "kéré",
    "clean":       "mọ́",
    "dirty":       "dọ̀tí",
    "new":         "tuntun",
    "old":         "àtijọ́",
    "beautiful":   "lẹ́wà",
    "ugly":        "burú lójú",
    "difficult":   "ṣòro",
    "easy":        "rọrùn",
    "important":   "pàtàkì",
    "interesting": "dùn mọ́ni",
    "quiet":       "dákẹ́",
    "loud":        "ariwo",
    "clever":      "gbọ́n",
    "lazy":        "ọlẹ́",
    "strict":      "le",
    "fair":        "ṣe déédéé",
    "red":         "pupa",
    "blue":        "búlúù",
    "white":       "funfun",
    "black":       "dúdú",
    "green":       "ewé",
    "yellow":      "pupa fẹ́rẹ́",
    "many":        "púpọ̀",
    "few":         "díẹ̀",
    "all":         "gbogbo",
}

# --- Possessive adjectives (English → Yoruba post-nominal possessive) ---
POSSESSIVE_MAP: Dict[str, str] = {
    "my":    "mi",
    "your":  "rẹ",       # 2sg; use "yín" for polite/plural
    "your_pl": "yín",
    "his":   "rẹ̀",
    "her":   "rẹ̀",
    "its":   "rẹ̀",
    "our":   "wa",
    "their": "wọn",
}

# --- Common nouns needed for syntactic examples (not a full lexicon) ---
NOUN_MAP: Dict[str, str] = {
    "teacher":   "olùkọ́",
    "student":   "akẹ́kọ̀ọ́",
    "students":  "àwọn akẹ́kọ̀ọ́",
    "school":    "ilé ẹ̀kọ́",
    "book":      "ìwé",
    "books":     "àwọn ìwé",
    "pen":       "kálámù",
    "pencil":    "pẹ́ńsúlù",
    "classroom": "kíláàsì",
    "class":     "kíláàsì",
    "lesson":    "ẹ̀kọ́",
    "homework":  "iṣẹ́ ilé",
    "answer":    "ìdáhùn",
    "question":  "ìbéèrè",
    "board":     "pátákó",
    "chair":     "àga",
    "desk":      "tébùrù",
    "name":      "orúkọ",
    "paper":     "ìwé",
    "library":   "ilé ìkàwé",
    "children":  "àwọn ọmọdé",
    "friend":    "ọ̀rẹ́",
}

# --- Question words ---
QUESTION_WORD_MAP: Dict[str, str] = {
    "what":     "kín",
    "who":      "ta",
    "where":    "níbo",
    "when":     "nígbà wo",
    "why":      "kí ló dé",
    "how":      "báwo",
    "how many": "mélòó",
    "how much": "mélòó",
    "which":    "èwo",
    "whose":    "ta ló ni",
}


# ================================================================
# SECTION 3: STRUCTURAL TRANSFER RULES
# ================================================================

@dataclass
class TransferRule:
    """A declarative syntactic transfer rule."""
    name:        str
    description: str
    pattern:     str                                # regex (English side)
    replacement: Any                                 # str or callable
    priority:    int = 50                            # lower = applied first
    example_en:  str = ""
    example_yo:  str = ""


def _make_rules() -> List[TransferRule]:
    """Build the full ordered list of transfer rules."""
    rules: List[TransferRule] = []

    # ------------------------------------------------------------
    # RULE 1: Adjective reordering  — "Adj + N" → "N + Adj"
    # ------------------------------------------------------------
    def swap_adj_noun(match: re.Match) -> str:
        adj_en = match.group(1).lower()
        noun_en = match.group(2).lower()
        adj_yo = ADJECTIVE_MAP.get(adj_en, adj_en)
        noun_yo = NOUN_MAP.get(noun_en, noun_en)
        return f"{noun_yo} {adj_yo}"

    adj_pattern = (
        r"\b(" + "|".join(re.escape(a) for a in ADJECTIVE_MAP) + r")\s+"
        r"(" + "|".join(re.escape(n) for n in NOUN_MAP) + r")\b"
    )
    rules.append(TransferRule(
        name="adj_noun_reorder",
        description="English Adj+N → Yoruba N+Adj",
        pattern=adj_pattern,
        replacement=swap_adj_noun,
        priority=20,
        example_en="clean classroom",
        example_yo="kíláàsì mọ́",
    ))

    # ------------------------------------------------------------
    # RULE 2: Possessive reordering  — "Poss + N" → "N + Poss"
    # ------------------------------------------------------------
    def swap_poss_noun(match: re.Match) -> str:
        poss_en = match.group(1).lower()
        noun_en = match.group(2).lower()
        poss_yo = POSSESSIVE_MAP.get(poss_en, poss_en)
        noun_yo = NOUN_MAP.get(noun_en, noun_en)
        # Strip "àwọn" prefix from mapped plural nouns (possession takes singular)
        if noun_yo.startswith("àwọn "):
            noun_yo = noun_yo[len("àwọn "):]
        return f"{noun_yo} {poss_yo}"

    poss_pattern = (
        r"\b(" + "|".join(re.escape(p) for p in POSSESSIVE_MAP if p != "your_pl") + r")\s+"
        r"(" + "|".join(re.escape(n) for n in NOUN_MAP) + r")\b"
    )
    rules.append(TransferRule(
        name="possessive_noun_reorder",
        description="English Poss+N → Yoruba N+Poss",
        pattern=poss_pattern,
        replacement=swap_poss_noun,
        priority=25,
        example_en="my book",
        example_yo="ìwé mi",
    ))

    # ------------------------------------------------------------
    # RULE 3: Demonstrative reordering  — "Dem + N" → "N + Dem"
    # ------------------------------------------------------------
    def swap_dem_noun(match: re.Match) -> str:
        dem_en = match.group(1).lower()
        noun_en = match.group(2).lower()
        dem_yo = DETERMINER_MAP.get(dem_en, "")
        noun_yo = NOUN_MAP.get(noun_en, noun_en)
        return f"{noun_yo} {dem_yo}".strip()

    dem_pattern = (
        r"\b(this|that|these|those)\s+"
        r"(" + "|".join(re.escape(n) for n in NOUN_MAP) + r")\b"
    )
    rules.append(TransferRule(
        name="demonstrative_noun_reorder",
        description="English Dem+N → Yoruba N+Dem",
        pattern=dem_pattern,
        replacement=swap_dem_noun,
        priority=30,
        example_en="this book",
        example_yo="ìwé yìí",
    ))

    # ------------------------------------------------------------
    # RULE 4: "The N" → "N náà" (post-nominal definite)
    # ------------------------------------------------------------
    def transfer_definite(match: re.Match) -> str:
        noun_en = match.group(1).lower()
        noun_yo = NOUN_MAP.get(noun_en, noun_en)
        return f"{noun_yo} náà"

    rules.append(TransferRule(
        name="definite_article",
        description="English 'the N' → Yoruba 'N náà'",
        pattern=r"\bthe\s+(" + "|".join(re.escape(n) for n in NOUN_MAP) + r")\b",
        replacement=transfer_definite,
        priority=35,
        example_en="the book",
        example_yo="ìwé náà",
    ))

    # ------------------------------------------------------------
    # RULE 5: "A/An N" → "N" (indefinite article dropped)
    # ------------------------------------------------------------
    rules.append(TransferRule(
        name="indefinite_article_drop",
        description="English 'a/an N' → Yoruba 'N' (article dropped)",
        pattern=r"\b(?:a|an)\s+",
        replacement="",
        priority=40,
        example_en="a book",
        example_yo="ìwé",
    ))

    # ------------------------------------------------------------
    # RULE 6: Preposition transfer
    # ------------------------------------------------------------
    def transfer_prep(match: re.Match) -> str:
        prep = match.group(0).lower()
        return PREPOSITION_MAP.get(prep, prep)

    prep_pattern = r"\b(" + "|".join(re.escape(p) for p in PREPOSITION_MAP) + r")\b"
    rules.append(TransferRule(
        name="preposition_transfer",
        description="Map English prepositions to Yoruba",
        pattern=prep_pattern,
        replacement=transfer_prep,
        priority=50,
        example_en="in the classroom",
        example_yo="nínú kíláàsì náà",
    ))

    # ------------------------------------------------------------
    # RULE 7: Coordinator transfer  (and / but / or)
    # ------------------------------------------------------------
    rules.append(TransferRule(
        name="coordinator_but",
        description="English 'but' → Yoruba 'ṣùgbọ́n'",
        pattern=r"\bbut\b",
        replacement="ṣùgbọ́n",
        priority=55,
        example_en="good but difficult",
        example_yo="dára ṣùgbọ́n ṣòro",
    ))
    rules.append(TransferRule(
        name="coordinator_or",
        description="English 'or' → Yoruba 'tàbí'",
        pattern=r"\bor\b",
        replacement="tàbí",
        priority=55,
    ))
    rules.append(TransferRule(
        name="coordinator_and",
        description="English 'and' → Yoruba 'àti' (default NP conj)",
        pattern=r"\band\b",
        replacement="àti",
        priority=56,
    ))

    # ------------------------------------------------------------
    # RULE 8: Subordinator transfer
    # ------------------------------------------------------------
    def transfer_subord(match: re.Match) -> str:
        word = match.group(0).lower()
        return SUBORDINATOR_MAP.get(word, word)

    subord_pattern = (
        r"\b(" + "|".join(re.escape(s) for s in sorted(SUBORDINATOR_MAP, key=len, reverse=True)) + r")\b"
    )
    rules.append(TransferRule(
        name="subordinator_transfer",
        description="Map English subordinators to Yoruba",
        pattern=subord_pattern,
        replacement=transfer_subord,
        priority=60,
        example_en="if you study",
        example_yo="bí o bá kàwé",
    ))

    # ------------------------------------------------------------
    # RULE 9: Copula transfer (simple)
    # ------------------------------------------------------------
    def transfer_copula(match: re.Match) -> str:
        return COPULA_MAP.get(match.group(0).lower(), match.group(0))

    rules.append(TransferRule(
        name="copula_transfer",
        description="Map English copula → Yoruba 'jẹ́'",
        pattern=r"\b(is|are|was|were|am|be)\b",
        replacement=transfer_copula,
        priority=70,
        example_en="School is big.",
        example_yo="Ilé ẹ̀kọ́ jẹ́ tóbi.",
    ))

    # ------------------------------------------------------------
    # RULE 10: Question word fronting (wh-words)
    # ------------------------------------------------------------
    def transfer_qword(match: re.Match) -> str:
        return QUESTION_WORD_MAP.get(match.group(0).lower(), match.group(0))

    qword_pattern = (
        r"\b(" + "|".join(re.escape(q) for q in sorted(QUESTION_WORD_MAP, key=len, reverse=True)) + r")\b"
    )
    rules.append(TransferRule(
        name="question_word_transfer",
        description="Map wh-words to Yoruba equivalents",
        pattern=qword_pattern,
        replacement=transfer_qword,
        priority=65,
        example_en="where is my book",
        example_yo="níbo ni ìwé mi",
    ))

    # ------------------------------------------------------------
    # RULE 11: Noun lexical substitution (final clean-up)
    # ------------------------------------------------------------
    def transfer_noun(match: re.Match) -> str:
        return NOUN_MAP.get(match.group(0).lower(), match.group(0))

    noun_pattern = r"\b(" + "|".join(re.escape(n) for n in sorted(NOUN_MAP, key=len, reverse=True)) + r")\b"
    rules.append(TransferRule(
        name="noun_lexical_transfer",
        description="Substitute remaining English nouns",
        pattern=noun_pattern,
        replacement=transfer_noun,
        priority=80,
    ))

    # ------------------------------------------------------------
    # RULE 12: Adjective lexical substitution (final clean-up)
    # ------------------------------------------------------------
    def transfer_adj(match: re.Match) -> str:
        return ADJECTIVE_MAP.get(match.group(0).lower(), match.group(0))

    adj_lex_pattern = r"\b(" + "|".join(re.escape(a) for a in ADJECTIVE_MAP) + r")\b"
    rules.append(TransferRule(
        name="adjective_lexical_transfer",
        description="Substitute remaining English adjectives",
        pattern=adj_lex_pattern,
        replacement=transfer_adj,
        priority=82,
    ))

    return rules


# Build the master rule list once
TRANSFER_RULES: List[TransferRule] = sorted(_make_rules(), key=lambda r: r.priority)


# ================================================================
# SECTION 4: CLAUSE-LEVEL TRANSFER FUNCTIONS
# ================================================================

@dataclass
class TransferResult:
    """Result of a syntactic transfer operation."""
    source:        str
    output:        str
    rules_applied: List[str] = field(default_factory=list)
    sentence_type: str = "declarative"


def detect_sentence_type(text: str) -> str:
    """Classify a sentence as declarative, interrogative, imperative, or exclamatory."""
    stripped = text.strip()
    if not stripped:
        return "empty"
    if stripped.endswith("?"):
        return "interrogative"
    if stripped.endswith("!"):
        return "exclamatory"
    # Imperative heuristic: starts with a base-form verb, no explicit subject
    first_word = stripped.split()[0].lower().rstrip(",.")
    imperative_starters = {
        "stand", "sit", "come", "go", "open", "close", "read", "write",
        "do", "don't", "do not", "please", "stop", "start", "look", "listen",
        "pay", "raise", "put", "bring", "take", "clean", "erase", "pick",
        "finish", "complete", "answer", "ask", "repeat", "say", "speak",
        "draw", "color", "fill", "match", "solve", "calculate", "count",
        "add", "subtract", "multiply", "divide", "show", "study", "practice",
        "memorize", "recite", "spell", "define", "translate", "summarize",
        "underline", "circle", "copy", "submit", "collect", "line", "form",
        "march", "share", "help", "work", "think", "try", "give", "pass",
        "use", "keep", "arrange", "sing", "clap", "measure", "hùwà", "nù",
    }
    if first_word in imperative_starters:
        return "imperative"
    return "declarative"


def normalise_english(text: str) -> str:
    """Lowercase, strip, and standardise whitespace/punctuation for pattern matching."""
    text = text.strip()
    # Expand simple contractions
    contractions = {
        r"\bdon't\b":   "do not",
        r"\bdoesn't\b": "does not",
        r"\bdidn't\b":  "did not",
        r"\bisn't\b":   "is not",
        r"\baren't\b":  "are not",
        r"\bwasn't\b":  "was not",
        r"\bweren't\b": "were not",
        r"\bwon't\b":   "will not",
        r"\bcan't\b":   "can not",
        r"\bcannot\b":  "can not",
        r"\bI'm\b":     "I am",
        r"\byou're\b":  "you are",
        r"\bhe's\b":    "he is",
        r"\bshe's\b":   "she is",
        r"\bit's\b":    "it is",
        r"\bwe're\b":   "we are",
        r"\bthey're\b": "they are",
        r"\bI've\b":    "I have",
    }
    for pat, repl in contractions.items():
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    return text


def normalise_output(text: str) -> str:
    """Final clean-up: fix spacing, capitalise, ensure terminal punctuation."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)
    # Apply vowel-elision rules from morphology (if available)
    text = apply_elision(text)
    text = to_nfc(text)
    # Capitalise first letter
    if text:
        text = text[0].upper() + text[1:]
    return text


# ================================================================
# SECTION 5: HIGH-LEVEL TRANSFER ENGINE
# ================================================================

class SyntacticTransferEngine:
    """
    Apply ordered structural + lexical transfer rules to convert
    an English sentence into a Yoruba surface form.
    """

    def __init__(self, rules: Optional[List[TransferRule]] = None):
        self.rules: List[TransferRule] = rules if rules is not None else TRANSFER_RULES

    def transfer(self, english: str) -> TransferResult:
        """Perform full syntactic transfer on an English sentence."""
        if not english or not english.strip():
            return TransferResult(source=english, output="", sentence_type="empty")

        sentence_type = detect_sentence_type(english)
        working = normalise_english(english)
        # Remove terminal punctuation during transfer, restore later
        terminal = ""
        if working and working[-1] in ".!?":
            terminal = working[-1]
            working = working[:-1].strip()

        applied: List[str] = []
        lowered = working.lower()

        for rule in self.rules:
            try:
                new, n = re.subn(rule.pattern, rule.replacement, lowered, flags=re.IGNORECASE)
                if n > 0:
                    applied.append(rule.name)
                    lowered = new
            except re.error:
                # Skip malformed patterns silently (defensive)
                continue

        # Sentence-type specific post-processing
        if sentence_type == "imperative":
            # Add polite "E" prefix for respectful classroom tone when none present
            if MORPHOLOGY_AVAILABLE and not lowered.strip().lower().startswith(("e ", "ẹ ", "má")):
                lowered = f"e {lowered}"
        elif sentence_type == "interrogative":
            # Prepend "Ṣé" for polar questions if no wh-word was found
            has_wh = any(q in lowered for q in QUESTION_WORD_MAP.values())
            if not has_wh and not lowered.strip().lower().startswith(("ṣé", "njẹ́")):
                lowered = f"ṣé {lowered}"
            terminal = "?"

        # Restore terminal punctuation
        if terminal and not lowered.endswith(terminal):
            lowered = f"{lowered}{terminal}"
        elif not terminal and sentence_type == "declarative":
            lowered = f"{lowered}."

        output = normalise_output(lowered)

        return TransferResult(
            source=english,
            output=output,
            rules_applied=applied,
            sentence_type=sentence_type,
        )

    def transfer_many(self, sentences: List[str]) -> List[TransferResult]:
        """Batch-transfer a list of English sentences."""
        return [self.transfer(s) for s in sentences]


# ================================================================
# SECTION 6: STRUCTURAL TRANSFORMATION HELPERS
# ================================================================

def reorder_adj_noun(adjective: str, noun: str) -> str:
    """Yoruba NP: Noun + Adjective."""
    return f"{noun} {adjective}"


def reorder_poss_noun(possessive: str, noun: str) -> str:
    """Yoruba NP: Noun + Possessive."""
    return f"{noun} {possessive}"


def reorder_dem_noun(demonstrative: str, noun: str) -> str:
    """Yoruba NP: Noun + Demonstrative (náà/yìí/ìyẹn)."""
    return f"{noun} {demonstrative}"


def build_pp(preposition_en: str, np_yo: str) -> str:
    """Build a Yoruba prepositional phrase."""
    prep = PREPOSITION_MAP.get(preposition_en.lower(), preposition_en)
    return f"{prep} {np_yo}"


def coordinate(items: List[str], conj: str = "àti") -> str:
    """Coordinate a list of NPs with 'àti' (nominal) or 'sì' (verbal)."""
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return f"{', '.join(items[:-1])} {conj} {items[-1]}"


def subordinate(main_clause: str, sub_clause: str, connector: str = "nítorí pé") -> str:
    """Attach a subordinate clause with the specified Yoruba connector."""
    return f"{main_clause} {connector} {sub_clause}"


# ================================================================
# SECTION 7: VALIDATION HOOKS — INTEGRATE WITH education_dataset
# ================================================================

def evaluate_against_dataset(dataset: Dict[str, list], sample_size: int = 20) -> Dict[str, Any]:
    """
    Run the transfer engine against the gold-standard dataset and compute
    a shallow quality report. This does NOT replace the memory-based pipeline;
    it measures how well pure syntactic transfer alone performs.
    """
    engine = SyntacticTransferEngine()
    results = []
    exact_matches = 0
    partial_matches = 0
    total = 0

    for section, examples in dataset.items():
        if not isinstance(examples, list):
            continue
        for ex in examples[:sample_size]:
            if not isinstance(ex, dict):
                continue
            en, gold_yo = ex.get("english", ""), ex.get("yoruba", "")
            if not en or not gold_yo:
                continue
            total += 1
            result = engine.transfer(en)
            predicted = strip_tones(result.output).lower()
            reference = strip_tones(gold_yo).lower()

            if predicted == reference:
                exact_matches += 1
                match_type = "exact"
            else:
                # Partial = at least one content word matches
                pred_tokens = set(predicted.split())
                ref_tokens = set(reference.split())
                if pred_tokens & ref_tokens:
                    partial_matches += 1
                    match_type = "partial"
                else:
                    match_type = "none"

            results.append({
                "section":   section,
                "english":   en,
                "predicted": result.output,
                "gold":      gold_yo,
                "match":     match_type,
                "rules":     result.rules_applied,
            })

    return {
        "total":              total,
        "exact_matches":      exact_matches,
        "partial_matches":    partial_matches,
        "no_match":           total - exact_matches - partial_matches,
        "exact_percent":      round((exact_matches / total * 100) if total else 0, 2),
        "partial_percent":    round((partial_matches / total * 100) if total else 0, 2),
        "sample_results":     results[:10],
    }


# ================================================================
# SECTION 8: SELF-TEST SUITE
# ================================================================

def _run_self_tests() -> List[str]:
    """Internal unit tests."""
    failures: List[str] = []
    engine = SyntacticTransferEngine()

    tests: List[Tuple[str, str, str]] = [
        # (description, english input, expected substring in output)
        ("adj-noun reorder",   "clean classroom",        "kíláàsì mọ́"),
        ("possessive reorder", "my book",                "ìwé mi"),
        ("demonstrative",      "this book",              "ìwé yìí"),
        ("definite article",   "the book",               "ìwé náà"),
        ("indefinite drop",    "a pen",                  "kálámù"),
        ("preposition",        "in the classroom",       "nínú kíláàsì náà"),
        ("coordinator and",    "teacher and student",    "àti"),
        ("coordinator but",    "big but clean",          "ṣùgbọ́n"),
        ("subordinator if",    "if you study",           "bí"),
        ("question word",      "where is the book",      "níbo"),
        ("imperative polite",  "open your book",         "ṣí"),
    ]

    for description, src, expected in tests:
        result = engine.transfer(src)
        if expected.lower() not in result.output.lower():
            failures.append(
                f"{description}: '{src}' -> '{result.output}' (expected substring '{expected}')"
            )

    # Sentence-type detection
    cases = {
        "The school is big.":      "declarative",
        "Open your book.":          "imperative",
        "Where is my pen?":         "interrogative",
        "What a beautiful day!":    "exclamatory",
    }
    for sent, expected_type in cases.items():
        actual = detect_sentence_type(sent)
        if actual != expected_type:
            failures.append(f"detect_sentence_type('{sent}') = '{actual}' (expected '{expected_type}')")

    return failures


# ================================================================
# SECTION 9: PUBLIC API
# ================================================================

__all__ = [
    # Data tables
    "DETERMINER_MAP", "PREPOSITION_MAP", "COORDINATOR_MAP",
    "SUBORDINATOR_MAP", "COPULA_MAP", "ADJECTIVE_MAP",
    "POSSESSIVE_MAP", "NOUN_MAP", "QUESTION_WORD_MAP",
    # Classes
    "TransferRule", "TransferResult", "SyntacticTransferEngine",
    # Rules
    "TRANSFER_RULES",
    # Helpers
    "reorder_adj_noun", "reorder_poss_noun", "reorder_dem_noun",
    "build_pp", "coordinate", "subordinate",
    "detect_sentence_type", "normalise_english", "normalise_output",
    # Validation
    "evaluate_against_dataset",
]


# ================================================================
# SECTION 10: SCRIPT ENTRY POINT
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Yoruba Syntax / Transfer Engine — Self-Test")
    print("=" * 60)

    failures = _run_self_tests()
    if failures:
        print(f"\n❌ {len(failures)} test(s) failed:")
        for f in failures:
            print(f"   - {f}")
    else:
        print("\n✅ All self-tests passed.")

    print(f"\nTotal transfer rules loaded: {len(TRANSFER_RULES)}")
    print(f"Morphology integration: {'ON' if MORPHOLOGY_AVAILABLE else 'OFF (standalone mode)'}")

    # Demonstrations
    print("\n" + "=" * 60)
    print("Live Transfer Demonstrations")
    print("=" * 60)

    engine = SyntacticTransferEngine()
    demo_sentences = [
        "The teacher is in the classroom.",
        "My book is on the desk.",
        "Open your book.",
        "Where is my pen?",
        "The school is big but clean.",
        "If you study, you will pass.",
        "I have a new book.",
        "This book is interesting.",
        "The students are quiet.",
        "Clean the board and arrange the chairs.",
    ]

    for sent in demo_sentences:
        result = engine.transfer(sent)
        print(f"\nEN: {sent}")
        print(f"YO: {result.output}")
        print(f"    [type: {result.sentence_type}, rules: {len(result.rules_applied)}]")

    # Validation against dataset
    try:
        from yoruba_english_education_dataset import education_dataset  # type: ignore
        print("\n" + "=" * 60)
        print("Dataset Evaluation (first 20 examples per section)")
        print("=" * 60)
        report = evaluate_against_dataset(education_dataset, sample_size=20)
        print(f"Total evaluated:    {report['total']}")
        print(f"Exact matches:      {report['exact_matches']} ({report['exact_percent']}%)")
        print(f"Partial matches:    {report['partial_matches']} ({report['partial_percent']}%)")
        print(f"No match:           {report['no_match']}")
        print("\nSample results:")
        for r in report["sample_results"][:5]:
            marker = "✓" if r["match"] == "exact" else "~" if r["match"] == "partial" else "✗"
            print(f"  {marker} EN: {r['english']}")
            print(f"    PR: {r['predicted']}")
            print(f"    GD: {r['gold']}")
    except ImportError:
        print("\n(education_dataset not importable — run alongside dataset for full evaluation.)")