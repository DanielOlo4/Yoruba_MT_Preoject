"""Build the reviewable English-Yorùbá verb-form inventory from the dictionary.

Run this script after changing the bilingual dictionary or the controlled verb
lexicon.  The generated CSV is a data resource, not a second translation path.
"""
from __future__ import annotations

import csv
from pathlib import Path

from english_morphology_rules import analyse_word, inflect
from yoruba_verb_grammar import VERB_LEXICON

ROOT = Path(__file__).parent
INPUT = ROOT / "yoruba_english_rule_based_lexicon.csv"
OUTPUT = ROOT / "yoruba_english_verb_forms.csv"

FIELDS = (
    "english_surface", "english_lemma", "english_morphology",
    "yoruba_surface", "yoruba_lemma", "yoruba_construction",
    "pos", "valency", "object_condition", "source",
)


def main() -> None:
    seen: set[tuple[str, ...]] = set()
    rows: list[dict[str, str]] = []
    with INPUT.open(encoding="utf-8-sig", newline="") as stream:
        records = list(csv.DictReader(stream))
    # The curated verb lexicon contains validated valency alternations such as
    # eat/jẹ versus eat/jẹun and serial verbs such as bring/mú … wá.  Include
    # it even when an imported dictionary has no matching verb row.
    dictionary_lemmas = {
        " ".join([analyse_word(row["english"].strip().lower().split()[0]).lemma, *row["english"].strip().lower().split()[1:]])
        for row in records if row.get("pos") == "VERB" and row.get("english", "").strip()
    }
    for lemma, verb in VERB_LEXICON.items():
        if lemma not in dictionary_lemmas:
            records.append({"english": lemma, "yoruba": verb.yoruba_lemma, "pos": "VERB", "alternatives": ""})
    for record in records:
            if record.get("pos") != "VERB":
                continue
            source_english = record["english"].strip().lower()
            yoruba = record["yoruba"].strip()
            if not source_english:
                continue
            parts = source_english.split()
            if parts[0] in {"a", "an", "the", "to"}:
                # Some imported dictionary entries carry a VERB tag although
                # their English gloss begins with a determiner or infinitival
                # marker.  Retain the entry for review, but do not manufacture
                # impossible forms such as "aed copy".
                row = {
                    "english_surface": source_english, "english_lemma": source_english,
                    "english_morphology": "dictionary_entry_uninflected",
                    "yoruba_surface": yoruba, "yoruba_lemma": yoruba,
                    "yoruba_construction": "dictionary_gloss", "pos": "VERB",
                    "valency": "unspecified", "object_condition": "review_needed",
                    "source": "dictionary",
                }
                signature = tuple(row[field] for field in FIELDS)
                if signature not in seen:
                    seen.add(signature); rows.append(row)
                continue
            head = analyse_word(parts[0]).lemma
            tail = " ".join(parts[1:])
            lemma = f"{head} {tail}".strip()
            controlled = VERB_LEXICON.get(lemma)
            transitive = controlled.yoruba_lemma if controlled else yoruba
            objectless = controlled.objectless_form if controlled else ""
            valency = controlled.valency.value if controlled else "unspecified"
            def english_surface(form: str) -> str:
                return f"{inflect(head, form)} {tail}".strip()
            forms = (
                (lemma, "base", transitive, "bare_verb", "with_object"),
                (english_surface("third_sg"), "third_person_present", transitive, "bare_verb", "with_object"),
                (english_surface("progressive"), "progressive", f"ń {transitive}", "progressive", "with_object"),
                (english_surface("past"), "past_or_completed", transitive, "nonfuture", "with_object"),
                (english_surface("participle"), "past_participle_or_perfect", f"ti {transitive}", "perfect", "with_object"),
                (f"will {lemma}", "future", f"yóò {transitive}", "future", "with_object"),
            )
            for surface, morphology, yo_surface, construction, condition in forms:
                row = {
                    "english_surface": surface, "english_lemma": lemma,
                    "english_morphology": morphology, "yoruba_surface": yo_surface,
                    "yoruba_lemma": transitive, "yoruba_construction": construction,
                    "pos": "VERB", "valency": valency,
                    "object_condition": condition, "source": "dictionary",
                }
                signature = tuple(row[field] for field in FIELDS)
                if signature not in seen:
                    seen.add(signature); rows.append(row)
            if objectless:
                for surface, morphology, prefix, construction in (
                    (lemma, "base", "", "bare_verb"),
                    (english_surface("third_sg"), "third_person_present", "", "bare_verb"),
                    (english_surface("progressive"), "progressive", "ń ", "progressive"),
                    (english_surface("past"), "past_or_completed", "", "nonfuture"),
                    (english_surface("participle"), "past_participle_or_perfect", "ti ", "perfect"),
                    (f"will {lemma}", "future", "yóò ", "future"),
                ):
                    row = {
                        "english_surface": surface, "english_lemma": lemma,
                        "english_morphology": morphology, "yoruba_surface": prefix + objectless,
                        "yoruba_lemma": objectless, "yoruba_construction": construction,
                        "pos": "VERB", "valency": valency,
                        "object_condition": "without_object", "source": "controlled_verb_lexicon",
                    }
                    signature = tuple(row[field] for field in FIELDS)
                    if signature not in seen:
                        seen.add(signature); rows.append(row)
    rows.sort(key=lambda row: (row["english_lemma"], row["object_condition"], row["english_morphology"]))
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    print(f"Wrote {len(rows)} verb-form records to {OUTPUT.name}")


if __name__ == "__main__":
    main()
