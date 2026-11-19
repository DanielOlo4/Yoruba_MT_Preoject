"""Single runtime pipeline for the Yorùbá-English rule-based translator.

Data precedence: reviewed sentence pairs, curated core lexicon, CSV dictionary.
The same lexicon instance powers exact matches, phrase matching and word lookup.
"""
from __future__ import annotations

import csv
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

from yoruba_english_education_dataset import education_dataset
from yoruba_lexicon import build_default_lexicon
from yoruba_morphology_rule import apply_elision
from english_morphology_rules import analyse_clause as analyse_english_inflection, analyse_word, inflect
from yoruba_verb_grammar import resolve_verb
from verb_form_lexicon import VerbFormLexicon
from clause_transfer import transfer_clause

WORD_RE = re.compile(r"[\wÀ-ÖØ-öø-ÿ'ọ́ẹ̀̀-]+|[.,!?;:]", re.UNICODE)
PUNCT = {".", ",", "!", "?", ";", ":"}
EN_PRONOUNS = {"i": "mo", "you": "o", "he": "ó", "she": "ó", "it": "ó", "we": "a", "they": "wọ́n", "me": "mi", "us": "wa", "them": "wọn"}
EN_POSSESSIVES = {"my": "mi", "your": "rẹ", "his": "rẹ̀", "her": "rẹ̀", "our": "wa", "their": "wọn"}
YO_PRONOUNS = {value: key for key, value in EN_PRONOUNS.items()}
YO_PRONOUNS.update({"mi": "me", "wa": "us", "wọn": "them", "ẹ": "you", "yín": "your", "rẹ": "your", "rẹ̀": "his/her"})
FUNCTION_EN_YO = {"and": "àti", "or": "tàbí", "but": "ṣùgbọ́n", "if": "bí", "because": "nítorí pé", "with": "pẹ̀lú", "from": "láti", "to": "sí", "in": "ní", "on": "lórí", "at": "ní", "for": "fún", "not": "kò", "can": "lè", "must": "gbọ́dọ̀", "will": "yóò", "what": "kín", "who": "ta", "where": "níbo", "when": "nígbà wo", "why": "kí ló dé", "how": "báwo", "this": "yìí", "that": "ìyẹn", "these": "wọ̀nyí", "those": "wọ̀nyẹn"}
FUNCTION_YO_EN = {value: key for key, value in FUNCTION_EN_YO.items()}
POS_MAP = {"NOUN": "N", "VERB": "V", "ADJ": "ADJ", "ADV": "ADV", "PRON": "PRON", "DET": "DET", "ADP": "PREP", "CCONJ": "CONJ", "SCONJ": "CONJ", "INTJ": "INTJ", "NUM": "NUM", "PART": "PART", "AUX": "AUX", "PROPN": "PROPN"}


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def key(text: str) -> str:
    text = nfc(text).lower().strip()
    text = re.sub(r"[.,!?;:]", "", text)
    return re.sub(r"\s+", " ", text)


def tokens(text: str) -> list[str]:
    return WORD_RE.findall(nfc(text).strip())


def detokenize(items: Iterable[str]) -> str:
    output = " ".join(items)
    output = re.sub(r"\s+([.,!?;:])", r"\1", output)
    output = re.sub(r"\s+", " ", output).strip()
    return output


@dataclass
class Entry:
    english: str
    yoruba: str
    pos: str = "X"
    source: str = "dictionary"
    priority: int = 1
    alternatives: list[str] = field(default_factory=list)


class UnifiedLexicon:
    """One indexed lexical store rather than separate, conflicting dictionaries."""
    def __init__(self) -> None:
        self.en: dict[str, list[Entry]] = defaultdict(list)
        self.yo: dict[str, list[Entry]] = defaultdict(list)
        self.entries: list[Entry] = []

    def add(self, entry: Entry) -> None:
        if not entry.english.strip() or not entry.yoruba.strip():
            return
        entry.english, entry.yoruba = nfc(entry.english.strip()), nfc(entry.yoruba.strip())
        self.entries.append(entry)
        self.en[key(entry.english)].append(entry)
        self.yo[key(entry.yoruba)].append(entry)

    def best(self, text: str, direction: str) -> Entry | None:
        index = self.en if direction == "en_to_yo" else self.yo
        candidates = index.get(key(text), [])
        return max(candidates, key=lambda item: item.priority) if candidates else None

    def alternatives(self, text: str, direction: str) -> list[str]:
        index = self.en if direction == "en_to_yo" else self.yo
        found = []
        for entry in sorted(index.get(key(text), []), key=lambda item: item.priority, reverse=True):
            value = entry.yoruba if direction == "en_to_yo" else entry.english
            if value not in found:
                found.append(value)
        return found

    def longest(self, stream: list[str], position: int, direction: str, maximum: int = 6) -> tuple[Entry | None, int]:
        for size in range(min(maximum, len(stream) - position), 0, -1):
            candidate = " ".join(stream[position:position + size])
            entry = self.best(candidate, direction)
            if entry:
                return entry, size
        return None, 0

    def stats(self) -> dict[str, Any]:
        return {"total_entries": len(self.entries), "unique_english_phrases": len(self.en), "unique_yoruba_phrases": len(self.yo), "sources": {source: sum(1 for entry in self.entries if entry.source == source) for source in sorted({entry.source for entry in self.entries})}}


def build_lexicon(csv_path: str | Path | None = None) -> UnifiedLexicon:
    lexicon = UnifiedLexicon()
    for section, examples in education_dataset.items():
        for example in examples:
            lexicon.add(Entry(example["english"], example["yoruba"], "MWE", f"dataset:{section}", 30))
    for entry in build_default_lexicon(include_dataset=False)._entries:
        lexicon.add(Entry(entry.english, entry.yoruba, entry.pos.value, "curated", 20, entry.glosses))
    path = Path(csv_path or Path(__file__).with_name("yoruba_english_rule_based_lexicon.csv"))
    if path.exists():
        with path.open(encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                lexicon.add(Entry(row.get("english", ""), row.get("yoruba", ""), POS_MAP.get(row.get("pos", ""), row.get("pos", "X")), "csv_dictionary", 10, [item for item in row.get("alternatives", "").split(" | ") if item]))
    return lexicon


@dataclass
class TranslationResult:
    source: str
    translation: str
    direction: str
    match_type: str
    confidence: float
    section: str | None = None
    alternatives: list[str] = field(default_factory=list)
    tokens_processed: int = 0
    rules_applied: list[str] = field(default_factory=list)
    def to_dict(self) -> dict[str, Any]: return self.__dict__.copy()


class UnifiedTranslator:
    VERSION = "2.0.0"
    def __init__(self, fuzzy_threshold: float = 0.86) -> None:
        self.lexicon = build_lexicon()
        self.verb_forms = VerbFormLexicon()
        self.fuzzy_threshold = fuzzy_threshold

    def _exact(self, text: str, direction: str) -> TranslationResult | None:
        entry = self.lexicon.best(text, direction)
        if direction == "en_to_yo" and len(tokens(text)) == 1:
            analysis = analyse_word(text)
            morphology = {"past": "past_or_completed", "participle": "past_participle_or_perfect", "progressive": "progressive", "third_sg": "third_person_present", "base": "base"}.get(analysis.form, "base")
            form = self.verb_forms.english(text, lemma=analysis.lemma, morphology=morphology, has_object=True)
            # An inflected English surface must take precedence over a raw
            # dictionary gloss with the same spelling, for example eating.
            if form and analysis.form != "base":
                return TranslationResult(text, form.yoruba_surface, direction, "verb_form_lexicon", 0.96, form.source, [], len(tokens(text)), ["verb_form_exact_lookup"])
        if not entry:
            if direction == "en_to_yo":
                form = self.verb_forms.english(text, has_object=True)
                if form:
                    return TranslationResult(text, form.yoruba_surface, direction, "verb_form_lexicon", 0.96, form.source, [], len(tokens(text)), ["verb_form_exact_lookup"])
            return None
        translation = entry.yoruba if direction == "en_to_yo" else entry.english
        return TranslationResult(text, translation, direction, "exact", 1.0, entry.source, self.lexicon.alternatives(text, direction)[1:5], len(tokens(text)), ["unified_exact_lookup"])

    def _fuzzy(self, text: str, direction: str) -> TranslationResult | None:
        source = self.lexicon.en if direction == "en_to_yo" else self.lexicon.yo
        target = key(text)
        if len(target) < 5 or len(target.split()) > 5:
            return None
        winner, score = None, 0.0
        for candidate in source:
            if abs(len(candidate) - len(target)) > max(4, len(target) // 3): continue
            value = SequenceMatcher(None, target, candidate).ratio()
            if value > score: winner, score = candidate, value
        if winner is None or score < self.fuzzy_threshold: return None
        entry = self.lexicon.best(winner, direction)
        translation = entry.yoruba if direction == "en_to_yo" else entry.english
        return TranslationResult(text, translation, direction, "fuzzy", score, entry.source, [], len(tokens(text)), [f"fuzzy_lookup:{score:.2f}"])

    def _en_to_yo(self, text: str) -> TranslationResult:
        stream, output, rules, hits, unknown = tokens(text), [], [], 0, 0
        analyses = list(analyse_english_inflection(stream).analyses)
        is_question = text.strip().endswith("?")
        first_content = True
        i = 0
        while i < len(stream):
            token = stream[i]
            if token in PUNCT:
                i += 1; continue
            lowered = token.lower()
            analysis = analyses[i] if i < len(analyses) else None
            if lowered in {"a", "an", "the"}:
                rules.append("article_drop"); i += 1; continue
            if lowered == "do" and first_content and i + 1 < len(stream) and stream[i + 1].lower() == "not":
                output.append("má"); rules.append("imperative_negation"); hits += 1; i += 2; continue
            if lowered in EN_PRONOUNS:
                output.append(EN_PRONOUNS[lowered]); hits += 1; i += 1; first_content = False; continue
            if lowered in EN_POSSESSIVES:
                # Possessives are postponed after their noun by the look-ahead
                # branch below when a lexical noun is available.
                following, following_size = self.lexicon.longest(stream, i + 1, "en_to_yo", 1)
                if following and following.pos in {"N", "NOUN"}:
                    output.extend([following.yoruba, EN_POSSESSIVES[lowered]])
                    rules.append("possessive_noun_reorder"); hits += 1 + following_size; i += 1 + following_size; continue
                output.append(EN_POSSESSIVES[lowered]); hits += 1; i += 1; continue
            # Recover English auxiliary structure before bilingual lookup.
            # This retains the lexical verb while mapping English TAM to its
            # Yorùbá construction.
            if analysis and analysis.role == "AUX":
                next_form = analyses[i + 1].form if i + 1 < len(analyses) else ""
                if analysis.lemma == "have" and next_form in {"past", "participle"}:
                    output.append("ti"); rules.append("perfect_auxiliary_to_ti"); hits += 1; i += 1; continue
                if analysis.lemma == "be" and next_form == "progressive":
                    output.append("ń"); rules.append("progressive_auxiliary_to_n"); hits += 1; i += 1; continue
                if analysis.lemma == "do":
                    rules.append("do_support_zero"); hits += 1; i += 1; continue
                # Copular be requires predicate-sensitive generation.  Leave
                # adjectival predicates unmarked, but retain wà before a
                # locative preposition.
                if analysis.lemma == "be":
                    if i + 1 < len(stream) and stream[i + 1].lower() in {"in", "on", "at", "under", "near", "here", "there"}:
                        output.append("wà")
                    rules.append("predicate_sensitive_copula"); hits += 1; i += 1; continue
            if lowered in FUNCTION_EN_YO:
                mapped = FUNCTION_EN_YO[lowered]
                if lowered == "will" and output: output.append(mapped); rules.append("future_marker")
                elif lowered in {"this", "that", "these", "those"}: output.append(mapped); rules.append("postnominal_demonstrative")
                else: output.append(mapped)
                hits += 1; i += 1; continue
            entry, size = self.lexicon.longest(stream, i, "en_to_yo")
            lemma = analysis.lemma if analysis else lowered
            has_object = i + 1 < len(stream) and stream[i + 1] not in PUNCT
            morphology = {"past": "past_or_completed", "participle": "past_participle_or_perfect", "progressive": "progressive", "third_sg": "third_person_present", "base": "base"}.get(analysis.form if analysis else "base", "base")
            form_entry = self.verb_forms.english(lowered, lemma=lemma, morphology=morphology, has_object=has_object)
            if not entry and lemma != lowered:
                entry, size = self.lexicon.longest([lemma], 0, "en_to_yo")
                if entry:
                    rules.append(f"english_inflection:{lowered}→{lemma}")
            if entry:
                value = entry.yoruba
                if form_entry:
                    value = form_entry.yoruba_lemma
                    marker = form_entry.tam_marker
                    if marker and analysis and analysis.form != "past" and marker not in output:
                        output.append(marker)
                    rules.append(f"verb_form_lexicon:{lowered}→{form_entry.yoruba_surface}")
                lexical, _serial_tail = resolve_verb(lemma, has_object=has_object)
                if lexical:
                    value = lexical
                # English adjective and possessive precede a noun; Yorùbá follows it.
                if i + size < len(stream):
                    following, following_size = self.lexicon.longest(stream, i + size, "en_to_yo", 1)
                    if entry.pos == "ADJ" and following and following.pos in {"N", "NOUN"}:
                        output.append(following.yoruba); output.append(value); rules.append("adj_noun_reorder"); hits += size + following_size; i += size + following_size; continue
                output.append(value); hits += size; i += size; first_content = False; continue
            if form_entry:
                marker = form_entry.tam_marker
                if marker and analysis and analysis.form != "past" and marker not in output:
                    output.append(marker)
                output.append(form_entry.yoruba_lemma)
                rules.append(f"verb_form_lexicon:{lowered}→{form_entry.yoruba_surface}")
                hits += 1; i += 1; first_content = False; continue
            lexical, _serial_tail = resolve_verb(lemma, has_object=i + 1 < len(stream) and stream[i + 1] not in PUNCT)
            if lexical:
                output.append(lexical); rules.append(f"verb_inventory:{lowered}→{lemma}")
                hits += 1; i += 1; first_content = False; continue
            output.append(f"[{token}]"); unknown += 1; i += 1
        if output and not is_question and text[:1].isupper() and stream and stream[0].lower() not in EN_PRONOUNS and stream[0].lower() not in {"i", "we", "they", "he", "she"}:
            # Polite classroom imperative only if the first translated token is a verb.
            first = self.lexicon.best(stream[0], "en_to_yo")
            if first and first.pos == "V": output.insert(0, "E"); rules.append("polite_imperative")
        if is_question and not output[:1] in (["níbo"], ["kín"], ["ta"], ["báwo"]): output.insert(0, "Ṣé"); rules.append("polar_question")
        terminal = "?" if is_question else ("!" if text.strip().endswith("!") else ".")
        result = apply_elision(detokenize(output))
        result = (result[:1].upper() + result[1:] if result else result) + terminal
        confidence = (hits / max(hits + unknown, 1)) * 0.72
        return TranslationResult(text, result, "en_to_yo", "rule_based" if hits else "unknown", confidence, None, [], len(stream), sorted(set(rules + ["unified_lexicon_transfer"])))

    def _yo_to_en(self, text: str) -> TranslationResult:
        stream, output, hits, unknown, i = tokens(text), [], 0, 0, 0
        pending_tam, subject = None, ""
        while i < len(stream):
            token = stream[i]
            if token in PUNCT: i += 1; continue
            lowered = token.lower()
            if lowered in YO_PRONOUNS:
                subject = YO_PRONOUNS[lowered]; output.append(subject); hits += 1; i += 1; continue
            if lowered == "ti": pending_tam = "perfect"; hits += 1; i += 1; continue
            if lowered == "ń": pending_tam = "progressive"; hits += 1; i += 1; continue
            if lowered in {"yóò", "yoo"}: pending_tam = "future"; hits += 1; i += 1; continue
            if lowered in FUNCTION_YO_EN: output.append(FUNCTION_YO_EN[lowered]); hits += 1; i += 1; continue
            entry, size = self.lexicon.longest(stream, i, "yo_to_en")
            form_entry = self.verb_forms.yoruba(lowered, has_object=i + 1 < len(stream) and stream[i + 1] not in PUNCT)
            if entry:
                lemma = form_entry.english_lemma.split()[0] if form_entry else entry.english.split()[0]
                if pending_tam == "perfect":
                    output.extend(["has" if subject in {"he", "she", "it"} else "have", inflect(lemma, "participle")])
                elif pending_tam == "progressive":
                    output.extend([{"i": "am", "you": "are", "we": "are", "they": "are"}.get(subject, "is"), inflect(lemma, "progressive")])
                elif pending_tam == "future": output.extend(["will", inflect(lemma, "base")])
                else: output.append(entry.english)
                pending_tam = None; hits += size; i += size; continue
            if form_entry:
                lemma = form_entry.english_lemma.split()[0]
                if pending_tam == "perfect": output.extend(["has" if subject in {"he", "she", "it"} else "have", inflect(lemma, "participle")])
                elif pending_tam == "progressive": output.extend([{"i": "am", "you": "are", "we": "are", "they": "are"}.get(subject, "is"), inflect(lemma, "progressive")])
                elif pending_tam == "future": output.extend(["will", inflect(lemma, "base")])
                else: output.append(lemma)
                pending_tam = None; hits += 1; i += 1; continue
            output.append(f"[{token}]"); unknown += 1; i += 1
        terminal = "?" if text.strip().endswith("?") else "."
        result = detokenize(output)
        result = result[:1].upper() + result[1:] if result else result
        return TranslationResult(text, result + terminal, "yo_to_en", "rule_based" if hits else "unknown", (hits / max(hits + unknown, 1)) * .72, None, [], len(stream), ["unified_lexicon_transfer"])

    def translate(self, text: str, direction: str) -> TranslationResult:
        text = nfc(str(text).strip())
        if not text: return TranslationResult(text, "", direction, "unknown", 0.0)
        exact = self._exact(text, direction)
        if exact:
            return exact
        if direction == "en_to_yo":
            clause = transfer_clause(text, lambda word: self.lexicon.best(word, direction), EN_PRONOUNS)
            if clause:
                output, rules = clause
                return TranslationResult(text, output[:1].upper() + output[1:] + ".", direction,
                                         "rule_based", .90, None, [], len(tokens(text)), rules)
        return self._fuzzy(text, direction) or (self._en_to_yo(text) if direction == "en_to_yo" else self._yo_to_en(text))

    def stats(self) -> dict[str, Any]: return self.lexicon.stats() | self.verb_forms.stats()
