"""English inflection analysis and controlled English surface generation.

The module is deliberately small, inspectable and rule based.  It recovers a
lemma before bilingual lookup, so *ate* and *brought* reach the same lexemes as
*eat* and *bring*.  Its clause analysis also separates lexical *have* from the
perfect auxiliary and lexical *be* from progressive and copular uses.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

TOKEN_RE = re.compile(r"[A-Za-z]+(?:n't)?|[.,!?;:]", re.UNICODE)


@dataclass(frozen=True)
class EnglishVerbForm:
    lemma: str
    past: str
    participle: str
    third_singular: str
    progressive: str


def _form(lemma: str, past: str, participle: str | None = None, third: str | None = None, progressive: str | None = None) -> EnglishVerbForm:
    return EnglishVerbForm(lemma, past, participle or past, third or f"{lemma}s", progressive or f"{lemma}ing")


# Frequent irregulars and high-value verbs in the project corpus.  Regular
# forms are handled below, so this table remains a transparent exception list.
IRREGULAR_FORMS = {
    form: record
    for record in (
        _form("be", "was", "been", "is", "being"),
        _form("have", "had", "had", "has", "having"),
        _form("do", "did", "done", "does", "doing"),
        _form("eat", "ate", "eaten", "eats", "eating"),
        _form("bring", "brought", "brought", "brings", "bringing"),
        _form("go", "went", "gone", "goes", "going"),
        _form("come", "came", "come", "comes", "coming"),
        _form("read", "read", "read", "reads", "reading"),
        _form("write", "wrote", "written", "writes", "writing"),
        _form("take", "took", "taken", "takes", "taking"),
        _form("give", "gave", "given", "gives", "giving"),
        _form("make", "made", "made", "makes", "making"),
        _form("see", "saw", "seen", "sees", "seeing"),
        _form("know", "knew", "known", "knows", "knowing"),
        _form("teach", "taught", "taught", "teaches", "teaching"),
        _form("learn", "learnt", "learnt", "learns", "learning"),
        _form("speak", "spoke", "spoken", "speaks", "speaking"),
        _form("say", "said", "said", "says", "saying"),
        _form("tell", "told", "told", "tells", "telling"),
        _form("get", "got", "gotten", "gets", "getting"),
        _form("buy", "bought", "bought", "buys", "buying"),
        _form("think", "thought", "thought", "thinks", "thinking"),
        _form("find", "found", "found", "finds", "finding"),
        _form("feel", "felt", "felt", "feels", "feeling"),
        _form("leave", "left", "left", "leaves", "leaving"),
        _form("keep", "kept", "kept", "keeps", "keeping"),
        _form("meet", "met", "met", "meets", "meeting"),
        _form("run", "ran", "run", "runs", "running"),
        _form("begin", "began", "begun", "begins", "beginning"),
        _form("become", "became", "become", "becomes", "becoming"),
        _form("break", "broke", "broken", "breaks", "breaking"),
        _form("choose", "chose", "chosen", "chooses", "choosing"),
        _form("drive", "drove", "driven", "drives", "driving"),
        _form("fall", "fell", "fallen", "falls", "falling"),
        _form("forget", "forgot", "forgotten", "forgets", "forgetting"),
        _form("hear", "heard", "heard", "hears", "hearing"),
        _form("hold", "held", "held", "holds", "holding"),
        _form("lose", "lost", "lost", "loses", "losing"),
        _form("pay", "paid", "paid", "pays", "paying"),
        _form("put", "put", "put", "puts", "putting"),
        _form("send", "sent", "sent", "sends", "sending"),
        _form("sit", "sat", "sat", "sits", "sitting"),
        _form("sleep", "slept", "slept", "sleeps", "sleeping"),
        _form("stand", "stood", "stood", "stands", "standing"),
        _form("understand", "understood", "understood", "understands", "understanding"),
        _form("wear", "wore", "worn", "wears", "wearing"),
        _form("win", "won", "won", "wins", "winning"),
    )
    for form in {record.lemma, record.past, record.participle, record.third_singular, record.progressive}
}
BE_FORMS = {"am", "is", "are", "was", "were", "been", "being", "be"}
MODALS = {"will", "shall", "can", "could", "may", "might", "must", "should", "would"}


@dataclass(frozen=True)
class TokenAnalysis:
    token: str
    lemma: str
    form: str = "base"             # base, past, participle, third_sg, progressive
    role: str = "LEX"              # LEX, AUX, MODAL, NEG, PARTICLE, PUNCT


def regular_forms(lemma: str) -> EnglishVerbForm:
    if lemma.endswith("y") and len(lemma) > 1 and lemma[-2] not in "aeiou":
        past, third = lemma[:-1] + "ied", lemma[:-1] + "ies"
    elif lemma.endswith("e"):
        past, third = lemma + "d", lemma + "s"
    elif lemma.endswith(("s", "x", "z", "ch", "sh", "o")):
        past, third = lemma + "ed", lemma + "es"
    else:
        past, third = lemma + "ed", lemma + "s"
    progressive = lemma[:-1] + "ing" if lemma.endswith("e") and not lemma.endswith(("ee", "ye", "oe")) else lemma + "ing"
    return EnglishVerbForm(lemma, past, past, third, progressive)


def analyse_word(token: str) -> TokenAnalysis:
    word = token.lower()
    if word in ".,!?;:": return TokenAnalysis(word, word, role="PUNCT")
    if word in {"not", "n't"}: return TokenAnalysis(word, "not", role="NEG")
    if word == "to": return TokenAnalysis(word, "to", role="PARTICLE")
    if word in MODALS: return TokenAnalysis(word, word, role="MODAL")
    if word in {"am", "is", "are"}: return TokenAnalysis(word, "be", "third_sg" if word == "is" else "base", "AUX")
    if word in {"was", "were"}: return TokenAnalysis(word, "be", "past", "AUX")
    if word in {"been"}: return TokenAnalysis(word, "be", "participle", "AUX")
    if word == "being": return TokenAnalysis(word, "be", "progressive", "AUX")
    if word in {"has", "had", "have"}: return TokenAnalysis(word, "have", "past" if word == "had" else ("third_sg" if word == "has" else "base"), "AUX")
    if word in {"does", "did", "do"}: return TokenAnalysis(word, "do", "past" if word == "did" else ("third_sg" if word == "does" else "base"), "AUX")
    record = IRREGULAR_FORMS.get(word)
    if record:
        form = "base"
        if word == record.past and word != record.lemma: form = "past"
        if word == record.participle and word not in {record.lemma, record.past}: form = "participle"
        if word == record.third_singular and word != record.lemma: form = "third_sg"
        if word == record.progressive and word != record.lemma: form = "progressive"
        return TokenAnalysis(word, record.lemma, form)
    if word.endswith("ies") and len(word) > 4: return TokenAnalysis(word, word[:-3] + "y", "third_sg")
    if word.endswith("ied") and len(word) > 4: return TokenAnalysis(word, word[:-3] + "y", "past")
    if word.endswith("ing") and len(word) > 5:
        stem = word[:-3]
        if len(stem) > 2 and stem[-1] == stem[-2] and stem[-1] not in "aeiou": stem = stem[:-1]
        return TokenAnalysis(word, stem, "progressive")
    if word.endswith("ed") and len(word) > 3:
        stem = word[:-2]
        if len(stem) > 2 and stem[-1] == stem[-2] and stem[-1] not in "aeiou": stem = stem[:-1]
        return TokenAnalysis(word, stem, "past")
    if word.endswith("es") and len(word) > 3: return TokenAnalysis(word, word[:-2] if word.endswith(("ses", "xes", "zes", "ches", "shes", "oes")) else word[:-1], "third_sg")
    if word.endswith("s") and len(word) > 3: return TokenAnalysis(word, word[:-1], "third_sg")
    return TokenAnalysis(word, word)


@dataclass(frozen=True)
class EnglishClauseFeatures:
    analyses: tuple[TokenAnalysis, ...]
    lexical_index: int | None
    tense: str = "present"
    aspect: str = "simple"
    polarity: str = "positive"
    modality: str | None = None

    @property
    def lexical_lemma(self) -> str | None:
        return self.analyses[self.lexical_index].lemma if self.lexical_index is not None else None


def analyse_clause(text_or_tokens: str | list[str]) -> EnglishClauseFeatures:
    raw = TOKEN_RE.findall(text_or_tokens) if isinstance(text_or_tokens, str) else text_or_tokens
    analyses = [analyse_word(token) for token in raw]
    polarity = "negative" if any(a.role == "NEG" for a in analyses) else "positive"
    modality = next((a.lemma for a in analyses if a.role == "MODAL"), None)
    lexical_candidates = [i for i, a in enumerate(analyses) if a.role == "LEX"]
    # An overt inflection is strong evidence of the verbal head.  For a bare
    # base form ("they eat rice"), a full POS tagger or bilingual lexicon makes
    # the final decision; the transfer pipeline still uses each token lemma.
    inflected_candidates = [i for i in lexical_candidates if analyses[i].form != "base"]
    supported_base = None
    for i, item in enumerate(analyses):
        if item.role == "MODAL" or item.lemma == "do":
            j = i + 1
            if j < len(analyses) and analyses[j].role == "NEG": j += 1
            if j < len(analyses) and analyses[j].role == "LEX":
                supported_base = j
    lexical_index = supported_base if supported_base is not None else (inflected_candidates[-1] if inflected_candidates else (lexical_candidates[-1] if lexical_candidates else None))
    tense, aspect = "present", "simple"
    if any(a.token in {"was", "were", "did", "had"} for a in analyses): tense = "past"
    if modality in {"will", "shall"}: tense = "future"
    has_perfect = any(a.lemma == "have" and a.role == "AUX" for a in analyses) and lexical_index is not None
    has_progressive = any(a.lemma == "be" and a.role == "AUX" for a in analyses) and lexical_index is not None and analyses[lexical_index].form == "progressive"
    if has_perfect and has_progressive: aspect = "perfect_progressive"
    elif has_perfect: aspect = "perfect"
    elif has_progressive: aspect = "progressive"
    elif lexical_index is not None and analyses[lexical_index].form == "past": tense = "past"
    return EnglishClauseFeatures(tuple(analyses), lexical_index, tense, aspect, polarity, modality)


def inflect(lemma: str, form: str) -> str:
    """Generate a controlled English verb surface form from a lemma."""
    record = IRREGULAR_FORMS.get(lemma.lower()) or regular_forms(lemma.lower())
    return {"base": record.lemma, "past": record.past, "participle": record.participle, "third_sg": record.third_singular, "progressive": record.progressive}.get(form, record.lemma)

