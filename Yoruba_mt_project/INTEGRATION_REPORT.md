# Supervisor revisions to the Yorùbá translation project

The project is a rule-based bilingual translator centred on the education domain. Its primary examples cover classroom instructions, school subjects and routine communication. The extended dictionary supports additional vocabulary. The revised productive rules described here run in the English to Yorùbá direction.

## Structure of the transfer

| Stage | Operation |
| --- | --- |
| Lexical lookup | Index sentence pairs and word senses. Use the POS of each lexical entry to identify candidate noun and verb phrases. |
| Source analysis | Identify subject, predicate, auxiliary, polarity, object and time expression in supported declaratives. Analyse English inflections such as `eats`, `ate`, `eaten` and `eating` as forms of `eat`. |
| Syntactic transfer | Retain subject, verb and object order. Move cardinal numbers and supported quantifiers after the noun, with `gbogbo` before the noun. Transfer spatial relations as whole units. |
| Target realisation | Select the Yorùbá verb stem and preverbal markers. Apply subject alternation in contexts such as `mo → mi` before `ò`. Preserve written tone and underdots through Unicode NFC normalisation. |

## Tense, aspect and polarity

The project treats English present, past and future as three source categories. In the controlled Yorùbá transfer, plain present and past can both map to the unmarked nonfuture construction. The lexical meaning and time expressions guide interpretation. A stative predicate such as `mọ̀` “know” normally supports a present reading in isolation. A dynamic event can receive a past reading, as in `Ó jẹ ìrẹsì lánàá`. English third person singular `-s` and the simple past form do not independently trigger a Yorùbá aspect marker.

| Construction | Affirmative | Negative | Example pair |
| --- | --- | --- | --- |
| Neutral nonfuture | Bare verb | `kò`, with contracted forms after eligible pronouns | She ate rice yesterday → Ó jẹ ìrẹsì lánàá. She did not eat rice yesterday → Kò jẹ ìrẹsì lánàá. |
| Perfect or completive | `ti` | `kò tíì` or `ò tíì` for the “not yet” reading | She has read two books → Ó ti ka ìwé méjì. She has not read two books yet → Kò tíì ka ìwé méjì. |
| Progressive | `ń` | `kì í` in the continuous negation analysis adopted here | She is reading two books → Ó ń ka ìwé méjì. She is not reading two books → Kì í ka ìwé méjì. |
| Habitual | `máa ń` | `kì í` | We usually eat rice → A máa ń jẹ ìrẹsì. We do not usually eat rice → A kì í jẹ ìrẹsì. |
| Future | `yóò` | `kì yóò` | She will eat rice → Ó yóò jẹ ìrẹsì. She will not eat rice → Kì yóò jẹ ìrẹsì. |
| Negative command | Imperative verb | `má` in simple commands, with `má ṣe` represented in the grammar inventory | Do not go → Má lọ. |

The progressive and habitual rules have separate rule identifiers. They can share a negative surface form, so the output may be interpreted habitually without context. The negative perfect implementation selects the “not yet” reading and does not cover every English negative perfect use. The future rule uses one affirmative form, `yóò`. Forms such as `á` and `máa` need their own context and are not generated as interchangeable variants by the controlled clause rules.

## Phrase structure, POS and tone

| Supervisor observation | Implementation |
| --- | --- |
| Show the lexicon and tag the dictionary | The extended CSV has a POS column for all 4,792 rows. The 367-entry curated CSV also provides semantic domain, register and written tone pattern. The table sense of `tábìlì` is tagged as a noun. Imported tags and glosses still require item-by-item linguistic review. |
| Relational expressions based on body parts | Spatial `on` maps to `lórí` with `orí` “head”, `in front of` to `níwájú` with `iwájú` “front”, and `behind` to `lẹ́yìn` with `ẹ̀yìn` “back”. The spatial mapping also includes `nínú` for “inside” and `lábẹ́` for “under”. |
| Articles and quantifiers | Controlled noun phrases allow zero realisation of English `a/an/the` where bare nouns are sufficient. `Two books` maps to `ìwé méjì` and `all the books` requires separate multi-determiner handling. |
| Tone and assimilation | Curated entries retain written tones and underdots. Surface alternations are limited to explicit forms such as `tí ó → tó` and `kì + ń → kì í`. The system does not infer a tone pattern from every unmarked imported word. |
| Lexical verbs and valency | The engine selects `jẹ` with a food object and `jẹun` without one. With `bring`, the serial construction `mú … wá` places the object between the verbs. Lexical possession `ní` is distinguished from perfect auxiliary `ti`. |

## Scope of evaluation

The grammar is a controlled prototype. It covers the simple constructions illustrated here. The reverse direction retains the existing bilingual lookup and fallback rules. Complex auxiliary chains, broad ambiguity resolution and exhaustive proofreading of inherited dictionary entries are outside this revision. Exact matches come from the project dataset, so a score calculated on that dataset measures retrieval and cannot establish accuracy on unseen sentences.

Reference for Standard Yorùbá continuous and future negation: [Negative Markers in Ào and Standard Yorùbá, Journal of West African Languages](https://journalofwestafricanlanguages.org/downloads?catid=92&id=449&m=0&task=download.send).
