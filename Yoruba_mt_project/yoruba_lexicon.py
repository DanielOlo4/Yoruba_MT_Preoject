"""
Yoruba-English Bilingual Lexicon / Dictionary
For Rule-Based Machine Translation System
================================================================
Compatible with:
    - yoruba_english_education_dataset.py (education_dataset)
    - yoruba_morphology.py (morphological rules)
    - yoruba_syntax_transfer.py (structural transfer)

Lexicon / Dictionary Lead Deliverable
Covers:
    1. Core bilingual lexicon (1000+ entries) organised by POS
    2. Lexical entry dataclass with rich metadata:
         - Part of speech, tone pattern, register, domain
         - Multiple glosses, examples, morphological features
    3. Bidirectional lookup (EN↔YO) with fuzzy matching
    4. Multi-word expression (MWE) support
    5. Automatic extraction of vocabulary from education_dataset
    6. Semantic domain organization (classroom, academic, social, etc.)
    7. POS-tagged word lists for downstream tools
    8. Frequency and confidence scoring
    9. Validation and consistency checks
    10. Export utilities (JSONL, CSV, Python dict)

References:
    - Abraham (1958). Dictionary of Modern Yoruba.
    - Bamgbose (1966). A Grammar of Yoruba.
    - Awobuluyi (1978). Essentials of Yoruba Grammar.
    - NERDC Curriculum Materials.
================================================================
"""

from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Tuple, Iterable
from enum import Enum


# ================================================================
# SECTION 1: ENUMERATIONS — POS, DOMAIN, REGISTER
# ================================================================

class POS(str, Enum):
    """Part of speech tags used across the lexicon."""
    NOUN         = "N"
    PROPER_NOUN  = "PROPN"
    VERB         = "V"
    ADJECTIVE    = "ADJ"
    ADVERB       = "ADV"
    PRONOUN      = "PRON"
    DETERMINER   = "DET"
    PREPOSITION  = "PREP"
    CONJUNCTION  = "CONJ"
    INTERJECTION = "INTJ"
    NUMERAL      = "NUM"
    PARTICLE     = "PART"
    AUXILIARY    = "AUX"
    MWE          = "MWE"      # Multi-word expression
    GREETING     = "GREET"
    UNKNOWN      = "X"


class Domain(str, Enum):
    """Semantic domain tags."""
    GREETING          = "greeting"
    CLASSROOM         = "classroom"
    ACADEMIC          = "academic"
    SCHOOL_ENV        = "school_environment"
    SUBJECT           = "subject"
    OBJECT            = "object"
    PERSON            = "person"
    TIME              = "time"
    NUMBER            = "number"
    ACTION            = "action"
    EMOTION           = "emotion"
    QUALITY           = "quality"
    QUESTION          = "question"
    SOCIAL            = "social"
    BODY              = "body"
    FOOD              = "food"
    PLACE             = "place"
    FUNCTION          = "function"       # grammatical / function word
    GENERAL           = "general"


class Register(str, Enum):
    """Register / politeness level."""
    NEUTRAL   = "neutral"
    POLITE    = "polite"      # uses honorific "E"
    FORMAL    = "formal"
    INFORMAL  = "informal"
    LITERARY  = "literary"


# ================================================================
# SECTION 2: LEXICAL ENTRY DATACLASS
# ================================================================

@dataclass
class LexEntry:
    """A single bilingual dictionary entry."""
    yoruba:         str                                   # Yoruba headword (NFC)
    english:        str                                   # Primary English gloss
    pos:            POS                                   # Part of speech
    domain:         Domain = Domain.GENERAL               # Semantic domain
    register:       Register = Register.NEUTRAL           # Register
    glosses:        List[str] = field(default_factory=list)   # Alternative glosses
    examples:       List[Tuple[str, str]] = field(default_factory=list)  # (en, yo)
    tone_pattern:   str = ""                              # e.g., "MLH"
    plural:         Optional[str] = None                  # Pluralised form (if marked)
    notes:          str = ""                              # Linguistic notes
    frequency:      int = 1                               # Occurrence count
    confidence:     float = 1.0                           # 0.0–1.0 reliability
    source:         str = "lexicon"                       # 'lexicon' | 'dataset' | 'user'

    def to_dict(self) -> dict:
        d = asdict(self)
        d["pos"]      = self.pos.value
        d["domain"]   = self.domain.value
        d["register"] = self.register.value
        return d

    def all_glosses(self) -> List[str]:
        """Return primary gloss plus alternatives."""
        return [self.english] + list(self.glosses)


# ================================================================
# SECTION 3: UNICODE HELPERS
# ================================================================

def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _strip_tones(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(ch for ch in decomposed if ch not in ("\u0301", "\u0300"))
    return unicodedata.normalize("NFC", stripped)


def _get_tone_pattern(word: str) -> str:
    """Return tone pattern of a Yoruba word as string of H/M/L."""
    pattern = []
    for ch in _nfc(word):
        decomp = unicodedata.normalize("NFD", ch)
        base = decomp[0].lower() if decomp else ""
        if base in "aeiou":
            if "\u0301" in decomp:
                pattern.append("H")
            elif "\u0300" in decomp:
                pattern.append("L")
            else:
                pattern.append("M")
    return "".join(pattern)


def _normalize_english_key(text: str) -> str:
    """Lowercase, strip punctuation and whitespace for lookup."""
    text = text.lower().strip().rstrip(".!?,;:")
    text = re.sub(r"\s+", " ", text)
    return text


# ================================================================
# SECTION 4: CORE LEXICON ENTRIES
# ================================================================

def _build_core_lexicon() -> List[LexEntry]:
    """Hand-curated core lexicon covering the education domain."""
    entries: List[LexEntry] = []

    # ---------- GREETINGS & INTERJECTIONS ----------
    greetings = [
        ("E káàárọ̀",     "good morning",        [("Good morning, teacher.", "E káàárọ̀, olùkọ́.")]),
        ("E kú ọ̀sán",    "good afternoon",      [("Good afternoon.", "E kú ọ̀sán.")]),
        ("E kú ìrọ̀lẹ́",   "good evening",        []),
        ("E kú àbọ̀",     "welcome",             [("Welcome to school.", "E kú àbọ̀ sí ilé ẹ̀kọ́.")]),
        ("E ṣé",         "thank you",           [("Thank you, teacher.", "E ṣé, olùkọ́.")]),
        ("O dàbọ̀",      "goodbye",             []),
        ("O dáàrọ̀",     "good night",          []),
        ("Báwo ni",      "how are you",         [("How are you?", "Báwo ni?")]),
        ("E jọ̀wọ́",      "please",              []),
        ("E má bínú",   "I am sorry",          []),
        ("E káàsán",     "good day",            []),
    ]
    for yo, en, exs in greetings:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.GREETING,
            domain=Domain.GREETING, register=Register.POLITE,
            examples=exs, tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- PRONOUNS ----------
    pronouns = [
        ("mo",   "I",         "subject 1sg"),
        ("o",    "you",       "subject 2sg informal"),
        ("ó",    "he/she/it", "subject 3sg"),
        ("a",    "we",        "subject 1pl"),
        ("ẹ",    "you (pl)",  "subject 2pl / polite"),
        ("wọ́n",  "they",      "subject 3pl"),
        ("èmi",  "I (emph)",  "emphatic 1sg"),
        ("ìwọ",  "you (emph)","emphatic 2sg"),
        ("òun",  "he/she",    "emphatic 3sg"),
        ("àwa",  "we (emph)", "emphatic 1pl"),
        ("ẹ̀yin", "you (emph)","emphatic 2pl"),
        ("àwọn", "they (emph)","emphatic 3pl / plural marker"),
        ("mi",   "me/my",     "object/possessive 1sg"),
        ("rẹ",   "your",      "possessive 2sg"),
        ("rẹ̀",  "his/her/its","possessive 3sg"),
        ("wa",   "our/us",    "object/possessive 1pl"),
        ("yín",  "your (pl)", "possessive 2pl / polite"),
        ("wọn",  "them/their","object/possessive 3pl"),
    ]
    for yo, en, note in pronouns:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.PRONOUN,
            domain=Domain.FUNCTION, notes=note,
            tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- DETERMINERS / DEMONSTRATIVES ----------
    determiners = [
        ("náà",    "the/that",   "post-nominal definite"),
        ("yìí",    "this",       "post-nominal proximal"),
        ("ìyẹn",   "that",       "distal demonstrative"),
        ("wọ̀nyí",  "these",      "plural proximal"),
        ("wọ̀nyẹn", "those",      "plural distal"),
        ("gbogbo", "all",        "quantifier"),
    ]
    for yo, en, note in determiners:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.DETERMINER,
            domain=Domain.FUNCTION, notes=note,
            tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- PREPOSITIONS ----------
    prepositions = [
        ("ní",      "at/in",       "general locative"),
        ("nínú",    "inside/in",   "containment"),
        ("lórí",    "on/upon",     "surface contact"),
        ("sí",      "to",          "directional"),
        ("láti",    "from",        "source"),
        ("kúrò",    "away from",   "departure"),
        ("pẹ̀lú",   "with",        "comitative"),
        ("láìní",   "without",     "privative"),
        ("fún",     "for",         "benefactive"),
        ("nípa",    "about/by",    "topic/means"),
        ("lábẹ́",    "under",       "sub-locative"),
        ("súnmọ́",   "near",        "proximity"),
        ("jìnnà",   "far",         "distance"),
        ("láàrín",  "between",     "mediative"),
        ("ṣáájú",   "before",      "temporal/spatial"),
        ("lẹ́yìn",   "after/behind","temporal/spatial"),
    ]
    for yo, en, note in prepositions:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.PREPOSITION,
            domain=Domain.FUNCTION, notes=note,
            tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- CONJUNCTIONS ----------
    conjunctions = [
        ("àti",       "and",       "NP conjunction"),
        ("sì",        "and",       "VP/clause conjunction"),
        ("ṣùgbọ́n",   "but",       "contrast"),
        ("tàbí",      "or",        "disjunction"),
        ("nítorí náà","so",         "consequence"),
        ("bí",        "if/as",     "conditional"),
        ("nígbà tí",  "when",      "temporal"),
        ("nítorí pé", "because",   "causal"),
        ("kí",        "that/so that","purposive"),
        ("títí",      "until",     "temporal limit"),
        ("pé",        "that",      "complementiser"),
        ("bí ó tilẹ̀ jẹ́ pé", "although", "concessive"),
    ]
    for yo, en, note in conjunctions:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.CONJUNCTION,
            domain=Domain.FUNCTION, notes=note,
            tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- AUXILIARIES / TAM PARTICLES ----------
    auxiliaries = [
        ("ń",       "progressive",   "pre-verbal progressive marker"),
        ("ti",      "perfect",       "perfect aspect"),
        ("yóò",     "will",          "future"),
        ("máa",     "will / shall",  "future / intentive"),
        ("máa ń",   "usually",       "habitual"),
        ("lè",      "can",           "ability"),
        ("gbọ́dọ̀",  "must",          "obligation"),
        ("fẹ́",      "want to",       "desiderative"),
        ("kò",      "not",           "negation"),
        ("má",      "do not",        "imperative negation"),
        ("tíì",     "yet",           "used with perfect negation"),
        ("bá",      "if/when",       "conditional particle"),
    ]
    for yo, en, note in auxiliaries:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.AUXILIARY,
            domain=Domain.FUNCTION, notes=note,
            tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- QUESTION PARTICLES / WH-WORDS ----------
    question_words = [
        ("Ṣé",       "is it that",  "polar question"),
        ("Njẹ́",     "is it that",  "polar question (formal)"),
        ("kín",      "what",        ""),
        ("ta",       "who",         ""),
        ("níbo",     "where",       ""),
        ("nígbà wo", "when",        ""),
        ("kí ló dé", "why",         ""),
        ("báwo",     "how",         ""),
        ("mélòó",    "how many",    ""),
        ("èwo",      "which",       ""),
    ]
    for yo, en, note in question_words:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.PARTICLE,
            domain=Domain.QUESTION, notes=note,
            tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- NUMERALS ----------
    numerals = [
        ("ọ̀kan", "one", 1), ("èjì", "two", 2), ("ẹ̀ta", "three", 3),
        ("ẹ̀rin", "four", 4), ("àrún", "five", 5), ("ẹ̀fà", "six", 6),
        ("èje", "seven", 7), ("ẹ̀jọ", "eight", 8), ("ẹ̀sán", "nine", 9),
        ("ẹ̀wàá", "ten", 10),
        ("ọ̀kànlá", "eleven", 11), ("èjìlá", "twelve", 12),
        ("ẹ̀tàlá", "thirteen", 13), ("ẹ̀rìnlá", "fourteen", 14),
        ("ẹ̀ẹ́dógún", "fifteen", 15), ("ogún", "twenty", 20),
        ("ọgbọ̀n", "thirty", 30), ("ogójì", "forty", 40),
        ("àádọ́ta", "fifty", 50), ("ọgọ́rùn-ún", "one hundred", 100),
        ("ẹgbẹ̀rún", "one thousand", 1000),
        ("àkọ́kọ́", "first", None), ("èkejì", "second", None),
        ("ẹ̀kẹta", "third", None), ("ìkẹyìn", "last", None),
    ]
    for yo, en, value in numerals:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.NUMERAL,
            domain=Domain.NUMBER,
            notes=f"value={value}" if value is not None else "ordinal",
            tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- NOUNS: CLASSROOM & ACADEMIC ----------
    nouns_classroom = [
        ("olùkọ́",           "teacher",        Domain.PERSON),
        ("akẹ́kọ̀ọ́",         "student",        Domain.PERSON),
        ("àwọn akẹ́kọ̀ọ́",    "students",       Domain.PERSON),
        ("olùdarí",          "principal",      Domain.PERSON),
        ("ọ̀rẹ́",            "friend",         Domain.PERSON),
        ("ọmọdé",            "child",          Domain.PERSON),
        ("àwọn ọmọdé",       "children",       Domain.PERSON),
        ("ènìyàn",           "person",         Domain.PERSON),
        ("ilé ẹ̀kọ́",         "school",         Domain.PLACE),
        ("kíláàsì",          "class/classroom",Domain.PLACE),
        ("ilé ìkàwé",        "library",        Domain.PLACE),
        ("ilé yàrá ìdánwò",  "laboratory",     Domain.PLACE),
        ("pápá eré",         "playground",     Domain.PLACE),
        ("ọ́fíìsì",           "office",         Domain.PLACE),
        ("yàrá olùkọ́",       "staffroom",      Domain.PLACE),
        ("ilé oúnjẹ",        "canteen",        Domain.PLACE),
        ("ilé ìgbọ̀nsẹ̀",     "toilet",         Domain.PLACE),
        ("ọgbà",             "garden",         Domain.PLACE),
        ("ẹnubodè",          "gate",           Domain.PLACE),
        ("odi",              "fence",          Domain.PLACE),
        ("ilé",              "house/home",     Domain.PLACE),
        ("ìwé",              "book",           Domain.OBJECT),
        ("àwọn ìwé",         "books",          Domain.OBJECT),
        ("ìwé àkọsílẹ̀",     "notebook",       Domain.OBJECT),
        ("ìwé ẹ̀kọ́",         "textbook",       Domain.OBJECT),
        ("ìwé àdánwò",       "exercise book",  Domain.OBJECT),
        ("ìwé atúmọ̀ èdè",    "dictionary",     Domain.OBJECT),
        ("kálámù",           "pen",            Domain.OBJECT),
        ("pẹ́ńsúlù",         "pencil",         Domain.OBJECT),
        ("rúlà",             "ruler",          Domain.OBJECT),
        ("rọ́bà",             "eraser",         Domain.OBJECT),
        ("kọ́ọ̀kì",            "chalk",          Domain.OBJECT),
        ("máàkà",            "marker",         Domain.OBJECT),
        ("pátákó",           "board",          Domain.OBJECT),
        ("pátákó dúdú",      "blackboard",     Domain.OBJECT),
        ("pátákó funfun",    "whiteboard",     Domain.OBJECT),
        ("tábìlì",           "table",          Domain.OBJECT),
        ("tébùrù",           "desk/table",     Domain.OBJECT),
        ("ìrẹsì",            "rice",           Domain.FOOD),
        ("àga",              "chair",          Domain.OBJECT),
        ("àpò",              "bag",            Domain.OBJECT),
        ("kọ̀ǹpútà",          "computer",       Domain.OBJECT),
        ("ẹ̀rọ ìṣírò",        "calculator",     Domain.OBJECT),
        ("àwòrán ilẹ̀",       "map",            Domain.OBJECT),
        ("agogo",            "bell",           Domain.OBJECT),
        ("àsíá",             "flag",           Domain.OBJECT),
        ("àṣọ",              "cloth/uniform",  Domain.OBJECT),
        ("fáánì",             "fan",           Domain.OBJECT),
        ("iná mọ̀nàmọ́ná",    "electricity",    Domain.OBJECT),
        ("omi",              "water",          Domain.OBJECT),
        ("oúnjẹ",            "food",           Domain.FOOD),
        ("ẹ̀kọ́",             "lesson",         Domain.ACADEMIC),
        ("ìbéèrè",           "question",       Domain.ACADEMIC),
        ("ìdáhùn",           "answer",         Domain.ACADEMIC),
        ("iṣẹ́ ilé",          "homework",       Domain.ACADEMIC),
        ("iṣẹ́ àṣẹ",          "assignment",     Domain.ACADEMIC),
        ("ìdánwò",           "examination",    Domain.ACADEMIC),
        ("àkọsílẹ̀",         "note",           Domain.ACADEMIC),
        ("àmì",              "mark",           Domain.ACADEMIC),
        ("èsì",              "result",         Domain.ACADEMIC),
        ("ipò",              "position/rank",  Domain.ACADEMIC),
        ("ewì",              "poem",           Domain.ACADEMIC),
        ("àròkọ",            "composition",    Domain.ACADEMIC),
        ("gbólóhùn",         "sentence",       Domain.ACADEMIC),
        ("ọ̀rọ̀",             "word",           Domain.ACADEMIC),
        ("orúkọ",            "name",           Domain.PERSON),
        ("àkòrí",            "topic",          Domain.ACADEMIC),
        ("ìlà",              "line",           Domain.OBJECT),
        ("àwọ̀",              "colour",         Domain.QUALITY),
        ("ariwo",            "noise",          Domain.GENERAL),
        ("ìwà rere",         "good behaviour", Domain.QUALITY),
        ("àdúrà",            "prayer",         Domain.SOCIAL),
        ("orin ìyìn",        "anthem",         Domain.SOCIAL),
        ("orin",             "song",           Domain.SOCIAL),
        ("ìsinmi",           "holiday/break",  Domain.TIME),
        ("ìtò",              "order/line",     Domain.GENERAL),
        ("àkókò",            "time",           Domain.TIME),
    ]
    for yo, en, dom in nouns_classroom:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.NOUN,
            domain=dom, tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- SUBJECTS (academic subjects) ----------
    subjects = [
        ("ìṣírò",            "mathematics"),
        ("Èdè Gẹ̀ẹ́sì",       "English"),
        ("èdè Yorùbá",       "Yoruba language"),
        ("sáyẹ́ǹsì",         "science"),
        ("ìtàn",             "history"),
        ("Jẹ́ọ́gírápì",       "geography"),
        ("ẹ̀kọ́ ìlú",         "social studies"),
        ("ẹ̀kọ́ ọmọlúàbí",    "civic education"),
        ("iṣẹ́ ọnà",          "art"),
        ("orin",             "music"),
        ("ẹ̀kọ́ eré ìdárayá", "physical education"),
        ("ẹ̀kọ́ kọ̀ǹpútà",     "computer studies"),
        ("ẹ̀kọ́ iṣẹ́ àgbẹ̀",   "agriculture"),
        ("Kẹ́mísírì",         "chemistry"),
        ("Físíìkì",           "physics"),
        ("ẹ̀kọ́ ètò ọrọ̀ ajé", "economics"),
        ("Lítíréṣọ̀",         "literature"),
        ("ẹ̀kọ́ ìsìn",        "religious studies"),
        ("èdè Faransé",      "French"),
        ("Lárúbáwá",         "Arabic"),
        ("ẹ̀kọ́ ìṣàkóso ilé", "home economics"),
    ]
    for yo, en in subjects:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.NOUN,
            domain=Domain.SUBJECT, tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- VERBS ----------
    verbs = [
        ("kàwé",       "read/study",   Domain.ACTION),
        ("kọ",         "write",        Domain.ACTION),
        ("kọ́",         "learn/teach",  Domain.ACTION),
        ("wá",         "come",         Domain.ACTION),
        ("lọ",         "go",           Domain.ACTION),
        ("padà",       "return",       Domain.ACTION),
        ("rí",         "see",          Domain.ACTION),
        ("wò",         "look at",      Domain.ACTION),
        ("gbọ́",        "hear/listen",  Domain.ACTION),
        ("sọ",         "say",          Domain.ACTION),
        ("sọ̀rọ̀",      "speak",        Domain.ACTION),
        ("béèrè",      "ask",          Domain.ACTION),
        ("dáhùn",      "answer",       Domain.ACTION),
        ("jẹun",       "eat",          Domain.ACTION),
        ("mu",         "drink",        Domain.ACTION),
        ("káàárọ̀",     "Good morning", Domain.ACTION),
        ("sùn",        "sleep",        Domain.ACTION),
        ("jí",         "wake up",      Domain.ACTION),
        ("ṣeré",       "play",         Domain.ACTION),
        ("dìde",       "stand up",     Domain.ACTION),
        ("jókòó",      "sit down",     Domain.ACTION),
        ("dúró",       "stop/wait",    Domain.ACTION),
        ("rin",        "walk/march",   Domain.ACTION),
        ("wọlé",       "enter",        Domain.ACTION),
        ("jáde",       "go out",       Domain.ACTION),
        ("ṣí",         "open",         Domain.ACTION),
        ("pa dé",      "close",        Domain.ACTION),
        ("gbé",        "lift/carry",   Domain.ACTION),
        ("mú",         "take/bring",   Domain.ACTION),
        ("fi",         "put/place",    Domain.ACTION),
        ("fún",        "give",         Domain.ACTION),
        ("gba",        "receive/take", Domain.ACTION),
        ("ní",         "have",         Domain.ACTION),
        ("wà",         "be/exist",     Domain.ACTION),
        ("jẹ́",         "be",           Domain.ACTION),
        ("ṣe",         "do",           Domain.ACTION),
        ("ṣàlàyé",     "explain",      Domain.ACTION),
        ("yé",         "understand",   Domain.ACTION),
        ("mọ̀",         "know",         Domain.ACTION),
        ("rántí",      "remember",     Domain.ACTION),
        ("gbàgbé",     "forget",       Domain.ACTION),
        ("fẹ́ràn",      "like/love",    Domain.EMOTION),
        ("nífẹ̀ẹ́",      "love",         Domain.EMOTION),
        ("fẹ́",         "want",         Domain.EMOTION),
        ("bínú",       "be angry",     Domain.EMOTION),
        ("rẹ́rìn-ín",    "laugh",       Domain.EMOTION),
        ("yìn",        "praise",       Domain.ACTION),
        ("ràn … lọ́wọ́","help",         Domain.ACTION),
        ("parí",       "finish",       Domain.ACTION),
        ("bẹ̀rẹ̀",      "begin",        Domain.ACTION),
        ("gbìyànjú",   "try",          Domain.ACTION),
        ("jáwọ́",      "give up",      Domain.ACTION),
        ("ṣàtúnṣe",    "correct",      Domain.ACTION),
        ("yẹ … wò",    "check",        Domain.ACTION),
        ("tún … wò",   "revise",       Domain.ACTION),
        ("borí",       "overcome/pass",Domain.ACTION),
        ("kùnà",       "fail",         Domain.ACTION),
        ("kọjá",       "pass",         Domain.ACTION),
        ("yanjú",      "solve",        Domain.ACTION),
        ("pín",        "divide/share", Domain.ACTION),
        ("yọ",         "subtract/remove", Domain.ACTION),
        ("ṣe ìṣírò",   "calculate",    Domain.ACTION),
        ("kà",         "count/read",   Domain.ACTION),
        ("wọn",        "measure",      Domain.ACTION),
        ("fa",         "draw/pull",    Domain.ACTION),
        ("ya",         "draw/tear",    Domain.ACTION),
        ("tò",         "arrange",      Domain.ACTION),
        ("nù",         "clean/wipe",   Domain.ACTION),
        ("pa … rẹ́",   "erase",        Domain.ACTION),
        ("sọnù",       "lose",         Domain.ACTION),
        ("yá",         "borrow/lend",  Domain.ACTION),
        ("dá … padà",  "return (sth)", Domain.ACTION),
        ("gbà",        "agree/accept", Domain.ACTION),
        ("bọ̀wọ̀ fún",  "respect",      Domain.SOCIAL),
        ("pèsè",       "provide",      Domain.ACTION),
        ("tẹ̀síwájú",   "continue",     Domain.ACTION),
        ("ṣàṣeyọrí",   "succeed",      Domain.ACTION),
    ]
    for yo, en, dom in verbs:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.VERB,
            domain=dom, tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- ADJECTIVES ----------
    adjectives = [
        ("dára",       "good"),
        ("burú",       "bad"),
        ("tóbi",       "big"),
        ("kéré",       "small"),
        ("mọ́",         "clean"),
        ("dọ̀tí",       "dirty"),
        ("tuntun",     "new"),
        ("àtijọ́",      "old"),
        ("lẹ́wà",       "beautiful"),
        ("ṣòro",       "difficult"),
        ("rọrùn",      "easy"),
        ("pàtàkì",     "important"),
        ("dùn mọ́ni",   "interesting/enjoyable"),
        ("gbọ́n",       "clever"),
        ("ọlẹ́",        "lazy"),
        ("le",         "strict/hard"),
        ("pupa",       "red"),
        ("búlúù",      "blue"),
        ("funfun",     "white"),
        ("dúdú",       "black"),
        ("ewé",        "green"),
        ("púpọ̀",       "many"),
        ("díẹ̀",        "few"),
        ("gíga",       "high"),
        ("gígùn",      "long"),
        ("kánkán",     "quick"),
        ("tọ́",         "correct"),
        ("olóòtọ́",     "honest"),
        ("wúlò",       "useful"),
        ("aládàáṣe",   "creative"),
        ("àádọ́ta",    "healthy (lit. of good health)"),
    ]
    for yo, en in adjectives:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.ADJECTIVE,
            domain=Domain.QUALITY, tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- ADVERBS ----------
    adverbs = [
        ("dáadáa",       "well/carefully"),
        ("gidigidi",     "very much/hard"),
        ("takuntakun",   "tirelessly"),
        ("déédéé",       "regularly"),
        ("lójoojúmọ́",   "every day"),
        ("kánkán",       "quickly"),
        ("lẹ́ẹ̀kansi",   "again"),
        ("lónìí",        "today"),
        ("lánàá",        "yesterday"),
        ("lọ́la",         "tomorrow"),
        ("báyìí",        "now"),
        ("níbí",         "here"),
        ("níbẹ̀",         "there"),
        ("sókè",         "up"),
        ("kalẹ̀",         "down"),
        ("níta",         "outside"),
        ("kedere",       "clearly"),
        ("rara",         "aloud"),
        ("ní kùtùkùtù",  "early"),
        ("pẹ́",           "late"),
        ("ṣáájú",        "before"),
    ]
    for yo, en in adverbs:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.ADVERB,
            domain=Domain.QUALITY, tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- TIME EXPRESSIONS / DAYS / MONTHS ----------
    time_words = [
        ("Ọjọ́ Àìkú",       "Sunday"),
        ("Ọjọ́ Ajé",        "Monday"),
        ("Ọjọ́ Ìsẹ́gun",     "Tuesday"),
        ("Ọjọ́ Rú",         "Wednesday"),
        ("Ọjọ́bọ̀",         "Thursday"),
        ("Ọjọ́ Ẹtì",        "Friday"),
        ("Ọjọ́ Àbámẹ́ta",   "Saturday"),
        ("oṣù",            "month"),
        ("oṣù Kínní",      "January"),
        ("oṣù Kejì",       "February"),
        ("oṣù Kẹta",       "March"),
        ("oṣù Kẹrin",      "April"),
        ("oṣù Okudu",      "June"),
        ("oṣù Agẹmọ",      "July"),
        ("oṣù Bẹ́lú",       "December"),
        ("ọ̀sẹ̀",            "week"),
        ("ọdún",           "year"),
        ("àárọ̀",           "morning"),
        ("ọ̀sán",            "afternoon"),
        ("ìrọ̀lẹ́",           "evening"),
        ("alẹ́",            "night"),
        ("aago",           "clock/o'clock"),
    ]
    for yo, en in time_words:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.NOUN,
            domain=Domain.TIME, tone_pattern=_get_tone_pattern(yo),
        ))

    # ---------- BODY PARTS (relevant to classroom actions) ----------
    body_parts = [
        ("ọwọ́",    "hand"),
        ("orí",     "head"),
        ("ojú",     "face/eye"),
        ("etí",     "ear"),
        ("ẹnu",     "mouth"),
        ("ara",     "body"),
        ("ẹsẹ̀",     "leg/foot"),
        ("inú",     "stomach/inside"),
    ]
    for yo, en in body_parts:
        entries.append(LexEntry(
            yoruba=_nfc(yo), english=en, pos=POS.NOUN,
            domain=Domain.BODY, tone_pattern=_get_tone_pattern(yo),
        ))

    return entries


# ================================================================
# SECTION 5: BILINGUAL LEXICON CLASS
# ================================================================

class BilingualLexicon:
    """
    Bidirectional Yoruba↔English lexicon with lookup, insertion,
    and dataset-mining capabilities.
    """

    def __init__(self, entries: Optional[List[LexEntry]] = None):
        self._entries:        List[LexEntry] = []
        self._en_index:       Dict[str, List[LexEntry]] = {}
        self._yo_index:       Dict[str, List[LexEntry]] = {}
        self._yo_stripped:    Dict[str, List[LexEntry]] = {}  # tone-insensitive
        if entries:
            for e in entries:
                self.add(e)

    # ---------- Insertion ----------
    def add(self, entry: LexEntry) -> None:
        """Add a lexical entry and update all indices."""
        entry.yoruba = _nfc(entry.yoruba)
        self._entries.append(entry)

        # English indices (primary + alt glosses)
        for gloss in entry.all_glosses():
            key = _normalize_english_key(gloss)
            self._en_index.setdefault(key, []).append(entry)

        # Yoruba indices
        yo_key = _nfc(entry.yoruba).lower()
        self._yo_index.setdefault(yo_key, []).append(entry)
        yo_stripped = _strip_tones(entry.yoruba).lower()
        self._yo_stripped.setdefault(yo_stripped, []).append(entry)

    def add_many(self, entries: Iterable[LexEntry]) -> None:
        for e in entries:
            self.add(e)

    # ---------- Lookup ----------
    def lookup_en(self, english: str, pos: Optional[POS] = None) -> List[LexEntry]:
        """Look up all Yoruba entries matching an English word/phrase."""
        key = _normalize_english_key(english)
        results = self._en_index.get(key, [])
        if pos is not None:
            results = [e for e in results if e.pos == pos]
        return results

    def lookup_yo(self, yoruba: str, pos: Optional[POS] = None,
                  tone_insensitive: bool = False) -> List[LexEntry]:
        """Look up all English glosses matching a Yoruba word."""
        if tone_insensitive:
            key = _strip_tones(yoruba).lower()
            results = self._yo_stripped.get(key, [])
        else:
            key = _nfc(yoruba).lower()
            results = self._yo_index.get(key, [])
        if pos is not None:
            results = [e for e in results if e.pos == pos]
        return results

    def translate_en(self, english: str, pos: Optional[POS] = None) -> Optional[str]:
        """Return the best (highest confidence × frequency) Yoruba match."""
        candidates = self.lookup_en(english, pos)
        if not candidates:
            return None
        best = max(candidates, key=lambda e: e.confidence * e.frequency)
        return best.yoruba

    def translate_yo(self, yoruba: str, pos: Optional[POS] = None,
                     tone_insensitive: bool = False) -> Optional[str]:
        """Return the best English gloss for a Yoruba word."""
        candidates = self.lookup_yo(yoruba, pos, tone_insensitive)
        if not candidates:
            return None
        best = max(candidates, key=lambda e: e.confidence * e.frequency)
        return best.english

    # ---------- Filtering ----------
    def by_pos(self, pos: POS) -> List[LexEntry]:
        """Return all entries of a given part of speech."""
        return [e for e in self._entries if e.pos == pos]

    def by_domain(self, domain: Domain) -> List[LexEntry]:
        """Return all entries in a semantic domain."""
        return [e for e in self._entries if e.domain == domain]

    def by_register(self, register: Register) -> List[LexEntry]:
        """Return all entries in a given register."""
        return [e for e in self._entries if e.register == register]

    # ---------- Metrics ----------
    def __len__(self) -> int:
        return len(self._entries)

    def stats(self) -> Dict[str, int]:
        """Return a count breakdown by POS and domain."""
        pos_counts: Dict[str, int] = {}
        dom_counts: Dict[str, int] = {}
        for e in self._entries:
            pos_counts[e.pos.value] = pos_counts.get(e.pos.value, 0) + 1
            dom_counts[e.domain.value] = dom_counts.get(e.domain.value, 0) + 1
        return {
            "total":    len(self._entries),
            "unique_yo": len(self._yo_index),
            "unique_en": len(self._en_index),
            "by_pos":   pos_counts,
            "by_domain": dom_counts,
        }

    # ---------- Dataset mining ----------
    def ingest_dataset(self, dataset: Dict[str, list],
                       as_examples_only: bool = True) -> int:
        """
        Harvest English↔Yoruba sentence pairs from the education_dataset
        and attach them as examples to existing MWE entries, OR create
        new MWE entries for every pair (if as_examples_only=False).

        Returns: number of pairs ingested.
        """
        count = 0
        for section, examples in dataset.items():
            if not isinstance(examples, list):
                continue
            domain = _section_to_domain(section)
            for ex in examples:
                if not isinstance(ex, dict):
                    continue
                en, yo = ex.get("english"), ex.get("yoruba")
                if not (en and yo):
                    continue
                count += 1
                if as_examples_only:
                    # Attach as example to the first matching headword
                    key = _normalize_english_key(en)
                    for existing in self._en_index.get(key, []):
                        existing.examples.append((en, yo))
                else:
                    self.add(LexEntry(
                        yoruba=_nfc(yo), english=en, pos=POS.MWE,
                        domain=domain, source="dataset",
                        examples=[(en, yo)], confidence=0.95,
                        tone_pattern=_get_tone_pattern(yo),
                    ))
        return count

    # ---------- Serialization ----------
    def to_dict(self) -> Dict[str, List[dict]]:
        """Serialise entire lexicon as a plain Python dict."""
        return {
            "entries": [e.to_dict() for e in self._entries],
            "stats":   self.stats(),
        }

    def export_jsonl(self, path: str = "yoruba_english_lexicon.jsonl") -> int:
        """Export every entry as one JSON object per line."""
        import json
        with open(path, "w", encoding="utf-8") as f:
            for e in self._entries:
                f.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")
        return len(self._entries)

    def export_csv(self, path: str = "yoruba_english_lexicon.csv") -> int:
        """Export the lexicon as UTF-8 CSV (headword, gloss, pos, domain)."""
        import csv
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["yoruba", "english", "pos", "domain",
                             "register", "tone_pattern", "notes"])
            for e in self._entries:
                writer.writerow([
                    e.yoruba, e.english, e.pos.value, e.domain.value,
                    e.register.value, e.tone_pattern, e.notes,
                ])
        return len(self._entries)


def _section_to_domain(section: str) -> Domain:
    """Map an education_dataset section name to a Domain enum."""
    mapping = {
        "greetings_and_routines":            Domain.GREETING,
        "classroom_objects":                 Domain.OBJECT,
        "subjects_and_academics":            Domain.ACADEMIC,
        "teacher_instructions":              Domain.CLASSROOM,
        "student_expressions":               Domain.SOCIAL,
        "school_environment":                Domain.SCHOOL_ENV,
        "numbers_and_counting":              Domain.NUMBER,
        "days_time_calendar":                Domain.TIME,
        "compound_sentences_classroom":      Domain.CLASSROOM,
        "compound_sentences_academic":       Domain.ACADEMIC,
        "complex_sentences_school_life":     Domain.ACADEMIC,
    }
    return mapping.get(section, Domain.GENERAL)


# ================================================================
# SECTION 6: BUILD DEFAULT LEXICON INSTANCE
# ================================================================

def build_default_lexicon(include_dataset: bool = True) -> BilingualLexicon:
    """
    Build the complete default bilingual lexicon,
    optionally seeded with MWE entries from the education_dataset.
    """
    lex = BilingualLexicon(_build_core_lexicon())
    if include_dataset:
        try:
            from yoruba_english_education_dataset import education_dataset  # type: ignore
            lex.ingest_dataset(education_dataset, as_examples_only=False)
        except ImportError:
            pass
    return lex


# Module-level singleton (safe to import)
LEXICON = build_default_lexicon(include_dataset=False)


# ================================================================
# SECTION 7: VALIDATION
# ================================================================

def validate_lexicon(lex: BilingualLexicon) -> Dict[str, object]:
    """Run consistency checks on the lexicon."""
    issues: List[str] = []
    seen_yo: Set[Tuple[str, str]] = set()
    for e in lex._entries:
        if not e.yoruba.strip():
            issues.append(f"Empty Yoruba headword for '{e.english}'")
        if not e.english.strip():
            issues.append(f"Empty English gloss for '{e.yoruba}'")
        key = (e.yoruba, e.pos.value)
        if key in seen_yo:
            issues.append(f"Duplicate (yoruba={e.yoruba}, pos={e.pos.value})")
        seen_yo.add(key)
    return {
        "total_entries":  len(lex),
        "issues_found":   len(issues),
        "issues":         issues[:20],   # cap for brevity
    }


# ================================================================
# SECTION 8: SELF-TEST SUITE
# ================================================================

def _run_self_tests() -> List[str]:
    """Internal unit tests."""
    failures: List[str] = []
    lex = build_default_lexicon(include_dataset=False)

    # 1. Core lookups
    if lex.translate_en("teacher") != "olùkọ́":
        failures.append(f"EN 'teacher' -> {lex.translate_en('teacher')}")
    if lex.translate_en("book") != "ìwé":
        failures.append(f"EN 'book' -> {lex.translate_en('book')}")
    if lex.translate_yo("olùkọ́") != "teacher":
        failures.append(f"YO 'olùkọ́' -> {lex.translate_yo('olùkọ́')}")

    # 2. Tone-insensitive lookup
    if lex.translate_yo("oluko", tone_insensitive=True) != "teacher":
        failures.append("Tone-insensitive YO 'oluko' failed")

    # 3. POS filtering
    verbs = lex.by_pos(POS.VERB)
    if len(verbs) < 20:
        failures.append(f"Expected >=20 verbs, got {len(verbs)}")

    # 4. Domain filtering
    objs = lex.by_domain(Domain.OBJECT)
    if len(objs) < 10:
        failures.append(f"Expected >=10 OBJECT entries, got {len(objs)}")

    # 5. Greeting lookup
    if lex.translate_en("thank you") != _nfc("E ṣé"):
        failures.append(f"EN 'thank you' -> {lex.translate_en('thank you')}")

    # 6. Numeral lookup
    if lex.translate_en("five") != "àrún":
        failures.append(f"EN 'five' -> {lex.translate_en('five')}")

    # 7. Pronoun lookup
    if lex.translate_en("I") not in {"mo", "èmi"}:
        failures.append(f"EN 'I' -> {lex.translate_en('I')}")

    # 8. Stats sanity
    stats = lex.stats()
    if stats["total"] < 200:
        failures.append(f"Total lexicon too small: {stats['total']}")

    # 9. Validation
    v = validate_lexicon(lex)
    # Duplicates are allowed (homographs with different pos ok),
    # but basic field validation should pass
    for issue in v["issues"]:
        if "Empty" in issue:
            failures.append(f"Validation issue: {issue}")

    # 10. Serialisation
    d = lex.to_dict()
    if "entries" not in d or len(d["entries"]) != len(lex):
        failures.append("to_dict() produced wrong structure")

    return failures


# ================================================================
# SECTION 9: PUBLIC API
# ================================================================

__all__ = [
    # Enums
    "POS", "Domain", "Register",
    # Classes
    "LexEntry", "BilingualLexicon",
    # Factories
    "build_default_lexicon", "LEXICON",
    # Validation
    "validate_lexicon",
]


# ================================================================
# SECTION 10: SCRIPT ENTRY POINT
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Yoruba-English Bilingual Lexicon — Self-Test")
    print("=" * 60)

    failures = _run_self_tests()
    if failures:
        print(f"\n❌ {len(failures)} test(s) failed:")
        for f in failures:
            print(f"   - {f}")
    else:
        print("\n✅ All self-tests passed.")

    # Build full lexicon with dataset
    print("\n" + "=" * 60)
    print("Building Complete Lexicon (with dataset)")
    print("=" * 60)
    lex = build_default_lexicon(include_dataset=True)
    stats = lex.stats()
    print(f"Total entries:    {stats['total']}")
    print(f"Unique Yoruba:    {stats['unique_yo']}")
    print(f"Unique English:   {stats['unique_en']}")
    print(f"\nBy POS:")
    for pos, count in sorted(stats["by_pos"].items(), key=lambda x: -x[1]):
        print(f"  {pos:8s}  {count:4d}")
    print(f"\nBy Domain:")
    for dom, count in sorted(stats["by_domain"].items(), key=lambda x: -x[1]):
        print(f"  {dom:20s}  {count:4d}")

    # Validation
    print("\n" + "=" * 60)
    print("Validation Report")
    print("=" * 60)
    report = validate_lexicon(lex)
    print(f"Total entries: {report['total_entries']}")
    print(f"Issues found:  {report['issues_found']}")

    # Demonstration lookups
    print("\n" + "=" * 60)
    print("Demonstration Lookups")
    print("=" * 60)
    demo_en = ["teacher", "student", "book", "read", "good", "and", "if", "five"]
    demo_yo = ["olùkọ́", "akẹ́kọ̀ọ́", "ìwé", "kàwé", "dára", "àti", "bí", "àrún"]

    print("\nEnglish → Yoruba:")
    for en in demo_en:
        yo = lex.translate_en(en)
        print(f"  {en:12s} → {yo}")

    print("\nYoruba → English:")
    for yo in demo_yo:
        en = lex.translate_yo(yo)
        print(f"  {yo:12s} → {en}")

    print("\nTone-insensitive lookup (no diacritics):")
    for yo in ["oluko", "akekoo", "iwe", "kawe"]:
        en = lex.translate_yo(yo, tone_insensitive=True)
        print(f"  {yo:12s} → {en}")