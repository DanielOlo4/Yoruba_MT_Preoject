"""POS annotation for the canonical Yoruba-English education dataset.

The primary dataset remains the single source of truth.  This module imports
``education_dataset`` from the project's primary data module, or reads it from
an explicitly supplied source file.  It never keeps a copied list of examples.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

DEFAULT_DATASET_MODULES = (
    "yoruba_english_education_dataset",
    "education_dataset",
    "yoruba_dataset",
)


def _extract_assignment(source: str, name: str) -> Any:
    """Safely extract a literal dict/list assignment from a Python source file."""
    match = re.search(rf"(?m)^\s*{re.escape(name)}\s*=\s*", source)
    if not match:
        raise ValueError(f"Could not find {name!r} in the source file.")
    start = match.end()
    while start < len(source) and source[start].isspace():
        start += 1
    if start >= len(source) or source[start] not in "[{":
        raise ValueError(f"{name!r} is not a literal list or dictionary.")

    opener = source[start]
    closer = "]" if opener == "[" else "}"
    depth, quote, escaped = 0, None, False
    for position in range(start, len(source)):
        character = source[position]
        if quote:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
            continue
        if character in "'\"":
            quote = character
        elif character == opener:
            depth += 1
        elif character == closer:
            depth -= 1
            if depth == 0:
                return ast.literal_eval(source[start : position + 1])
    raise ValueError(f"{name!r} has no closing delimiter.")


def load_primary_dataset(source_path: str | Path | None = None) -> dict[str, list[dict[str, str]]]:
    """Load the primary dataset without maintaining a second dataset copy."""
    if source_path:
        return _extract_assignment(Path(source_path).read_text(encoding="utf-8"), "education_dataset")

    for module_name in DEFAULT_DATASET_MODULES:
        try:
            dataset = importlib.import_module(module_name).education_dataset
            return dataset
        except (ImportError, AttributeError):
            continue
    raise ImportError(
        "Primary dataset not found. Pass --dataset-source /path/to/your/data-file.py "
        "or name the data module yoruba_english_education_dataset.py."
    )


def load_lexicons(source_path: str | Path | None = None) -> tuple[dict[str, str], dict[str, str]]:
    """Load the project's POS lexicons when they are in the supplied source file."""
    if source_path:
        source = Path(source_path).read_text(encoding="utf-8")
        return (
            _extract_assignment(source, "ENGLISH_LEXICON"),
            _extract_assignment(source, "YORUBA_LEXICON"),
        )
    for module_name in DEFAULT_DATASET_MODULES:
        try:
            module = importlib.import_module(module_name)
            return module.ENGLISH_LEXICON, module.YORUBA_LEXICON
        except (ImportError, AttributeError):
            continue
    return {}, {}


def tokenize(text: str) -> list[str]:
    """Split text while preserving Yorùbá diacritics, hyphens, and punctuation."""
    return re.findall(r"[\wÀ-ÖØ-öø-ÿ'ọ́ẹ̀ẹ̀̀\-]+|[^\w\s]", text, flags=re.UNICODE)


class POSTagger:
    def __init__(self, english_lexicon: dict[str, str], yoruba_lexicon: dict[str, str]):
        self.english = {word.casefold(): tag for word, tag in english_lexicon.items()}
        self.yoruba = {word.casefold(): tag for word, tag in yoruba_lexicon.items()}

    @staticmethod
    def _fallback_english(token: str) -> str:
        token = token.casefold()
        if token.endswith("ly"):
            return "ADV"
        if token.endswith(("ing", "ed")):
            return "VERB"
        if token.endswith(("tion", "ment", "ness", "ity")):
            return "NOUN"
        return "NOUN"

    @staticmethod
    def _fallback_yoruba(token: str) -> str:
        token = token.casefold()
        if token.startswith(("ì", "à", "olù", "alá")):
            return "NOUN"
        return "NOUN"

    def tag(self, text: str, language: str) -> list[list[str]]:
        lexicon = self.english if language == "english" else self.yoruba
        fallback = self._fallback_english if language == "english" else self._fallback_yoruba
        tags: list[list[str]] = []
        for index, token in enumerate(tokenize(text)):
            if re.fullmatch(r"[^\w\s]+", token, flags=re.UNICODE):
                tag = "PUNCT"
            elif re.fullmatch(r"\d+(?:[.,]\d+)*", token):
                tag = "NUM"
            elif token.casefold() in lexicon:
                tag = lexicon[token.casefold()]
            elif index > 0 and token[:1].isupper():
                tag = "PROPN"
            else:
                tag = fallback(token)
            tags.append([token, tag])
        return tags


def validate_dataset(dataset: dict[str, list[dict[str, str]]]) -> list[str]:
    errors: list[str] = []
    for section, examples in dataset.items():
        if not isinstance(examples, list):
            errors.append(f"{section}: expected a list of examples")
            continue
        for number, example in enumerate(examples, start=1):
            if not isinstance(example, dict) or not all(isinstance(example.get(key), str) and example[key].strip() for key in ("english", "yoruba")):
                errors.append(f"{section}, example {number}: needs non-empty english and yoruba strings")
    return errors


def tag_primary_dataset(dataset: dict[str, list[dict[str, str]]], tagger: POSTagger) -> dict[str, list[dict[str, Any]]]:
    """Create POS fields from every current record in the primary dataset."""
    errors = validate_dataset(dataset)
    if errors:
        raise ValueError("Dataset validation failed:\n" + "\n".join(errors))
    return {
        section: [
            {
                **example,
                "english_pos": tagger.tag(example["english"], "english"),
                "yoruba_pos": tagger.tag(example["yoruba"], "yoruba"),
            }
            for example in examples
        ]
        for section, examples in dataset.items()
    }


def export_jsonl(tagged_dataset: dict[str, list[dict[str, Any]]], output_path: str | Path) -> None:
    with Path(output_path).open("w", encoding="utf-8") as file:
        for section, examples in tagged_dataset.items():
            for example in examples:
                file.write(json.dumps({"section": section, **example}, ensure_ascii=False) + "\n")


def summary(tagged_dataset: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    english, yoruba = Counter(), Counter()
    for examples in tagged_dataset.values():
        for example in examples:
            english.update(tag for _, tag in example["english_pos"])
            yoruba.update(tag for _, tag in example["yoruba_pos"])
    return {
        "sections": len(tagged_dataset),
        "examples": sum(len(examples) for examples in tagged_dataset.values()),
        "english_pos": dict(english),
        "yoruba_pos": dict(yoruba),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="POS-tag the current primary Yoruba-English dataset.")
    parser.add_argument("--dataset-source", help="Python/text file containing education_dataset and the POS lexicons.")
    parser.add_argument("--output", default="yoruba_english_pos_tagged.jsonl", help="JSONL output path.")
    args = parser.parse_args()

    dataset = load_primary_dataset(args.dataset_source)
    english_lexicon, yoruba_lexicon = load_lexicons(args.dataset_source)
    tagged = tag_primary_dataset(dataset, POSTagger(english_lexicon, yoruba_lexicon))
    export_jsonl(tagged, args.output)
    print(json.dumps(summary(tagged), ensure_ascii=False, indent=2))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
