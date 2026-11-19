"""
================================================================
YORUBA-ENGLISH RULE-BASED MACHINE TRANSLATION SYSTEM
================================================================
Architecture: Modular Pipeline (Preprocessing -> Tokenization ->
              Dictionary Lookup -> Rule Application -> Post-processing)
Compatible with: education_dataset (Python dict format)
Author: Software Architect
Python: 3.8+
================================================================
"""

import re
import json
import unicodedata
from collections import defaultdict, Counter
from difflib import SequenceMatcher
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from yoruba_english_education_dataset import education_dataset   


# ================================================================
# SECTION 1: CONFIGURATION & ENUMS
# ================================================================

class Direction(Enum):
    """Translation direction enumeration."""
    EN_TO_YO = "english_to_yoruba"
    YO_TO_EN = "yoruba_to_english"


class MatchType(Enum):
    """Type of translation match found."""
    EXACT = "exact"
    FUZZY = "fuzzy"
    PARTIAL = "partial"
    RULE_BASED = "rule_based"
    DICTIONARY = "dictionary"
    UNKNOWN = "unknown"


@dataclass
class TranslationResult:
    """Container for translation output with metadata."""
    source: str
    translation: str
    direction: str
    match_type: str
    confidence: float
    section: Optional[str] = None
    alternatives: List[str] = field(default_factory=list)
    tokens_processed: int = 0
    rules_applied: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "translation": self.translation,
            "direction": self.direction,
            "match_type": self.match_type,
            "confidence": round(self.confidence, 3),
            "section": self.section,
            "alternatives": self.alternatives,
            "tokens_processed": self.tokens_processed,
            "rules_applied": self.rules_applied,
        }


# ================================================================
# SECTION 2: TEXT PREPROCESSING MODULE
# ================================================================

class TextPreprocessor:
    """Handles text normalization, cleaning, and diacritic management."""

    PUNCTUATION_PATTERN = re.compile(r'([.,!?;:"\'()])')
    MULTI_SPACE_PATTERN = re.compile(r'\s+')

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """Normalize unicode to NFC form (preserves Yoruba diacritics)."""
        return unicodedata.normalize('NFC', text)

    @staticmethod
    def strip_diacritics(text: str) -> str:
        """Remove diacritics for fuzzy matching (NOT for display)."""
        nfd = unicodedata.normalize('NFD', text)
        return ''.join(c for c in nfd if not unicodedata.combining(c))

    @classmethod
    def clean(cls, text: str) -> str:
        """Clean and normalize input text."""
        if not isinstance(text, str):
            text = str(text)
        text = cls.normalize_unicode(text.strip())
        text = cls.MULTI_SPACE_PATTERN.sub(' ', text)
        return text

    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        """Tokenize text preserving punctuation as separate tokens."""
        text = cls.clean(text)
        spaced = cls.PUNCTUATION_PATTERN.sub(r' \1 ', text)
        tokens = [t for t in spaced.split() if t]
        return tokens

    @staticmethod
    def detokenize(tokens: List[str]) -> str:
        """Reconstruct text from tokens with proper punctuation spacing."""
        text = ' '.join(tokens)
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        text = re.sub(r'\(\s+', '(', text)
        text = re.sub(r'\s+\)', ')', text)
        return text.strip()

    @staticmethod
    def preserve_case(source: str, target: str) -> str:
        """Preserve capitalization pattern from source to target."""
        if not source or not target:
            return target
        if source[0].isupper() and target and target[0].islower():
            target = target[0].upper() + target[1:]
        if source.isupper() and len(source) > 1:
            target = target.upper()
        return target


# ================================================================
# SECTION 3: DICTIONARY BUILDER
# ================================================================

class BilingualDictionary:
    """Builds and manages bidirectional translation dictionaries."""

    def __init__(self):
        self.en_to_yo: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        self.yo_to_en: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        self.en_to_yo_normalized: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        self.yo_to_en_normalized: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        self.word_level_en_yo: Dict[str, Counter] = defaultdict(Counter)
        self.word_level_yo_en: Dict[str, Counter] = defaultdict(Counter)
        self.sections: Dict[str, int] = {}
        self.total_entries: int = 0

    def _normalize_key(self, text: str) -> str:
        """Create normalized lookup key (lowercase, no diacritics, no punct)."""
        text = TextPreprocessor.clean(text).lower()
        text = TextPreprocessor.strip_diacritics(text)
        text = re.sub(r'[.,!?;:"\'()]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _extract_word_pairs(self, en_text: str, yo_text: str) -> None:
        """Build word-level alignment heuristics for unseen phrases."""
        en_tokens = [t.lower() for t in TextPreprocessor.tokenize(en_text)
                     if t.isalpha()]
        yo_tokens = [t.lower() for t in TextPreprocessor.tokenize(yo_text)
                     if any(ch.isalpha() for ch in t)]

        for en_tok in en_tokens:
            for yo_tok in yo_tokens:
                self.word_level_en_yo[en_tok][yo_tok] += 1
                self.word_level_yo_en[yo_tok][en_tok] += 1

    def build(self, dataset: Dict[str, Any]) -> None:
        """Build dictionaries from the education dataset."""
        for section, examples in dataset.items():
            if not isinstance(examples, list):
                continue

            section_count = 0
            for example in examples:
                if not isinstance(example, dict):
                    continue
                en = example.get("english", "").strip()
                yo = example.get("yoruba", "").strip()
                if not en or not yo:
                    continue

                en_clean = TextPreprocessor.clean(en)
                yo_clean = TextPreprocessor.clean(yo)

                self.en_to_yo[en_clean].append((yo_clean, section))
                self.yo_to_en[yo_clean].append((en_clean, section))

                en_norm = self._normalize_key(en_clean)
                yo_norm = self._normalize_key(yo_clean)
                self.en_to_yo_normalized[en_norm].append((yo_clean, section))
                self.yo_to_en_normalized[yo_norm].append((en_clean, section))

                self._extract_word_pairs(en_clean, yo_clean)

                section_count += 1
                self.total_entries += 1

            self.sections[section] = section_count

    def lookup_exact(self, text: str, direction: Direction) -> Optional[Tuple[str, str]]:
        """Exact dictionary lookup. Returns (translation, section) or None."""
        text_clean = TextPreprocessor.clean(text)
        source_dict = (self.en_to_yo if direction == Direction.EN_TO_YO
                       else self.yo_to_en)
        if text_clean in source_dict and source_dict[text_clean]:
            return source_dict[text_clean][0]
        return None

    def lookup_normalized(self, text: str, direction: Direction) -> Optional[Tuple[str, str]]:
        """Case/diacritic-insensitive lookup."""
        key = self._normalize_key(text)
        source_dict = (self.en_to_yo_normalized if direction == Direction.EN_TO_YO
                       else self.yo_to_en_normalized)
        if key in source_dict and source_dict[key]:
            return source_dict[key][0]
        return None

    def lookup_word(self, word: str, direction: Direction) -> Optional[str]:
        """Look up a single word using word-level statistics."""
        word_lower = word.lower()
        source = (self.word_level_en_yo if direction == Direction.EN_TO_YO
                  else self.word_level_yo_en)
        if word_lower in source and source[word_lower]:
            return source[word_lower].most_common(1)[0][0]
        return None

    def get_alternatives(self, text: str, direction: Direction, limit: int = 3) -> List[str]:
        """Return alternative translations for a given input."""
        text_clean = TextPreprocessor.clean(text)
        source_dict = (self.en_to_yo if direction == Direction.EN_TO_YO
                       else self.yo_to_en)
        entries = source_dict.get(text_clean, [])
        seen = []
        for translation, _ in entries:
            if translation not in seen:
                seen.append(translation)
            if len(seen) >= limit:
                break
        return seen

    def stats(self) -> Dict[str, Any]:
        """Return dictionary build statistics."""
        return {
            "total_entries": self.total_entries,
            "unique_english_phrases": len(self.en_to_yo),
            "unique_yoruba_phrases": len(self.yo_to_en),
            "sections": self.sections,
            "word_level_en_entries": len(self.word_level_en_yo),
            "word_level_yo_entries": len(self.word_level_yo_en),
        }


# ================================================================
# SECTION 4: FUZZY MATCHING MODULE
# ================================================================

class FuzzyMatcher:
    """Finds closest match when exact lookup fails."""

    def __init__(self, dictionary: BilingualDictionary,
                 threshold: float = 0.75):
        self.dictionary = dictionary
        self.threshold = threshold

    @staticmethod
    def similarity(a: str, b: str) -> float:
        """Compute string similarity ratio (0.0 to 1.0)."""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def find_best_match(self, text: str, direction: Direction
                        ) -> Optional[Tuple[str, str, float]]:
        """Find best fuzzy match. Returns (translation, section, score)."""
        text_clean = TextPreprocessor.clean(text)
        text_norm = self.dictionary._normalize_key(text_clean)

        source_dict = (self.dictionary.en_to_yo if direction == Direction.EN_TO_YO
                       else self.dictionary.yo_to_en)

        best_score = 0.0
        best_translation = None
        best_section = None

        text_len = len(text_norm)

        for candidate, entries in source_dict.items():
            cand_norm = self.dictionary._normalize_key(candidate)
            # Length-based pruning for performance
            if abs(len(cand_norm) - text_len) > max(10, text_len * 0.5):
                continue
            score = self.similarity(text_norm, cand_norm)
            if score > best_score:
                best_score = score
                best_translation = entries[0][0]
                best_section = entries[0][1]

        if best_score >= self.threshold and best_translation:
            return (best_translation, best_section, best_score)
        return None


# ================================================================
# SECTION 5: GRAMMAR RULES ENGINE
# ================================================================

class YorubaGrammarRules:
    """
    Rule-based transformations for Yoruba linguistic patterns.
    Based on Bamgbose (1966), Awobuluyi (1978), and Yusuf (1998).
    """

    # Pronoun mappings (subject position)
    EN_TO_YO_PRONOUNS = {
        "i": "mo", "you": "o", "he": "ó", "she": "ó",
        "it": "ó", "we": "a", "they": "wọ́n",
    }

    YO_TO_EN_PRONOUNS = {
        "mo": "I", "mi": "me/my", "o": "you", "ó": "he/she/it",
        "a": "we", "wa": "us/our", "wọ́n": "they", "wọn": "them/their",
    }

    # Tense/aspect markers
    YORUBA_TENSE_MARKERS = {
        "present_continuous": "ń",
        "future": "yóò",
        "past_completed": "ti",
        "habitual": "máa ń",
    }

    # Common greeting patterns
    GREETING_PATTERNS = [
        (r'^good morning', 'E káàárọ̀'),
        (r'^good afternoon', 'E kú ọ̀sán'),
        (r'^good evening', 'E kú ìrọ̀lẹ́'),
        (r'^good night', 'O dáàrọ̀'),
        (r'^thank you', 'E ṣé'),
        (r'^welcome', 'E kú àbọ̀'),
        (r'^goodbye', 'O dàbọ̀'),
    ]

    # Question word mappings
    QUESTION_WORDS_EN_YO = {
        "what": "kín",
        "who": "ta",
        "where": "níbo",
        "when": "nígbà wo",
        "why": "kí ló dé",
        "how": "báwo",
        "which": "èwo",
    }

    @classmethod
    def is_question(cls, text: str) -> bool:
        """Detect if text is a question."""
        text_lower = text.lower().strip()
        if text.endswith('?'):
            return True
        question_starters = ['what', 'who', 'where', 'when', 'why',
                             'how', 'which', 'is', 'are', 'do', 'does',
                             'can', 'may', 'will', 'should']
        first_word = text_lower.split()[0] if text_lower.split() else ""
        return first_word in question_starters

    @classmethod
    def apply_greeting_rule(cls, text: str) -> Optional[str]:
        """Try to match a greeting pattern."""
        text_lower = text.lower()
        for pattern, replacement in cls.GREETING_PATTERNS:
            if re.match(pattern, text_lower):
                return replacement
        return None

    @classmethod
    def translate_pronoun(cls, word: str, direction: Direction) -> Optional[str]:
        """Translate a pronoun word."""
        word_lower = word.lower()
        if direction == Direction.EN_TO_YO:
            return cls.EN_TO_YO_PRONOUNS.get(word_lower)
        return cls.YO_TO_EN_PRONOUNS.get(word_lower)

    @classmethod
    def translate_question_word(cls, word: str) -> Optional[str]:
        """Translate English question words."""
        return cls.QUESTION_WORDS_EN_YO.get(word.lower())


# ================================================================
# SECTION 6: TRANSLATION PIPELINE
# ================================================================

class TranslationPipeline:
    """
    Main translation orchestrator.
    Pipeline stages:
      1. Preprocess input
      2. Try exact match
      3. Try normalized match
      4. Try fuzzy match
      5. Apply grammar rules (greetings, questions)
      6. Fall back to word-level translation
      7. Post-process output
    """

    def __init__(self, dataset: Dict[str, Any],
                 fuzzy_threshold: float = 0.75):
        self.dictionary = BilingualDictionary()
        self.dictionary.build(dataset)
        self.fuzzy = FuzzyMatcher(self.dictionary, threshold=fuzzy_threshold)
        self.rules = YorubaGrammarRules()
        self.preprocessor = TextPreprocessor()

    def _translate_sentence(self, sentence: str,
                            direction: Direction) -> TranslationResult:
        """Translate a single sentence through the pipeline."""
        rules_applied = []
        source = sentence
        cleaned = self.preprocessor.clean(sentence)

        # Stage 1: Exact match
        exact = self.dictionary.lookup_exact(cleaned, direction)
        if exact:
            translation, section = exact
            rules_applied.append("exact_match")
            alternatives = self.dictionary.get_alternatives(cleaned, direction)
            return TranslationResult(
                source=source,
                translation=translation,
                direction=direction.value,
                match_type=MatchType.EXACT.value,
                confidence=1.0,
                section=section,
                alternatives=[a for a in alternatives if a != translation],
                tokens_processed=len(self.preprocessor.tokenize(cleaned)),
                rules_applied=rules_applied,
            )

        # Stage 2: Normalized match (case/diacritic insensitive)
        normalized = self.dictionary.lookup_normalized(cleaned, direction)
        if normalized:
            translation, section = normalized
            rules_applied.append("normalized_match")
            return TranslationResult(
                source=source,
                translation=translation,
                direction=direction.value,
                match_type=MatchType.EXACT.value,
                confidence=0.95,
                section=section,
                tokens_processed=len(self.preprocessor.tokenize(cleaned)),
                rules_applied=rules_applied,
            )

        # Stage 3: Fuzzy match
        fuzzy_result = self.fuzzy.find_best_match(cleaned, direction)
        if fuzzy_result:
            translation, section, score = fuzzy_result
            rules_applied.append(f"fuzzy_match(score={score:.2f})")
            return TranslationResult(
                source=source,
                translation=translation,
                direction=direction.value,
                match_type=MatchType.FUZZY.value,
                confidence=score,
                section=section,
                tokens_processed=len(self.preprocessor.tokenize(cleaned)),
                rules_applied=rules_applied,
            )

        # Stage 4: Rule-based (greetings)
        if direction == Direction.EN_TO_YO:
            greeting = self.rules.apply_greeting_rule(cleaned)
            if greeting:
                rules_applied.append("greeting_rule")
                return TranslationResult(
                    source=source,
                    translation=greeting + ".",
                    direction=direction.value,
                    match_type=MatchType.RULE_BASED.value,
                    confidence=0.70,
                    tokens_processed=len(self.preprocessor.tokenize(cleaned)),
                    rules_applied=rules_applied,
                )

        # Stage 5: Word-level fallback
        tokens = self.preprocessor.tokenize(cleaned)
        translated_tokens = []
        hit_count = 0
        for tok in tokens:
            if re.match(r'^[.,!?;:"\'()]$', tok):
                translated_tokens.append(tok)
                continue
            # Try pronoun
            pron = self.rules.translate_pronoun(tok, direction)
            if pron:
                translated_tokens.append(pron)
                hit_count += 1
                continue
            # Try question word
            if direction == Direction.EN_TO_YO:
                qw = self.rules.translate_question_word(tok)
                if qw:
                    translated_tokens.append(qw)
                    hit_count += 1
                    continue
            # Try word-level dictionary
            word_trans = self.dictionary.lookup_word(tok, direction)
            if word_trans:
                translated_tokens.append(word_trans)
                hit_count += 1
            else:
                translated_tokens.append(f"[{tok}]")

        if hit_count > 0:
            rules_applied.append(f"word_level({hit_count}/{len(tokens)})")
            result_text = self.preprocessor.detokenize(translated_tokens)
            result_text = self.preprocessor.preserve_case(cleaned, result_text)
            confidence = hit_count / max(len(tokens), 1) * 0.6
            return TranslationResult(
                source=source,
                translation=result_text,
                direction=direction.value,
                match_type=MatchType.PARTIAL.value,
                confidence=confidence,
                tokens_processed=len(tokens),
                rules_applied=rules_applied,
            )

        # Stage 6: Unknown
        return TranslationResult(
            source=source,
            translation=f"[UNTRANSLATED: {source}]",
            direction=direction.value,
            match_type=MatchType.UNKNOWN.value,
            confidence=0.0,
            tokens_processed=len(tokens),
            rules_applied=["no_match_found"],
        )

    def translate(self, text: str,
                  direction: Direction = Direction.EN_TO_YO
                  ) -> TranslationResult:
        """Public translate method."""
        if not text or not text.strip():
            return TranslationResult(
                source=text, translation="",
                direction=direction.value,
                match_type=MatchType.UNKNOWN.value,
                confidence=0.0,
            )
        return self._translate_sentence(text, direction)

    def translate_batch(self, texts: List[str],
                        direction: Direction = Direction.EN_TO_YO
                        ) -> List[TranslationResult]:
        """Translate a list of texts."""
        return [self.translate(t, direction) for t in texts]

    def translate_document(self, document: str,
                           direction: Direction = Direction.EN_TO_YO
                           ) -> List[TranslationResult]:
        """Split a document into sentences and translate each."""
        sentences = re.split(r'(?<=[.!?])\s+', document.strip())
        sentences = [s for s in sentences if s.strip()]
        return self.translate_batch(sentences, direction)


# ================================================================
# SECTION 7: EVALUATION & QUALITY MODULE
# ================================================================

class TranslationEvaluator:
    """Evaluate translation quality against the dataset."""

    def __init__(self, pipeline: TranslationPipeline,
                 dataset: Dict[str, Any]):
        self.pipeline = pipeline
        self.dataset = dataset

    def _collect_pairs(self) -> List[Dict[str, str]]:
        pairs = []
        for section, examples in self.dataset.items():
            if not isinstance(examples, list):
                continue
            for ex in examples:
                if isinstance(ex, dict) and "english" in ex and "yoruba" in ex:
                    pairs.append({
                        "section": section,
                        "english": ex["english"],
                        "yoruba": ex["yoruba"],
                    })
        return pairs

    def evaluate(self, direction: Direction = Direction.EN_TO_YO,
                 sample_size: Optional[int] = None) -> Dict[str, Any]:
        """Run evaluation and return accuracy metrics."""
        pairs = self._collect_pairs()
        if sample_size:
            pairs = pairs[:sample_size]

        total = len(pairs)
        exact_hits = 0
        high_conf = 0
        match_type_counts = Counter()

        for pair in pairs:
            if direction == Direction.EN_TO_YO:
                src, expected = pair["english"], pair["yoruba"]
            else:
                src, expected = pair["yoruba"], pair["english"]

            result = self.pipeline.translate(src, direction)
            match_type_counts[result.match_type] += 1

            expected_norm = self.pipeline.dictionary._normalize_key(expected)
            got_norm = self.pipeline.dictionary._normalize_key(result.translation)
            if expected_norm == got_norm:
                exact_hits += 1
            if result.confidence >= 0.85:
                high_conf += 1

        return {
            "direction": direction.value,
            "total_evaluated": total,
            "exact_matches": exact_hits,
            "exact_match_accuracy": round(exact_hits / total * 100, 2) if total else 0,
            "high_confidence_translations": high_conf,
            "high_confidence_rate": round(high_conf / total * 100, 2) if total else 0,
            "match_type_distribution": dict(match_type_counts),
        }


# ================================================================
# SECTION 8: SYSTEM FACADE (MAIN API)
# ================================================================

class YorubaEnglishTranslator:
    """
    Main facade class for the translation system.
    Compatible with the education_dataset Python format.

    Usage:
        from translator import YorubaEnglishTranslator
        from your_dataset_file import education_dataset

        translator = YorubaEnglishTranslator(education_dataset)
        result = translator.en_to_yo("Good morning, teacher.")
        print(result.translation)
    """

    VERSION = "1.0.0"

    def __init__(self, dataset: Dict[str, Any],
                 fuzzy_threshold: float = 0.75,
                 verbose: bool = False):
        self.verbose = verbose
        if verbose:
            print(f"[Translator v{self.VERSION}] Building pipeline...")
        self.pipeline = TranslationPipeline(dataset, fuzzy_threshold)
        self.evaluator = TranslationEvaluator(self.pipeline, dataset)
        if verbose:
            stats = self.pipeline.dictionary.stats()
            print(f"[Translator] Loaded {stats['total_entries']} entries "
                  f"across {len(stats['sections'])} sections.")

    def en_to_yo(self, text: str) -> TranslationResult:
        """Translate English to Yoruba."""
        return self.pipeline.translate(text, Direction.EN_TO_YO)

    def yo_to_en(self, text: str) -> TranslationResult:
        """Translate Yoruba to English."""
        return self.pipeline.translate(text, Direction.YO_TO_EN)

    def translate_document_en_to_yo(self, document: str) -> List[TranslationResult]:
        return self.pipeline.translate_document(document, Direction.EN_TO_YO)

    def translate_document_yo_to_en(self, document: str) -> List[TranslationResult]:
        return self.pipeline.translate_document(document, Direction.YO_TO_EN)

    def batch_translate(self, texts: List[str],
                        direction: str = "en_to_yo") -> List[TranslationResult]:
        dir_enum = (Direction.EN_TO_YO if direction == "en_to_yo"
                    else Direction.YO_TO_EN)
        return self.pipeline.translate_batch(texts, dir_enum)

    def evaluate(self, direction: str = "en_to_yo",
                 sample_size: Optional[int] = None) -> Dict[str, Any]:
        dir_enum = (Direction.EN_TO_YO if direction == "en_to_yo"
                    else Direction.YO_TO_EN)
        return self.evaluator.evaluate(dir_enum, sample_size)

    def stats(self) -> Dict[str, Any]:
        return self.pipeline.dictionary.stats()

    def export_results(self, results: List[TranslationResult],
                       path: str) -> None:
        """Export translation results to JSONL."""
        with open(path, "w", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(r.to_dict(), ensure_ascii=False) + "\n")


# ================================================================
# SECTION 9: DEMO / SELF-TEST
# ================================================================

def _demo():
    """
    Demonstration using the education_dataset.
    Import the dataset from your file or paste it in the same module.
    """
    # ---- Import the dataset ----
    # If this file lives beside the dataset file:
    #   from yoruba_dataset import education_dataset
    # For self-contained demo, we build a minimal sample:
    sample_dataset = {
        "greetings_and_routines": [
            {"english": "Good morning, teacher.", "yoruba": "E káàárọ̀, olùkọ́."},
            {"english": "Thank you, teacher.", "yoruba": "E ṣé, olùkọ́."},
            {"english": "Stand up.", "yoruba": "E dìde."},
            {"english": "Sit down.", "yoruba": "E jókòó."},
        ],
        "student_expressions": [
            {"english": "I understand.", "yoruba": "Mo yé mi."},
            {"english": "I do not understand.", "yoruba": "Kò yé mi."},
            {"english": "I have a question.", "yoruba": "Mo ní ìbéèrè kan."},
        ],
    }

    translator = YorubaEnglishTranslator(sample_dataset, verbose=True)

    print("\n" + "=" * 60)
    print("DICTIONARY STATS")
    print("=" * 60)
    print(json.dumps(translator.stats(), indent=2, ensure_ascii=False))

    print("\n" + "=" * 60)
    print("ENGLISH -> YORUBA TRANSLATIONS")
    print("=" * 60)
    test_sentences_en = [
        "Good morning, teacher.",
        "Thank you, teacher.",
        "Stand up.",
        "good morning teacher",       # case/punct variation -> normalized match
        "I understand.",
        "I have a question.",
        "Hello world.",                # unknown -> partial/fallback
    ]
    for sent in test_sentences_en:
        res = translator.en_to_yo(sent)
        print(f"\nEN: {res.source}")
        print(f"YO: {res.translation}")
        print(f"    [match={res.match_type}, conf={res.confidence:.2f}, "
              f"rules={res.rules_applied}]")

    print("\n" + "=" * 60)
    print("YORUBA -> ENGLISH TRANSLATIONS")
    print("=" * 60)
    test_sentences_yo = [
        "E káàárọ̀, olùkọ́.",
        "Mo yé mi.",
        "E dìde.",
        "Kò yé mi.",
    ]
    for sent in test_sentences_yo:
        res = translator.yo_to_en(sent)
        print(f"\nYO: {res.source}")
        print(f"EN: {res.translation}")
        print(f"    [match={res.match_type}, conf={res.confidence:.2f}]")

    print("\n" + "=" * 60)
    print("EVALUATION (EN -> YO)")
    print("=" * 60)
    metrics = translator.evaluate(direction="en_to_yo")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


# The legacy implementation above is retained for audit. All imports resolve
# to this facade, which has one lexicon and one ordered rule path.
from unified_pipeline import UnifiedTranslator as _UnifiedTranslator


class YorubaEnglishTranslator:
    """Public application interface for the unified runtime pipeline."""
    VERSION = _UnifiedTranslator.VERSION

    def __init__(self, dataset=None, fuzzy_threshold=0.86, verbose=False):
        self.pipeline = _UnifiedTranslator(fuzzy_threshold=fuzzy_threshold)
        self.dataset = dataset or education_dataset
        if verbose:
            print(f"[Translator v{self.VERSION}] Loaded {self.stats()['total_entries']} unified lexical entries.")

    def en_to_yo(self, text):
        return self.pipeline.translate(text, "en_to_yo")

    def yo_to_en(self, text):
        return self.pipeline.translate(text, "yo_to_en")

    def batch_translate(self, texts, direction="en_to_yo"):
        translate = self.en_to_yo if direction == "en_to_yo" else self.yo_to_en
        return [translate(text) for text in texts]

    def translate_document_en_to_yo(self, document):
        return [self.en_to_yo(sentence) for sentence in re.split(r"(?<=[.!?])\s+", document.strip()) if sentence]

    def translate_document_yo_to_en(self, document):
        return [self.yo_to_en(sentence) for sentence in re.split(r"(?<=[.!?])\s+", document.strip()) if sentence]

    def stats(self):
        return self.pipeline.stats()

    def evaluate(self, direction="en_to_yo", sample_size=None):
        pairs = [(ex["english"], ex["yoruba"]) for examples in self.dataset.values() for ex in examples]
        pairs = pairs[:sample_size] if sample_size else pairs
        exact = 0
        for english, yoruba in pairs:
            result = self.en_to_yo(english) if direction == "en_to_yo" else self.yo_to_en(yoruba)
            expected = yoruba if direction == "en_to_yo" else english
            if result.translation.rstrip(".?!").casefold() == expected.rstrip(".?!").casefold():
                exact += 1
        return {"direction": direction, "total_evaluated": len(pairs), "exact_matches": exact,
                "exact_match_accuracy": round(100 * exact / len(pairs), 2) if pairs else 0}

if __name__ == "__main__":
    # ── Initialize the translator with the full dataset ──
    translator = YorubaEnglishTranslator(education_dataset, verbose=True)

    # ── Print dictionary stats ──
    print("\n" + "=" * 60)
    print("DICTIONARY STATS")
    print("=" * 60)
    print(json.dumps(translator.stats(), indent=2, ensure_ascii=False))

    # ── English → Yoruba ──
    print("\n" + "=" * 60)
    print("ENGLISH -> YORUBA")
    print("=" * 60)
    test_en = [
        "Good morning, teacher.",
        "Stand up.",
        "Open your book.",
        "I understand.",
        "What is two plus three?",
        "The school is big.",
    ]
    for sent in test_en:
        res = translator.en_to_yo(sent)
        print(f"\n  EN: {res.source}")
        print(f"  YO: {res.translation}")
        print(f"      [match={res.match_type}, conf={res.confidence:.2f}]")

    # ── Yoruba → English ──
    print("\n" + "=" * 60)
    print("YORUBA -> ENGLISH")
    print("=" * 60)
    test_yo = [
        "E káàárọ̀, olùkọ́.",
        "E dìde.",
        "Mo yé mi.",
        "Ilé ẹ̀kọ́ tóbi.",
    ]
    for sent in test_yo:
        res = translator.yo_to_en(sent)
        print(f"\n  YO: {res.source}")
        print(f"  EN: {res.translation}")
        print(f"      [match={res.match_type}, conf={res.confidence:.2f}]")

    # ── Full Evaluation ──
    print("\n" + "=" * 60)
    print("EVALUATION")
    print("=" * 60)
    metrics = translator.evaluate(direction="en_to_yo")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
