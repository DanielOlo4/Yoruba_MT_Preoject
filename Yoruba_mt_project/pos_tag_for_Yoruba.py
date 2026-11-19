# # ================================================================
# # YORUBA-ENGLISH POS TAGGING MODULE
# # Compatible with rule-based Yoruba translation models
# # ================================================================

# import re
# import json
# from collections import defaultdict

# # ================================================================
# # POS TAG DEFINITIONS (Universal Dependencies compatible)
# # ================================================================

# POS_TAGS = {
#     "NOUN": "Common noun",
#     "PROPN": "Proper noun",
#     "PRON": "Pronoun",
#     "VERB": "Verb",
#     "AUX": "Auxiliary verb",
#     "ADJ": "Adjective",
#     "ADV": "Adverb",
#     "ADP": "Adposition/Preposition",
#     "DET": "Determiner",
#     "NUM": "Numeral",
#     "CCONJ": "Coordinating conjunction",
#     "SCONJ": "Subordinating conjunction",
#     "PART": "Particle",
#     "INTJ": "Interjection",
#     "PUNCT": "Punctuation",
#     "SYM": "Symbol",
#     "X": "Other/Unknown",
# }

# # ================================================================
# # YORUBA LEXICON (word -> POS tag)
# # ================================================================

# YORUBA_LEXICON = {
#     # ---------- PRONOUNS ----------
#     "mo": "PRON", "mi": "PRON", "èmi": "PRON", "mí": "PRON",
#     "o": "PRON", "ìwọ": "PRON", "rẹ": "PRON", "ẹ": "PRON", "yín": "PRON",
#     "ó": "PRON", "òun": "PRON", "rẹ̀": "PRON", "ẹ̀": "PRON",
#     "a": "PRON", "àwa": "PRON", "wa": "PRON",
#     "wọ́n": "PRON", "àwọn": "PRON", "wọn": "PRON",
#     "ara": "PRON", "fúnra": "PRON",

#     # ---------- AUXILIARIES / TENSE MARKERS ----------
#     "ń": "AUX", "yóò": "AUX", "máa": "AUX", "ti": "AUX",
#     "ó": "AUX", "yió": "AUX", "a": "AUX", "ìbá": "AUX",
#     "lè": "AUX", "gbọ́dọ̀": "AUX", "yẹ": "AUX", "fẹ́": "AUX",
#     "ń": "AUX",

#     # ---------- COPULA / LINKING ----------
#     "jẹ́": "AUX", "ni": "AUX", "wà": "VERB",

#     # ---------- VERBS ----------
#     "kí": "VERB", "wá": "VERB", "lọ": "VERB", "bá": "VERB",
#     "dìde": "VERB", "jókòó": "VERB", "wọlé": "VERB", "jáde": "VERB",
#     "dákẹ́": "VERB", "pa": "VERB", "mọ́": "VERB", "gbọ́": "VERB",
#     "fi": "VERB", "wò": "VERB", "wo": "VERB", "ya": "VERB",
#     "padà": "VERB", "gbé": "VERB", "sọ": "VERB", "ṣí": "VERB",
#     "yí": "VERB", "ka": "VERB", "kọ": "VERB", "ṣe": "VERB",
#     "mú": "VERB", "fà": "VERB", "fún": "VERB", "gbà": "VERB",
#     "dúró": "VERB", "rin": "VERB", "nù": "VERB", "rẹ́": "VERB",
#     "parí": "VERB", "dẹ́kun": "VERB", "jẹ": "VERB", "jẹun": "VERB",
#     "mu": "VERB", "kọ́": "VERB", "fẹ́ràn": "VERB", "nífẹ̀ẹ́": "VERB",
#     "ṣèlérí": "VERB", "gbàgbé": "VERB", "rántí": "VERB", "sọnù": "VERB",
#     "nílò": "VERB", "lo": "VERB", "yẹ": "VERB", "wọn": "VERB",
#     "pín": "VERB", "ràn": "VERB", "lọ́wọ́": "VERB", "borí": "VERB",
#     "kùnà": "VERB", "kọjá": "VERB", "yọ": "VERB", "túmọ̀": "VERB",
#     "ṣàlàyé": "VERB", "ṣàkópọ̀": "VERB", "ṣàtúnṣe": "VERB", "fiwera": "VERB",
#     "yanjú": "VERB", "kà": "VERB", "pè": "VERB", "pe": "VERB",
#     "bi": "VERB", "béèrè": "VERB", "dáhùn": "VERB", "rò": "VERB",
#     "gbìyànjú": "VERB", "jáwọ́": "VERB", "ṣiṣẹ́": "VERB", "jìbìtì": "VERB",
#     "kàwé": "VERB", "ṣẹlẹ̀": "VERB", "tó": "VERB", "dára": "VERB",
#     "dùn": "VERB", "tẹ̀lé": "VERB", "tẹ̀síwájú": "VERB", "sun": "VERB",
#     "jí": "VERB", "dé": "VERB", "pẹ́": "VERB", "pèsè": "VERB",
#     "bọ̀wọ̀": "VERB", "fọwọ́sowọ́pọ̀": "VERB", "ṣàṣeyọrí": "VERB",
#     "ṣètò": "VERB", "jíròrò": "VERB", "yìn": "VERB", "bẹ̀rẹ̀": "VERB",
#     "kún": "VERB", "yí": "VERB", "ṣe": "VERB", "fà": "VERB",
#     "so": "VERB", "pọ̀": "VERB", "gbìn": "VERB", "mbomi": "VERB",
#     "tò": "VERB", "jíròrò": "VERB", "gbé": "VERB", "kalẹ̀": "VERB",
#     "pàdánù": "VERB", "yá": "VERB", "dá": "VERB", "padà": "VERB",
#     "sọ̀rọ̀": "VERB", "kọrin": "VERB", "jó": "VERB", "ṣeré": "VERB",
#     "bínú": "VERB", "lóye": "VERB", "yé": "VERB", "mọ": "VERB",
#     "mọ̀": "VERB", "rí": "VERB", "ṣí": "VERB", "ṣàmì": "VERB",
#     "gbọ́n": "ADJ", "tóbi": "ADJ", "kéré": "ADJ", "lẹ́wà": "ADJ",
#     "jẹ ẹ́": "VERB", "jáde": "VERB", "wúlò": "ADJ", "san": "VERB",
#     "rẹ̀": "VERB", "hùwà": "VERB", "múra": "VERB",

#     # ---------- NOUNS ----------
#     "olùkọ́": "NOUN", "akẹ́kọ̀ọ́": "NOUN", "ilé": "NOUN", "ẹ̀kọ́": "NOUN",
#     "kíláàsì": "NOUN", "ìwé": "NOUN", "kálámù": "NOUN", "pẹ́ńsúlù": "NOUN",
#     "rúlà": "NOUN", "rọ́bà": "NOUN", "tébùrù": "NOUN", "àga": "NOUN",
#     "pátákó": "NOUN", "kọ́ọ̀kì": "NOUN", "máàkà": "NOUN", "àkọsílẹ̀": "NOUN",
#     "atúmọ̀": "NOUN", "èdè": "NOUN", "àwòrán": "NOUN", "ilẹ̀": "NOUN",
#     "ayé": "NOUN", "kọ̀ǹpútà": "NOUN", "ẹ̀rọ": "NOUN", "ìṣírò": "NOUN",
#     "àpò": "NOUN", "ìgbọ̀nsẹ̀": "NOUN", "omi": "NOUN", "orí": "NOUN",
#     "ebi": "NOUN", "òùngbẹ": "NOUN", "ara": "NOUN", "àṣọ": "NOUN",
#     "ìbéèrè": "NOUN", "ìdáhùn": "NOUN", "ohun": "NOUN", "èlò": "NOUN",
#     "ìpèsè": "NOUN", "iṣẹ́": "NOUN", "ilé ìgbọ̀nsẹ̀": "NOUN",
#     "sáyẹ́ǹsì": "NOUN", "Gẹ̀ẹ́sì": "PROPN", "Yorùbá": "PROPN",
#     "Faransé": "PROPN", "Lárúbáwá": "PROPN", "ìtàn": "NOUN",
#     "jẹ́ọ́gírápì": "NOUN", "ìlú": "NOUN", "ọmọlúàbí": "NOUN",
#     "ọnà": "NOUN", "orin": "NOUN", "eré": "NOUN", "ìdárayá": "NOUN",
#     "àgbẹ̀": "NOUN", "alààyè": "NOUN", "kẹ́mísírì": "NOUN", "físíìkì": "NOUN",
#     "ètò": "NOUN", "ọrọ̀": "NOUN", "ajé": "NOUN", "lítíréṣọ̀": "NOUN",
#     "ìsìn": "NOUN", "ìṣàkóso": "NOUN", "ìyàwòrán": "NOUN", "tẹ̀kníkà": "NOUN",
#     "àtò": "NOUN", "àkókò": "NOUN", "àmì": "NOUN", "ipò": "NOUN",
#     "èsì": "NOUN", "ìdánwò": "NOUN", "ewì": "NOUN", "ọ̀rọ̀": "NOUN",
#     "gbólóhùn": "NOUN", "ìtumọ̀": "NOUN", "àròkọ": "NOUN", "ẹsè": "NOUN",
#     "ìtọ́sọ́nà": "NOUN", "ìlà": "NOUN", "àyè": "NOUN", "ìṣòro": "NOUN",
#     "nọ́ńbà": "NOUN", "gígùn": "NOUN", "oṣùpá": "NOUN", "àwọ̀": "NOUN",
#     "alábàáṣiṣẹ́": "NOUN", "ọ̀rẹ́": "NOUN", "ẹgbẹ́": "NOUN", "àdánwò": "NOUN",
#     "ìdánilẹ́kọ̀ọ́": "NOUN", "ọjọ́": "NOUN", "ìsinmi": "NOUN", "oṣù": "NOUN",
#     "ọdún": "NOUN", "ọ̀sẹ̀": "NOUN", "ìgbà": "NOUN", "aago": "NOUN",
#     "ìṣẹ́jú": "NOUN", "agogo": "NOUN", "ariwo": "NOUN", "pápá": "NOUN",
#     "àpéjọ": "NOUN", "olùdarí": "NOUN", "ọ́fíìsì": "NOUN", "yàrá": "NOUN",
#     "ẹnubodè": "NOUN", "odi": "NOUN", "ọgbà": "NOUN", "oúnjẹ": "NOUN",
#     "ìkàwé": "NOUN", "ìtànná": "NOUN", "iná": "NOUN", "mọ̀nàmọ́ná": "NOUN",
#     "fáánì": "NOUN", "àṣà": "NOUN", "ìwà": "NOUN", "rere": "ADJ",
#     "ààbò": "NOUN", "àyíká": "NOUN", "ìbọ̀wọ̀": "NOUN", "ìgbọ́kànlé": "NOUN",
#     "ìjíròrò": "NOUN", "èrò": "NOUN", "àkòrí": "NOUN", "ẹ̀bùn": "NOUN",
#     "iṣẹ́ àṣẹ": "NOUN", "iṣẹ́ ilé": "NOUN", "ọwọ́": "NOUN", "etí": "NOUN",
#     "orúkọ": "NOUN", "àsíá": "NOUN", "àtúnyẹ̀wò": "NOUN", "àtúnpadà": "NOUN",
#     "ọjọ́ ọjọ́": "NOUN", "ojú": "NOUN", "ewé": "NOUN", "àwòrán ilẹ̀": "NOUN",
#     "ọ̀la": "NOUN", "àná": "NOUN", "lẹ́tà": "NOUN", "àfọ̀nù": "NOUN",
#     "ìpadé": "NOUN", "ìlera": "NOUN", "ìyípadà": "NOUN", "kẹ́míkà": "NOUN",
#     "okun": "NOUN", "agbára": "NOUN", "ọgbọ́n": "NOUN", "àsán": "NOUN",
#     "ìrọ̀lẹ́": "NOUN", "àárọ̀": "NOUN", "ọ̀sán": "NOUN", "àbọ̀": "NOUN",
#     "àtúnpadà": "NOUN", "ìmọ̀": "NOUN", "ìlérí": "NOUN", "ẹgbẹ̀rún": "NUM",
#     "ìkẹyìn": "ADJ", "iṣẹ́ àgbékalẹ̀": "NOUN", "ìgbàlódé": "ADJ",
#     "àdúrà": "NOUN", "ìyìn": "NOUN", "ìtò": "NOUN", "ìbùjókòó": "NOUN",
#     "ohùn": "NOUN", "àdánrawò": "NOUN", "àṣìṣe": "NOUN", "àdàkọ": "NOUN",
#     "àbámẹ́ta": "NOUN", "Bọ́lájí": "PROPN", "Adesewa": "PROPN",
#     "ọkùrin": "NOUN", "ọmọdé": "NOUN", "obìnrin": "NOUN", "ọmọ": "NOUN",
#     "òbí": "NOUN", "ìfẹ̀ẹ́": "NOUN",

#     # ---------- ADJECTIVES ----------
#     "dáadáa": "ADJ", "tuntun": "ADJ", "funfun": "ADJ", "dúdú": "ADJ",
#     "pupa": "ADJ", "búlúù": "ADJ", "ewé": "ADJ", "mọ́": "ADJ",
#     "dọ̀tí": "ADJ", "le": "ADJ", "rọrùn": "ADJ", "ṣòro": "ADJ",
#     "dára": "ADJ", "tó dára": "ADJ", "pàtàkì": "ADJ", "aládàáṣe": "ADJ",
#     "gíga": "ADJ", "gíga jù": "ADJ", "déédéé": "ADJ", "mìíràn": "ADJ",
#     "olóòtọ́": "ADJ", "ọlẹ́": "ADJ", "kedere": "ADJ", "kánkán": "ADV",
#     "ṣófo": "ADJ", "takuntakun": "ADV", "gidigidi": "ADV",
#     "pé": "ADJ", "tẹ́lẹ̀": "ADJ",

#     # ---------- ADVERBS ----------
#     "lónìí": "ADV", "lọ́la": "ADV", "lánàá": "ADV", "nísisìyí": "ADV",
#     "báyìí": "ADV", "nígbà": "ADV", "nígbàgbogbo": "ADV", "lẹ́ẹ̀kansi": "ADV",
#     "lójoojúmọ́": "ADV", "sókè": "ADV", "kalẹ̀": "ADV", "síwájú": "ADV",
#     "lẹ́yìn": "ADV", "níbí": "ADV", "níbẹ̀": "ADV", "jìnnà": "ADV",
#     "súnmọ́": "ADV", "ní ìdákẹ́rọ́rọ́": "ADV", "ní ohùn rara": "ADV",
#     "jù": "ADV", "síi": "ADV", "ní àkókò": "ADV", "kùtùkùtù": "ADV",
#     "ní àárọ̀": "ADV", "ní ọ̀sán": "ADV", "ní ìrọ̀lẹ́": "ADV",
#     "rara": "ADV", "lẹ́ẹ̀kan": "ADV", "fúnra": "ADV", "músẹ́": "ADV",
#     "sílẹ̀": "ADV",

#     # ---------- ADPOSITIONS/PREPOSITIONS ----------
#     "ní": "ADP", "sí": "ADP", "lórí": "ADP", "nínú": "ADP",
#     "sínú": "ADP", "lábẹ́": "ADP", "lẹ́gbẹ̀ẹ́": "ADP", "fún": "ADP",
#     "pẹ̀lú": "ADP", "láti": "ADP", "títí": "ADP", "nípa": "ADP",
#     "sẹ́yìn": "ADP", "àbẹ́": "ADP", "lọ́wọ́": "ADP", "ká": "ADP",
#     "sẹ́gbẹ̀ẹ́": "ADP",

#     # ---------- DETERMINERS ----------
#     "náà": "DET", "yìí": "DET", "yí": "DET", "ìyẹn": "DET",
#     "èyí": "DET", "ohun": "DET", "gbogbo": "DET", "kọ̀ọ̀kan": "DET",
#     "kan": "DET", "díẹ̀": "DET", "púpọ̀": "DET", "ọ̀pọ̀lọpọ̀": "DET",
#     "mélòó": "DET",

#     # ---------- NUMBERS ----------
#     "ọ̀kan": "NUM", "èjì": "NUM", "ẹ̀ta": "NUM", "ẹ̀rin": "NUM",
#     "àrún": "NUM", "ẹ̀fà": "NUM", "èje": "NUM", "ẹ̀jọ": "NUM",
#     "ẹ̀sán": "NUM", "ẹ̀wàá": "NUM", "ọ̀kànlá": "NUM", "èjìlá": "NUM",
#     "ẹ̀tàlá": "NUM", "ẹ̀rìnlá": "NUM", "ẹ̀ẹ́dógún": "NUM", "ogún": "NUM",
#     "ọgbọ̀n": "NUM", "ogójì": "NUM", "àádọ́ta": "NUM", "ọgọ́rùn-ún": "NUM",
#     "ẹgbẹ̀rún": "NUM", "àkọ́kọ́": "NUM", "èkejì": "NUM", "ẹ̀kẹta": "NUM",
#     "méjì": "NUM", "mẹ́ta": "NUM", "mẹ́rin": "NUM", "márùn-ún": "NUM",
#     "mẹ́fà": "NUM", "méje": "NUM", "mẹ́jọ": "NUM", "mẹ́sàn-án": "NUM",
#     "mẹ́wàá": "NUM", "méjìlá": "NUM", "kìíní": "NUM",

#     # ---------- CONJUNCTIONS ----------
#     "àti": "CCONJ", "sì": "CCONJ", "tàbí": "CCONJ", "ṣùgbọ́n": "CCONJ",
#     "kí": "SCONJ", "nítorí": "SCONJ", "nítorí pé": "SCONJ", "bí": "SCONJ",
#     "bí...bá": "SCONJ", "tí": "SCONJ", "nígbà tí": "SCONJ", "bí ó tilẹ̀ jẹ́ pé": "SCONJ",
#     "pé": "SCONJ", "bí ó bá": "SCONJ", "nítorí náà": "SCONJ",

#     # ---------- PARTICLES ----------
#     "kò": "PART", "ò": "PART", "má": "PART", "bá": "PART",
#     "kì í": "PART", "ì": "PART", "tíì": "PART", "tilẹ̀": "PART",
#     "jọ̀wọ́": "PART", "ṣé": "PART", "náà": "PART",

#     # ---------- INTERJECTIONS ----------
#     "e": "INTJ", "ẹ": "INTJ", "ṣé": "INTJ", "ha": "INTJ",
#     "káàárọ̀": "INTJ", "kú": "INTJ", "báwo": "INTJ", "dàbọ̀": "INTJ",
# }

# # ================================================================
# # ENGLISH LEXICON (word -> POS tag)
# # ================================================================

# ENGLISH_LEXICON = {
#     # Pronouns
#     "i": "PRON", "you": "PRON", "he": "PRON", "she": "PRON",
#     "it": "PRON", "we": "PRON", "they": "PRON",
#     "me": "PRON", "him": "PRON", "her": "PRON", "us": "PRON", "them": "PRON",
#     "my": "PRON", "your": "PRON", "his": "PRON", "its": "PRON",
#     "our": "PRON", "their": "PRON", "mine": "PRON", "yours": "PRON",
#     "myself": "PRON", "yourself": "PRON", "himself": "PRON", "herself": "PRON",
#     "ourselves": "PRON", "themselves": "PRON", "this": "DET", "that": "DET",
#     "these": "DET", "those": "DET", "who": "PRON", "whom": "PRON",
#     "which": "PRON", "what": "PRON", "whose": "PRON",

#     # Auxiliaries
#     "am": "AUX", "is": "AUX", "are": "AUX", "was": "AUX", "were": "AUX",
#     "be": "AUX", "been": "AUX", "being": "AUX",
#     "have": "AUX", "has": "AUX", "had": "AUX", "having": "AUX",
#     "do": "AUX", "does": "AUX", "did": "AUX",
#     "will": "AUX", "would": "AUX", "shall": "AUX", "should": "AUX",
#     "can": "AUX", "could": "AUX", "may": "AUX", "might": "AUX",
#     "must": "AUX", "ought": "AUX",

#     # Common verbs
#     "go": "VERB", "goes": "VERB", "went": "VERB", "gone": "VERB", "going": "VERB",
#     "come": "VERB", "comes": "VERB", "came": "VERB", "coming": "VERB",
#     "see": "VERB", "sees": "VERB", "saw": "VERB", "seen": "VERB", "seeing": "VERB",
#     "read": "VERB", "reads": "VERB", "reading": "VERB",
#     "write": "VERB", "writes": "VERB", "wrote": "VERB", "written": "VERB", "writing": "VERB",
#     "study": "VERB", "studies": "VERB", "studied": "VERB", "studying": "VERB",
#     "learn": "VERB", "learns": "VERB", "learned": "VERB", "learning": "VERB",
#     "teach": "VERB", "teaches": "VERB", "taught": "VERB", "teaching": "VERB",
#     "ask": "VERB", "asks": "VERB", "asked": "VERB", "asking": "VERB",
#     "answer": "VERB", "answers": "VERB", "answered": "VERB", "answering": "VERB",
#     "stand": "VERB", "stands": "VERB", "stood": "VERB", "standing": "VERB",
#     "sit": "VERB", "sits": "VERB", "sat": "VERB", "sitting": "VERB",
#     "open": "VERB", "opens": "VERB", "opened": "VERB", "opening": "VERB",
#     "close": "VERB", "closes": "VERB", "closed": "VERB", "closing": "VERB",
#     "give": "VERB", "gives": "VERB", "gave": "VERB", "given": "VERB", "giving": "VERB",
#     "take": "VERB", "takes": "VERB", "took": "VERB", "taken": "VERB", "taking": "VERB",
#     "bring": "VERB", "brings": "VERB", "brought": "VERB", "bringing": "VERB",
#     "put": "VERB", "puts": "VERB", "putting": "VERB",
#     "get": "VERB", "gets": "VERB", "got": "VERB", "getting": "VERB",
#     "make": "VERB", "makes": "VERB", "made": "VERB", "making": "VERB",
#     "know": "VERB", "knows": "VERB", "knew": "VERB", "known": "VERB",
#     "think": "VERB", "thinks": "VERB", "thought": "VERB", "thinking": "VERB",
#     "want": "VERB", "wants": "VERB", "wanted": "VERB",
#     "need": "VERB", "needs": "VERB", "needed": "VERB",
#     "like": "VERB", "likes": "VERB", "liked": "VERB",
#     "love": "VERB", "loves": "VERB", "loved": "VERB",
#     "listen": "VERB", "listens": "VERB", "listened": "VERB", "listening": "VERB",
#     "look": "VERB", "looks": "VERB", "looked": "VERB", "looking": "VERB",
#     "speak": "VERB", "speaks": "VERB", "spoke": "VERB", "spoken": "VERB", "speaking": "VERB",
#     "say": "VERB", "says": "VERB", "said": "VERB", "saying": "VERB",
#     "tell": "VERB", "tells": "VERB", "told": "VERB", "telling": "VERB",
#     "pay": "VERB", "pays": "VERB", "paid": "VERB", "paying": "VERB",
#     "raise": "VERB", "raises": "VERB", "raised": "VERB", "raising": "VERB",
#     "turn": "VERB", "turns": "VERB", "turned": "VERB", "turning": "VERB",
#     "copy": "VERB", "copies": "VERB", "copied": "VERB", "copying": "VERB",
#     "submit": "VERB", "submits": "VERB", "submitted": "VERB", "submitting": "VERB",
#     "collect": "VERB", "collects": "VERB", "collected": "VERB", "collecting": "VERB",
#     "clean": "VERB", "cleans": "VERB", "cleaned": "VERB", "cleaning": "VERB",
#     "erase": "VERB", "erases": "VERB", "erased": "VERB", "erasing": "VERB",
#     "pick": "VERB", "picks": "VERB", "picked": "VERB", "picking": "VERB",
#     "finish": "VERB", "finishes": "VERB", "finished": "VERB", "finishing": "VERB",
#     "stop": "VERB", "stops": "VERB", "stopped": "VERB", "stopping": "VERB",
#     "behave": "VERB", "behaves": "VERB", "behaved": "VERB",
#     "clap": "VERB", "claps": "VERB", "clapped": "VERB",
#     "sing": "VERB", "sings": "VERB", "sang": "VERB", "sung": "VERB", "singing": "VERB",
#     "pass": "VERB", "passes": "VERB", "passed": "VERB", "passing": "VERB",
#     "repeat": "VERB", "repeats": "VERB", "repeated": "VERB", "repeating": "VERB",
#     "explain": "VERB", "explains": "VERB", "explained": "VERB", "explaining": "VERB",
#     "draw": "VERB", "draws": "VERB", "drew": "VERB", "drawn": "VERB", "drawing": "VERB",
#     "color": "VERB", "colored": "VERB",
#     "try": "VERB", "tries": "VERB", "tried": "VERB", "trying": "VERB",
#     "work": "VERB", "works": "VERB", "worked": "VERB", "working": "VERB",
#     "share": "VERB", "shares": "VERB", "shared": "VERB", "sharing": "VERB",
#     "help": "VERB", "helps": "VERB", "helped": "VERB", "helping": "VERB",
#     "cheat": "VERB", "cheats": "VERB", "cheated": "VERB", "cheating": "VERB",
#     "practice": "VERB", "practices": "VERB", "practiced": "VERB", "practicing": "VERB",
#     "correct": "VERB", "corrects": "VERB", "corrected": "VERB",
#     "check": "VERB", "checks": "VERB", "checked": "VERB", "checking": "VERB",
#     "compare": "VERB", "compares": "VERB", "compared": "VERB", "comparing": "VERB",
#     "memorize": "VERB", "memorized": "VERB",
#     "recite": "VERB", "recited": "VERB",
#     "spell": "VERB", "spells": "VERB", "spelled": "VERB",
#     "define": "VERB", "defines": "VERB", "defined": "VERB",
#     "use": "VERB", "uses": "VERB", "used": "VERB", "using": "VERB",
#     "translate": "VERB", "translates": "VERB", "translated": "VERB",
#     "summarize": "VERB", "summarized": "VERB",
#     "follow": "VERB", "follows": "VERB", "followed": "VERB", "following": "VERB",
#     "underline": "VERB", "underlined": "VERB",
#     "circle": "VERB", "circled": "VERB",
#     "fill": "VERB", "fills": "VERB", "filled": "VERB",
#     "match": "VERB", "matches": "VERB", "matched": "VERB",
#     "complete": "VERB", "completes": "VERB", "completed": "VERB",
#     "solve": "VERB", "solves": "VERB", "solved": "VERB", "solving": "VERB",
#     "calculate": "VERB", "calculates": "VERB", "calculated": "VERB",
#     "count": "VERB", "counts": "VERB", "counted": "VERB", "counting": "VERB",
#     "measure": "VERB", "measures": "VERB", "measured": "VERB",
#     "add": "VERB", "adds": "VERB", "added": "VERB",
#     "subtract": "VERB", "subtracts": "VERB", "subtracted": "VERB",
#     "multiply": "VERB", "multiplies": "VERB", "multiplied": "VERB",
#     "divide": "VERB", "divides": "VERB", "divided": "VERB",
#     "show": "VERB", "shows": "VERB", "showed": "VERB", "shown": "VERB",
#     "understand": "VERB", "understands": "VERB", "understood": "VERB",
#     "forget": "VERB", "forgets": "VERB", "forgot": "VERB", "forgotten": "VERB",
#     "remember": "VERB", "remembers": "VERB", "remembered": "VERB",
#     "promise": "VERB", "promises": "VERB", "promised": "VERB",
#     "borrow": "VERB", "borrows": "VERB", "borrowed": "VERB",
#     "lose": "VERB", "loses": "VERB", "lost": "VERB", "losing": "VERB",
#     "arrive": "VERB", "arrives": "VERB", "arrived": "VERB",
#     "allow": "VERB", "allows": "VERB", "allowed": "VERB",
#     "scold": "VERB", "scolded": "VERB",
#     "mark": "VERB", "marks": "VERB", "marked": "VERB",
#     "record": "VERB", "records": "VERB", "recorded": "VERB",
#     "revise": "VERB", "revises": "VERB", "revised": "VERB",
#     "cooperate": "VERB", "cooperates": "VERB", "cooperated": "VERB",
#     "respect": "VERB", "respects": "VERB", "respected": "VERB",
#     "reward": "VERB", "rewards": "VERB", "rewarded": "VERB",
#     "promote": "VERB", "promotes": "VERB", "promoted": "VERB",
#     "provide": "VERB", "provides": "VERB", "provided": "VERB",
#     "organise": "VERB", "organised": "VERB", "organize": "VERB", "organized": "VERB",
#     "encourage": "VERB", "encourages": "VERB", "encouraged": "VERB",
#     "praise": "VERB", "praises": "VERB", "praised": "VERB",
#     "assess": "VERB", "assesses": "VERB", "assessed": "VERB",
#     "present": "VERB", "presents": "VERB", "presented": "VERB",
#     "receive": "VERB", "receives": "VERB", "received": "VERB",
#     "score": "VERB", "scores": "VERB", "scored": "VERB",
#     "wake": "VERB", "wakes": "VERB", "woke": "VERB", "waking": "VERB",
#     "play": "VERB", "plays": "VERB", "played": "VERB", "playing": "VERB",
#     "dance": "VERB", "danced": "VERB",
#     "sell": "VERB", "sells": "VERB", "sold": "VERB", "selling": "VERB",
#     "eat": "VERB", "eats": "VERB", "ate": "VERB", "eating": "VERB",
#     "drink": "VERB", "drinks": "VERB", "drank": "VERB", "drinking": "VERB",
#     "ring": "VERB", "rings": "VERB", "rang": "VERB", "ringing": "VERB",
#     "start": "VERB", "starts": "VERB", "started": "VERB", "starting": "VERB",
#     "begin": "VERB", "begins": "VERB", "began": "VERB", "beginning": "VERB",
#     "end": "VERB", "ends": "VERB", "ended": "VERB", "ending": "VERB",
#     "arrange": "VERB", "arranges": "VERB", "arranged": "VERB",
#     "keep": "VERB", "keeps": "VERB", "kept": "VERB", "keeping": "VERB",
#     "plant": "VERB", "plants": "VERB", "planted": "VERB",
#     "water": "VERB", "watered": "VERB",
#     "smile": "VERB", "smiles": "VERB", "smiled": "VERB",
#     "discuss": "VERB", "discusses": "VERB", "discussed": "VERB",
#     "return": "VERB", "returns": "VERB", "returned": "VERB", "returning": "VERB",
#     "fail": "VERB", "fails": "VERB", "failed": "VERB",
#     "miss": "VERB", "missed": "VERB",
#     "punish": "VERB", "punished": "VERB",
#     "line": "VERB", "lined": "VERB",
#     "march": "VERB", "marched": "VERB",
#     "form": "VERB", "formed": "VERB",
#     "greet": "VERB", "greets": "VERB", "greeted": "VERB",
#     "enter": "VERB", "enters": "VERB", "entered": "VERB", "entering": "VERB",
#     "continue": "VERB", "continues": "VERB", "continued": "VERB",
#     "reopen": "VERB", "reopens": "VERB", "reopened": "VERB",
#     "equal": "VERB", "equals": "VERB",

#     # Nouns
#     "teacher": "NOUN", "student": "NOUN", "students": "NOUN", "school": "NOUN",
#     "class": "NOUN", "classroom": "NOUN", "book": "NOUN", "books": "NOUN",
#     "pen": "NOUN", "pencil": "NOUN", "ruler": "NOUN", "eraser": "NOUN",
#     "sharpener": "NOUN", "desk": "NOUN", "chair": "NOUN", "board": "NOUN",
#     "blackboard": "NOUN", "whiteboard": "NOUN", "chalk": "NOUN", "marker": "NOUN",
#     "notebook": "NOUN", "textbook": "NOUN", "dictionary": "NOUN", "map": "NOUN",
#     "globe": "NOUN", "computer": "NOUN", "calculator": "NOUN", "bag": "NOUN",
#     "table": "NOUN", "duster": "NOUN", "homework": "NOUN", "assignment": "NOUN",
#     "work": "NOUN", "paper": "NOUN", "papers": "NOUN", "name": "NOUN",
#     "notes": "NOUN", "lesson": "NOUN", "page": "NOUN", "passage": "NOUN",
#     "question": "NOUN", "questions": "NOUN", "answer": "NOUN", "answers": "NOUN",
#     "prayer": "NOUN", "anthem": "NOUN", "hand": "NOUN", "hands": "NOUN",
#     "seat": "NOUN", "line": "NOUN", "day": "NOUN", "days": "NOUN",
#     "morning": "NOUN", "afternoon": "NOUN", "evening": "NOUN", "night": "NOUN",
#     "holiday": "NOUN", "term": "NOUN", "subject": "NOUN", "subjects": "NOUN",
#     "mathematics": "NOUN", "english": "PROPN", "yoruba": "PROPN",
#     "science": "NOUN", "history": "NOUN", "geography": "NOUN",
#     "art": "NOUN", "music": "NOUN", "education": "NOUN", "agriculture": "NOUN",
#     "biology": "NOUN", "chemistry": "NOUN", "physics": "NOUN", "economics": "NOUN",
#     "literature": "NOUN", "french": "PROPN", "arabic": "PROPN",
#     "timetable": "NOUN", "examination": "NOUN", "marks": "NOUN", "results": "NOUN",
#     "uniform": "NOUN", "materials": "NOUN", "desks": "NOUN",
#     "library": "NOUN", "laboratory": "NOUN", "playground": "NOUN", "children": "NOUN",
#     "assembly": "NOUN", "ground": "NOUN", "principal": "NOUN", "office": "NOUN",
#     "staffroom": "NOUN", "gate": "NOUN", "fence": "NOUN", "garden": "NOUN",
#     "canteen": "NOUN", "food": "NOUN", "break": "NOUN", "bell": "NOUN",
#     "flag": "NOUN", "toilet": "NOUN", "electricity": "NOUN", "water": "NOUN",
#     "fan": "NOUN", "flowers": "NOUN", "house": "NOUN", "home": "NOUN",
#     "number": "NOUN", "numbers": "NOUN", "length": "NOUN", "problem": "NOUN",
#     "exercise": "NOUN", "composition": "NOUN", "essay": "NOUN", "poem": "NOUN",
#     "word": "NOUN", "words": "NOUN", "sentence": "NOUN", "instructions": "NOUN",
#     "blanks": "NOUN", "pair": "NOUN", "pairs": "NOUN", "groups": "NOUN",
#     "mistake": "NOUN", "mistakes": "NOUN", "friend": "NOUN", "partner": "NOUN",
#     "headache": "NOUN", "today": "NOUN", "tomorrow": "NOUN", "yesterday": "NOUN",
#     "week": "NOUN", "month": "NOUN", "months": "NOUN", "year": "NOUN",
#     "time": "NOUN", "minutes": "NOUN", "hour": "NOUN", "hours": "NOUN",
#     "monday": "PROPN", "tuesday": "PROPN", "wednesday": "PROPN", "thursday": "PROPN",
#     "friday": "PROPN", "saturday": "PROPN", "sunday": "PROPN",
#     "january": "PROPN", "february": "PROPN", "march": "PROPN", "april": "PROPN",
#     "may": "PROPN", "june": "PROPN", "july": "PROPN", "august": "PROPN",
#     "september": "PROPN", "october": "PROPN", "november": "PROPN", "december": "PROPN",
#     "idea": "NOUN", "ideas": "NOUN", "topic": "NOUN", "feedback": "NOUN",
#     "project": "NOUN", "debate": "NOUN", "environment": "NOUN", "teaching": "NOUN",
#     "learning": "NOUN", "technology": "NOUN", "test": "NOUN", "weather": "NOUN",
#     "prize": "NOUN", "cultural": "ADJ", "scripts": "NOUN", "scores": "NOUN",
#     "syllabus": "NOUN", "revision": "NOUN", "trees": "NOUN", "reactions": "NOUN",
#     "chemical": "ADJ", "forces": "NOUN", "energy": "NOUN", "farming": "NOUN",
#     "stories": "NOUN", "skill": "NOUN", "resumption": "NOUN", "voice": "NOUN",
#     "boy": "NOUN", "girl": "NOUN", "parents": "NOUN", "adesewa": "PROPN",
#     "bolaji": "PROPN", "attention": "NOUN", "noise": "NOUN", "o'clock": "NOUN",

#     # Adjectives
#     "good": "ADJ", "bad": "ADJ", "big": "ADJ", "small": "ADJ",
#     "fine": "ADJ", "clean": "ADJ", "dirty": "ADJ", "new": "ADJ",
#     "old": "ADJ", "white": "ADJ", "black": "ADJ", "red": "ADJ",
#     "blue": "ADJ", "green": "ADJ", "beautiful": "ADJ", "nice": "ADJ",
#     "happy": "ADJ", "sad": "ADJ", "best": "ADJ", "better": "ADJ",
#     "difficult": "ADJ", "easy": "ADJ", "important": "ADJ", "interesting": "ADJ",
#     "creative": "ADJ", "enjoyable": "ADJ", "healthy": "ADJ", "modern": "ADJ",
#     "ready": "ADJ", "late": "ADJ", "early": "ADJ", "sick": "ADJ",
#     "hungry": "ADJ", "thirsty": "ADJ", "confused": "ADJ", "sorry": "ADJ",
#     "present": "ADJ", "absent": "ADJ", "many": "ADJ", "much": "ADJ",
#     "large": "ADJ", "near": "ADJ", "far": "ADJ", "high": "ADJ",
#     "clever": "ADJ", "lazy": "ADJ", "strict": "ADJ", "fair": "ADJ",
#     "honest": "ADJ", "noisy": "ADJ", "quiet": "ADJ", "safe": "ADJ",
#     "right": "ADJ", "correct": "ADJ", "wrong": "ADJ", "neatly": "ADV",
#     "loud": "ADJ", "clear": "ADJ", "silent": "ADJ", "aloud": "ADV",
#     "orderly": "ADJ", "disciplined": "ADJ", "useful": "ADJ",
#     "responsible": "ADJ", "last": "ADJ", "next": "ADJ",
#     "rewarding": "ADJ", "challenging": "ADJ", "main": "ADJ",
#     "every": "DET", "all": "DET", "another": "DET", "each": "DET",
#     "both": "DET", "some": "DET", "any": "DET", "no": "DET",
#     "equipped": "ADJ", "attentively": "ADV", "confidently": "ADV",
#     "comfortably": "ADV", "politely": "ADV", "smoothly": "ADV",
#     "regularly": "ADV", "quickly": "ADV", "carefully": "ADV",
#     "clearly": "ADV", "louder": "ADV", "harder": "ADV", "more": "ADV",
#     "well": "ADV",

#     # Adverbs
#     "now": "ADV", "then": "ADV", "here": "ADV", "there": "ADV",
#     "always": "ADV", "never": "ADV", "often": "ADV", "sometimes": "ADV",
#     "usually": "ADV", "very": "ADV", "quite": "ADV", "too": "ADV",
#     "also": "ADV", "only": "ADV", "just": "ADV", "even": "ADV",
#     "still": "ADV", "already": "ADV", "yet": "ADV", "soon": "ADV",
#     "again": "ADV", "together": "ADV", "today": "ADV", "tomorrow": "ADV",
#     "yesterday": "ADV", "hard": "ADV", "fast": "ADV", "slowly": "ADV",
#     "silently": "ADV", "home": "ADV", "outside": "ADV", "inside": "ADV",
#     "back": "ADV", "down": "ADV", "up": "ADV", "out": "ADV",
#     "in": "ADP", "on": "ADP", "at": "ADP", "to": "ADP",
#     "from": "ADP", "with": "ADP", "for": "ADP", "of": "ADP",
#     "about": "ADP", "into": "ADP", "onto": "ADP", "upon": "ADP",
#     "before": "ADP", "after": "ADP", "during": "ADP", "until": "SCONJ",
#     "between": "ADP", "among": "ADP", "by": "ADP", "through": "ADP",
#     "under": "ADP", "over": "ADP", "above": "ADP", "below": "ADP",
#     "beside": "ADP", "against": "ADP", "around": "ADP",

#     # Determiners
#     "the": "DET", "a": "DET", "an": "DET",

#     # Numbers
#     "one": "NUM", "two": "NUM", "three": "NUM", "four": "NUM",
#     "five": "NUM", "six": "NUM", "seven": "NUM", "eight": "NUM",
#     "nine": "NUM", "ten": "NUM", "eleven": "NUM", "twelve": "NUM",
#     "thirteen": "NUM", "fourteen": "NUM", "fifteen": "NUM", "sixteen": "NUM",
#     "seventeen": "NUM", "eighteen": "NUM", "nineteen": "NUM", "twenty": "NUM",
#     "thirty": "NUM", "forty": "NUM", "fifty": "NUM", "sixty": "NUM",
#     "seventy": "NUM", "eighty": "NUM", "ninety": "NUM", "hundred": "NUM",
#     "thousand": "NUM", "million": "NUM", "first": "ADJ", "second": "ADJ",
#     "third": "ADJ", "fourth": "ADJ", "fifth": "ADJ",

#     # Conjunctions
#     "and": "CCONJ", "but": "CCONJ", "or": "CCONJ", "nor": "CCONJ",
#     "yet": "CCONJ", "so": "CCONJ",
#     "because": "SCONJ", "since": "SCONJ", "although": "SCONJ", "though": "SCONJ",
#     "if": "SCONJ", "unless": "SCONJ", "when": "SCONJ", "while": "SCONJ",
#     "whereas": "SCONJ", "whether": "SCONJ", "that": "SCONJ",

#     # Particles
#     "not": "PART", "n't": "PART", "to": "PART",

#     # Interjections
#     "hello": "INTJ", "hi": "INTJ", "goodbye": "INTJ", "welcome": "INTJ",
#     "please": "INTJ", "thanks": "INTJ", "thank": "INTJ", "oh": "INTJ",
#     "ah": "INTJ", "wow": "INTJ", "ok": "INTJ", "okay": "INTJ",
#     "yes": "INTJ", "no": "INTJ",
# }

# # ================================================================
# # MULTI-WORD EXPRESSIONS (phrases to handle as units)
# # ================================================================

# YORUBA_PHRASES = {
#     "e káàárọ̀": "INTJ",
#     "e kú àsán": "INTJ",
#     "e kú ìrọ̀lẹ́": "INTJ",
#     "e kú àbọ̀": "INTJ",
#     "e ṣé": "INTJ",
#     "o dàbọ̀": "INTJ",
#     "e máa bínú": "INTJ",
#     "ẹ jọ̀wọ́": "INTJ",
#     "nítorí pé": "SCONJ",
#     "nígbà tí": "SCONJ",
#     "bí ó tilẹ̀ jẹ́ pé": "SCONJ",
#     "bí ó bá": "SCONJ",
#     "nítorí náà": "SCONJ",
#     "kí ẹ sì": "SCONJ",
# }

# ENGLISH_PHRASES = {
#     "good morning": "INTJ",
#     "good afternoon": "INTJ",
#     "good evening": "INTJ",
#     "good night": "INTJ",
#     "good bye": "INTJ",
#     "thank you": "INTJ",
#     "you are welcome": "INTJ",
#     "see you": "INTJ",
#     "even though": "SCONJ",
#     "as if": "SCONJ",
#     "so that": "SCONJ",
#     "in order to": "SCONJ",
# }

# # ================================================================
# # TOKENIZER
# # ================================================================

# def tokenize(text, lang="english"):
#     """Tokenize text preserving punctuation and diacritics."""
#     # Preserve Yoruba diacritics; split off punctuation
#     tokens = re.findall(r"[\w'\-]+|[^\w\s]", text, re.UNICODE)
#     return tokens


# # ================================================================
# # RULE-BASED POS TAGGER
# # ================================================================

# class POSTagger:
#     """
#     Rule-based POS tagger for English and Yoruba.
#     Uses lexicon lookup + morphological/positional rules.
#     """

#     def __init__(self):
#         self.yoruba_lex = {k.lower(): v for k, v in YORUBA_LEXICON.items()}
#         self.english_lex = {k.lower(): v for k, v in ENGLISH_LEXICON.items()}

#     # -------- helpers --------
#     def _is_punct(self, token):
#         return bool(re.fullmatch(r"[^\w\s]+", token))

#     def _is_number(self, token):
#         return bool(re.fullmatch(r"\d+([.,]\d+)*", token))

#     def _is_proper_noun(self, token):
#         # Starts with capital and is not sentence-initial check (handled elsewhere)
#         return token[0].isupper() if token else False

#     # -------- English rules --------
#     def _english_morphology(self, token):
#         t = token.lower()
#         if t.endswith("ing") and len(t) > 5:
#             return "VERB"
#         if t.endswith("ed") and len(t) > 4:
#             return "VERB"
#         if t.endswith("ly") and len(t) > 4:
#             return "ADV"
#         if t.endswith("tion") or t.endswith("ment") or t.endswith("ness"):
#             return "NOUN"
#         if t.endswith("ful") or t.endswith("ous") or t.endswith("ive"):
#             return "ADJ"
#         if t.endswith("s") and len(t) > 3:
#             return "NOUN"  # plural guess
#         return "NOUN"  # default fallback

#     def tag_english(self, text):
#         tokens = tokenize(text, "english")
#         tagged = []
#         for i, tok in enumerate(tokens):
#             if self._is_punct(tok):
#                 tagged.append((tok, "PUNCT"))
#                 continue
#             if self._is_number(tok):
#                 tagged.append((tok, "NUM"))
#                 continue
#             key = tok.lower()
#             if key in self.english_lex:
#                 tag = self.english_lex[key]
#             elif i > 0 and self._is_proper_noun(tok):
#                 tag = "PROPN"
#             else:
#                 tag = self._english_morphology(tok)
#             tagged.append((tok, tag))
#         return tagged

#     # -------- Yoruba rules --------
#     def _yoruba_morphology(self, token):
#         t = token.lower()
#         # Yoruba verb-forming prefixes
#         if t.startswith("ìk") or t.startswith("ìt") or t.startswith("ìj"):
#             return "NOUN"  # nominalized form
#         if t.startswith("à") and len(t) > 2:
#             return "NOUN"  # nominalization prefix 'à-'
#         if t.startswith("ì") and len(t) > 2:
#             return "NOUN"  # nominalization prefix 'ì-'
#         if t.startswith("ol") or t.startswith("al"):
#             return "NOUN"  # agentive prefix 'olù-', 'alá-'
#         return "NOUN"

#     def tag_yoruba(self, text):
#         tokens = tokenize(text, "yoruba")
#         tagged = []
#         for i, tok in enumerate(tokens):
#             if self._is_punct(tok):
#                 tagged.append((tok, "PUNCT"))
#                 continue
#             if self._is_number(tok):
#                 tagged.append((tok, "NUM"))
#                 continue
#             key = tok.lower()
#             if key in self.yoruba_lex:
#                 tag = self.yoruba_lex[key]
#             elif i > 0 and self._is_proper_noun(tok):
#                 tag = "PROPN"
#             else:
#                 tag = self._yoruba_morphology(tok)
#             tagged.append((tok, tag))
#         return tagged


# # ================================================================
# # DATASET TAGGING FUNCTION
# # ================================================================

# def tag_dataset(dataset):
#     """
#     Return a POS-tagged version of the education dataset.
#     Structure mirrors original but adds 'english_pos' and 'yoruba_pos'.
#     """
#     tagger = POSTagger()
#     tagged_dataset = {}

#     for section, examples in dataset.items():
#         tagged_section = []
#         for example in examples:
#             en_tags = tagger.tag_english(example["english"])
#             yo_tags = tagger.tag_yoruba(example["yoruba"])
#             tagged_section.append({
#                 "english": example["english"],
#                 "yoruba": example["yoruba"],
#                 "english_pos": en_tags,
#                 "yoruba_pos": yo_tags,
#             })
#         tagged_dataset[section] = tagged_section
#     return tagged_dataset


# # ================================================================
# # EXPORT UTILITIES
# # ================================================================

# def export_tagged_jsonl(tagged_dataset, path="yoruba_english_pos_tagged.jsonl"):
#     """Export the tagged dataset to JSONL for use in translation pipelines."""
#     with open(path, "w", encoding="utf-8") as f:
#         for section, examples in tagged_dataset.items():
#             for ex in examples:
#                 record = {"section": section, **ex}
#                 f.write(json.dumps(record, ensure_ascii=False) + "\n")


# def tagged_summary(tagged_dataset):
#     """Return a frequency count of POS tags across both languages."""
#     en_counts = defaultdict(int)
#     yo_counts = defaultdict(int)
#     for examples in tagged_dataset.values():
#         for ex in examples:
#             for _, tag in ex["english_pos"]:
#                 en_counts[tag] += 1
#             for _, tag in ex["yoruba_pos"]:
#                 yo_counts[tag] += 1
#     return {"english": dict(en_counts), "yoruba": dict(yo_counts)}


# # ================================================================
# # RULE-BASED TRANSLATION INTEGRATION HELPER
# # ================================================================

# def to_translation_rule_format(tagged_example):
#     """
#     Convert a tagged example into a format suitable for feeding into
#     a rule-based translation engine. Produces aligned token+POS pairs.

#     Returns:
#         {
#           "src_tokens": [...],
#           "src_pos":    [...],
#           "tgt_tokens": [...],
#           "tgt_pos":    [...]
#         }
#     """
#     src_tokens, src_pos = zip(*tagged_example["english_pos"]) if tagged_example["english_pos"] else ([], [])
#     tgt_tokens, tgt_pos = zip(*tagged_example["yoruba_pos"]) if tagged_example["yoruba_pos"] else ([], [])
#     return {
#         "src_tokens": list(src_tokens),
#         "src_pos":    list(src_pos),
#         "tgt_tokens": list(tgt_tokens),
#         "tgt_pos":    list(tgt_pos),
#     }


# # ================================================================
# # DEMO
# # ================================================================

# if __name__ == "__main__":
#     # Assumes `education_dataset` is already loaded in the environment
#     try:
#         tagged = tag_dataset(education_dataset)
#     except NameError:
#         # Fallback demo if dataset not imported
#         demo = {
#             "demo": [
#                 {"english": "Good morning, teacher.", "yoruba": "E káàárọ̀, olùkọ́."},
#                 {"english": "Open your book.", "yoruba": "Ṣí ìwé rẹ."},
#             ]
#         }
#         tagged = tag_dataset(demo)

#     # Print first 3 tagged examples from first section
#     first_section = next(iter(tagged))
#     print(f"=== Section: {first_section} ===\n")
#     for ex in tagged[first_section][:3]:
#         print("EN:", ex["english"])
#         print("    tags:", ex["english_pos"])
#         print("YO:", ex["yoruba"])
#         print("    tags:", ex["yoruba_pos"])
#         print()

#     # Summary
#     summary = tagged_summary(tagged)
#     print("English tag counts:", summary["english"])
#     print("Yoruba  tag counts:", summary["yoruba"])

#     # Export
#     export_tagged_jsonl(tagged, "yoruba_english_pos_tagged.jsonl")
#     print("\nExported to yoruba_english_pos_tagged.jsonl")