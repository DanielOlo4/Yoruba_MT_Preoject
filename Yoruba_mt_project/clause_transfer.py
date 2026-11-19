"""Controlled subject-initial English to Yorùbá clause transfer."""
import re

from english_morphology_rules import analyse_word
from yoruba_verb_grammar import realise_predicate, resolve_verb

LOCATIVES = {
    "in front of": "níwájú", "behind": "lẹ́yìn", "inside": "nínú",
    "under": "lábẹ́", "on": "lórí", "in": "nínú", "at": "ní",
}
QUANTIFIERS = {
    "one": "kan", "two": "méjì", "three": "mẹ́ta", "four": "mẹ́rin",
    "five": "márùn-ún", "many": "púpọ̀", "some": "kan", "all": "gbogbo",
}
TIME = {"yesterday": "lánàá", "tomorrow": "lọ́la", "today": "lónìí"}
ARTICLES = {"a", "an", "the"}
NOUNS = {"N", "NOUN", "PROPN"}
VERBS = {"V", "VERB"}
BE = {"am", "is", "are", "was", "were"}
HAVE = {"has", "have", "had"}
DO = {"do", "does", "did"}
FUTURE = {"will", "shall"}


def locative(words):
    for english, yoruba in LOCATIVES.items():
        parts = english.split()
        if words[:len(parts)] == parts:
            return yoruba, len(parts)
    return "", 0


def nominal(words, lookup, pronouns):
    if not words:
        return "", []
    if len(words) == 1 and words[0] in pronouns:
        return pronouns[words[0]], []
    if words[-1] in TIME:
        core = nominal(words[:-1], lookup, pronouns)
        if core:
            return " ".join(filter(None, (core[0], TIME[words[-1]]))), core[1]
    marker, length = locative(words)
    if marker and length < len(words):
        complement = nominal(words[length:], lookup, pronouns)
        if complement:
            return f"{marker} {complement[0]}", ["relational_locative", *complement[1]]
    prefix = words[0]
    if prefix in ARTICLES or prefix in QUANTIFIERS:
        words = words[1:]
    variants = [" ".join(words)]
    if len(words) == 1:
        word = words[0]
        if word.endswith("s"):
            variants.append(word[:-1])
        if word.endswith("es"):
            variants.append(word[:-2])
        if word.endswith("ies"):
            variants.append(word[:-3] + "y")
    for variant in variants:
        entry = lookup(variant)
        if not entry or entry.pos not in NOUNS:
            continue
        noun = entry.yoruba
        if prefix in QUANTIFIERS and noun.startswith("àwọn "):
            noun = noun.removeprefix("àwọn ")
        if prefix in QUANTIFIERS:
            value = QUANTIFIERS[prefix]
            return (f"{value} {noun}" if prefix == "all" else f"{noun} {value}"), ["noun_quantifier_order"]
        return noun, ["article_zero"] if prefix in ARTICLES else []
    return None


def transfer_clause(text, lookup, pronouns):
    text = text.lower().replace("’", "'").strip()
    text = re.sub(r"\bwon't\b", "will not", text)
    text = re.sub(r"\b(do|does|did|is|are|was|were|has|have|had)n't\b", r"\1 not", text)
    if not re.fullmatch(r"[a-z0-9 -]+\.?", text):
        return None
    words = text.rstrip(".").split()
    for boundary in range(1, len(words)):
        subject = nominal(words[:boundary], lookup, pronouns)
        if not subject:
            continue
        head = words[boundary]
        index = boundary
        aspect, tense, negative = "simple", "present", False
        if head in BE | HAVE | DO | FUTURE:
            index += 1
            if words[index:index + 1] == ["not"]:
                negative = True
                index += 1
            if index == len(words):
                continue
            form = analyse_word(words[index]).form
            if head in BE:
                if locative(words[index:])[0]:
                    complement = nominal(words[index:], lookup, pronouns)
                    if complement:
                        predicate = realise_predicate(subject[0], "sí" if negative else "wà", negative=negative)
                        result = f"{predicate} {complement[0]}"
                        return result, ["locative_copula", *subject[1], *complement[1]]
                if form != "progressive":
                    continue
                aspect = "progressive"
            elif head in HAVE:
                if form in {"past", "participle"} or words[index] == "read":
                    aspect = "perfect"
                elif negative:
                    continue
                else:
                    index = boundary
            elif head in FUTURE:
                aspect, tense = "future", "future"
            if head in {"did", "was", "were", "had"}:
                tense = "past"
        if words[index] in {"usually", "habitually"} and aspect == "simple":
            aspect = "habitual"
            index += 1
            if index == len(words):
                continue
        surface = words[index]
        analysis = analyse_word(surface)
        if index == boundary and (analysis.form == "past" or (surface == "read" and words[-1] == "yesterday")):
            tense = "past"
        rest = words[index + 1:]
        if aspect == "perfect" and negative and rest[-1:] == ["yet"]:
            rest = rest[:-1]
        complement = nominal(rest, lookup, pronouns)
        if complement is None:
            continue
        has_object = bool(rest and rest[0] not in TIME and not locative(rest)[0])
        lemma = "have_possession" if surface in HAVE and aspect == "simple" else analysis.lemma
        verb, serial = resolve_verb(lemma, has_object=has_object)
        if not verb:
            entry = lookup(analysis.lemma) or lookup(surface)
            if not entry or entry.pos not in VERBS:
                continue
            verb = entry.yoruba
        predicate = realise_predicate(subject[0], verb, aspect=aspect, negative=negative)
        result = " ".join(filter(None, (predicate, complement[0], serial)))
        polarity = "negative" if negative else "affirmative"
        return result, [f"english_{tense}", "yoruba_future" if tense == "future" else "yoruba_nonfuture",
                        f"{aspect}_{polarity}", *subject[1], *complement[1]]
    return None
