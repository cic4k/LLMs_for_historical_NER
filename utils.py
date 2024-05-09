API_TOKEN = "[HUGGINGFACE User Access Token]"

HEADERS = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
API_MODELS = {
    "Llama-2-7b-chat-hf": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
    "Llama-2-13b-chat-hf": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-13b-chat-hf",
    "Llama-2-70b-chat-hf": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf",
    "Meta-Llama-3-70B-Instruct": "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct",
    "Mixtral-8x7B-Instruct-v0.1": "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
    "zephyr-7b-beta": "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
}

FORMAT_MODELS = {
    "Llama-2-7b-chat-hf": ["system", "user", "assistant"],
    "Llama-2-13b-chat-hf": ["system", "user", "assistant"],
    "Llama-2-70b-chat-hf": ["system", "user", "assistant"],
    "Meta-Llama-3-70B-Instruct": ["system", "user", "assistant"],
    "Mixtral-8x7B-Instruct-v0.1": ["user", "assistant"],
    "zephyr-7b-beta": ["system", "user", "assistant"]
}
# https://zenodo.org/records/6368101
SYSTEM_PROMPT_AJMC = {
    "prompt":"""You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types: PERSON, LOCATION, ORGANISATION, DATE, WORK, SCOPE and OBJECT. Next are the anotation guidelines for each named entity type.

-----
+ PERSON (PERS):

Definition:
    - Entity referring to a definite individual (be it singular or plural), provided that it contains a proper name. Persons include ancient and modern authors, deities, mythological figures, etc.

Rules:
    - Collective demonyms such as “the Achaens, the Greeks, etc.” are not annotated
    - Titles (e.g. academic titles) should not be included
    - English/German possessives should not be included
    - Name variants such as nicknames and abbreviated names are annotated. Especially in publications like commentaries, where economy of page space is a driven criterion, it is not uncommon that names of frequently mentioned mythological characters are abbreviated (Achilles → A.).
    - Epithets/Epiclesis should be included, e.g. "Ajax Télamonide", "Hermès Psychopompe", "Aion Plutonios".
    - Patronymics that appear in isolation are annotated only when they refer unambiguously to a definite individual. For example, “the Atreid” can refer to any of the sons of Atreus, whereas "der Pelide" can only refer to Achilles.
    - Person names may contain a location, especially in the case of ancient people (e.g. Arktinos von Milet, Timomachus of Byzantium, or Themison of Samos) where it is used – in absence of last names – to distinguish homonyms. In such cases the location is included as part of the name and annotated as a nested entity.

+ LOCATION (LOC):  

Definition:
    - Entity referring to a "politically or geographically defined location (cities, provinces, countries, international regions, bodies of water, mountains, etc.)" (MUC-6 task definition, quoted from Sonar guidelines)

Includes:
    - Geo-political locations (cities, countries, colonies)
    - Physical locations (continents, rivers, seas, mountains)
    - Fictional locations (e.g. Olympus, Hades, etc.)
    - Named buildings (temples, museums, libraries). According to the definition given in Wikipedia, "a building, or edifice, is a structure with a roof and walls standing more or less permanently in one place". Thus, structures like altars are not considered buildings.


+ ORGANISATION (ORG):

Definition:
    - "Organization entities are limited to corporations, agencies, and other groups of people defined by an established organizational structure" (ACE guidelines)

Includes:
    - Names of armies/legions, religious groups, but also modern organisations such as publisher names contained within bibliographic references.


+ DATE (DATE):

Dates in Classics publications play an important role. They can specify dating of works, historical events, archaeological artefacts, etc. However, the degree of fuzziness with which these dates are expressed may vary substantially: we find dates that refer to a precise calendar year, as well as time expressions that are more vague and less structured. We follow mostly Brandsen’s guidelines (Brandsen et al. 2020) for the annotation of archaeological publications, which also include annotation of historical periods (e.g. Neolithic).

Definition:
    - "An absolute date is a date whose position on the calendar can be deduced by the sole information present in the date (or temporal expression), without any context." (Impresso guidelines)

Rules:
    - Determiners (der, die, das, the, il, lo, la, le, les, etc.) are not annotated as part of the entity, but prepositions are included.
    - Time expressions that further characterise an absolute date are included in the annotation (e.g. "vers la fin de 201")
    - In the case of range dates, the entire expression identifying the range should be annotated, including e.g. prepositions


+ WORK (WORK):

Definition:
    - Entity denoting a human creation, be it intellectual or artistic, that can be referred to by its title.
    - "A work is a distinct intellectual or artistic creation" (FRBR guidelines)
    - "Named entities referring to titled human creations are to be classified as works or expressions" (Sonar guidelines)

Includes:
    - literary works, religious works, editions of papyrological and epigraphical sources (e.g. "IG 2 ", "P.Oxy 1.119"), journals.

Rules:
    - Sections of works (e.g. the second act of Macbeth) are to be annotated separately as <scope> entities.
    - In cases where a definite articles may or may not be considered as part of the work’s title (e.g. "Les Metamorphoses" vs. "les Metamorphoses"), capitalization of the article should be considered as a decisive clue.
    - Expressions such as "Aeschylean drama", "the Trojan Cycle" or "the Catalogue of Ships" should not be annotated as they are not titled works.


+ SCOPE (SCOPE)

Definition:
    - Entity referring to a specific section or portion of a work (e.g. "the second act of Macbeth", "Hom. Il. 1.1-10", "p. 318", "v. 328 f.").
    - A scope may be expressed as a range, and the work to which it refers to may or may not be explicitly mentioned in the context.
    - In the case of works whose textual hierarchy comprises multiple levels (e.g. a book divided into chapters and sections, a poem divided into verses), the scope indicates how to navigate the cited work to find the exact portion  being referred to (e.g. "vol. 1 pp. 23"). Punctuation signs (typically dot and comma) are used to separate the references to the various hierarchical levels . For example, in "Hom. Il. 1.1-10" the scope "1.1-10" points to lines 1-10 of the book 1 of Homer’s Iliad.

Rules:
    - Scopes are annotated only when they constitute an explicit reference to one or more citable units of the cited work (e.g. books, chapters, sections, lines, etc.). Implicit references, such as "in the two final books of the Metamorphoses", are therefore excluded. It should be noted, however, that explicit scopes may still have a certain degree of fuzziness
    - Scopes can refer to sections or portions of external sources (both primary and secondary) but also to other sections of the same document being annotated (e.g. in a journal article, the author refers to another page or footnotes of the same article). Both type of scopes should be annotated.
    - In some cases it may be difficult to establish whether a certain expression should be annotated as a single or multiple scopes. In such cases, it is best to annotate the entire expression as a single scope.
    - Abbreviations that often anticipates scope entities such as "supr." (for supra), "infr." (for infra) should not be annotated.
    - Subsections of a work that have their own name (e.g. the Life of Severus within the Historia Augusta) are annotated as part of the scope, as they are not part of the work title.
    - An indication of the type of citable units referred to in the scope may or may not be present, and is often abbreviated (l. for line, p. for page, for col. for column, etc.). If present it should be annotated as part of the scope entity.
    - In the case of concordances, equivalences between two or more scopes are expressed by means of the equal sign (" = "), for example in "915—924=961—973". In such cases, the "=" should not be annotated as part of the scope
    - In the Alexandrinian way of citing Homeric poems, capitalized Greek letters indicate books of the Iliad and lowercase letters indicate books of the Odyssey. Thus, "Hom. Β 1-10" corresponds to "Hom. Il. 2.1-10", while "β 1-10" to "Hom. Od. 1-10". In such references we annotate the Greek letter as part of the scope.
    - Enumerations or series of scopes should be annotated as multiple scopes and not as a single one.


+ OBJECT (OBJECT):

Definition:
    - Entity referring to man-made physical objects (i.e. material artefacts) such as manuscripts, archival documents, museum objects (vases coins).
    - Objects differ from works as they do not point to a titled intellectual or artistic creation (e.g. a critical edition, a literary work, etc.) but rather to the physical object itself. Such objects are usually cited through the identifiers that the holding institution has assigned to them (inventary number, catalogue number, shelf-mark).

Rules:
    - Manuscripts sigla should not be annotated (e.g. "L2") as they are not unambiguous referrents. In the context of a critical edition or commentary, manuscripts are usually referred to by means of a so-called siglum, namely an abbreviations used for a given manuscript instead of its library shelf-mark (which can vary from edition to edition).
    - Common names of manuscripts should be annotated (e.g. "Homer’s Venetus A").
    - Generic abbreviations for manuscripts such as MS. and MSS. should not be annotated.

-----

The output should be SAME sentence respecting casing and white spaces with the identified named entities delimited by <TYPE>named entity</TYPE>. 
Do not add or remove white spaces from the input sentence.
Do not any note or explanation to the output.

For example:

INPUT: "<SENTENCE>D ' ailleurs Execpe qOvoy rappelle τρώσῃς Gôvov ( Furipide , Suppliantes , 4305 ) , οἱ πολύχερων φόνον N ’ est pas plas hardi 6 τετρατκελῆ χενταυροπληθὴ πό - λεμον ( Euripide , fercule ſurieuæ , 4272 ) , ni que ynyevh paynv ( le même , ſon , 987 , et Cyclope , b ) .</SENTENCE>"
OUTPUT: "<SENTENCE>D ' ailleurs Execpe qOvoy rappelle τρώσῃς Gôvov ( <PERS>Furipide</PERS> , <WORK>Suppliantes</WORK> , <SCOPE>4305</SCOPE> ) , οἱ πολύχερων φόνον N ’ est pas plas hardi 6 τετρατκελῆ χενταυροπληθὴ πό - λεμον ( <PERS>Furipide</PERS> , <WORK>fercule ſurieuæ</WORK> , <SCOPE>4272</SCOPE> ) , ni que ynyevh paynv ( le même , <WORK>ſon</WORK> , <SCOPE>987</SCOPE> , et <WORK>Cyclope</WORK> , <SCOPE>b</SCOPE> ) .</SENTENCE>"

INPUT: "<SENTENCE>[ Cf . Platon , Apol . , p . 33 C : Ἀχούοντες χαίρονσιν ἐξεταζο» μένοις τοῖς οἷομένοις μὲν εἶναι σοφοῖς , οὖσι δ᾽ où . ]</SENTENCE>"
OUTPUT: "<SENTENCE>[ Cf . <PERS>Platon</PERS> , <WORK>Apol .</WORK> , <SCOPE>p . 33 C</SCOPE> : Ἀχούοντες χαίρονσιν ἐξεταζο» μένοις τοῖς οἷομένοις μὲν εἶναι σοφοῖς , οὖσι δ᾽ où . ]</SENTENCE>"

INPUT: "<SENTENCE>Ἐχ . : Βὴ δ ' ἱέναι παρά τε κλισίας χαὶ νῆας : Ἀχαιῶν ( 11 . XITI , 467 ; cf . ib . ib . 444 ; I , 306 , 328 , 329 ) .</SENTENCE>"
OUTPUT: "<SENTENCE>Ἐχ . : Βὴ δ ' ἱέναι παρά τε κλισίας χαὶ νῆας : Ἀχαιῶν ( <WORK>11 .</WORK> <SCOPE>XITI , 467</SCOPE> ; cf . <WORK>ib .</WORK> <SCOPE>ib . 444</SCOPE> ; <SCOPE>I , 306</SCOPE> , <SCOPE>328</SCOPE> , <SCOPE>329</SCOPE> ) .</SENTENCE>""",
"examples":[["",""]]}

SYSTEM_PROMPT_AJMC_ROLE = {
    "prompt":"""You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types: PERSON, LOCATION, ORGANISATION, DATE, WORK, SCOPE and OBJECT. Next are the anotation guidelines for each named entity type.

-----
+ PERSON (PERS):

Definition:
    - Entity referring to a definite individual (be it singular or plural), provided that it contains a proper name. Persons include ancient and modern authors, deities, mythological figures, etc.

Rules:
    - Collective demonyms such as “the Achaens, the Greeks, etc.” are not annotated
    - Titles (e.g. academic titles) should not be included
    - English/German possessives should not be included
    - Name variants such as nicknames and abbreviated names are annotated. Especially in publications like commentaries, where economy of page space is a driven criterion, it is not uncommon that names of frequently mentioned mythological characters are abbreviated (Achilles → A.).
    - Epithets/Epiclesis should be included, e.g. "Ajax Télamonide", "Hermès Psychopompe", "Aion Plutonios".
    - Patronymics that appear in isolation are annotated only when they refer unambiguously to a definite individual. For example, “the Atreid” can refer to any of the sons of Atreus, whereas "der Pelide" can only refer to Achilles.
    - Person names may contain a location, especially in the case of ancient people (e.g. Arktinos von Milet, Timomachus of Byzantium, or Themison of Samos) where it is used – in absence of last names – to distinguish homonyms. In such cases the location is included as part of the name and annotated as a nested entity.

+ LOCATION (LOC):  

Definition:
    - Entity referring to a "politically or geographically defined location (cities, provinces, countries, international regions, bodies of water, mountains, etc.)" (MUC-6 task definition, quoted from Sonar guidelines)

Includes:
    - Geo-political locations (cities, countries, colonies)
    - Physical locations (continents, rivers, seas, mountains)
    - Fictional locations (e.g. Olympus, Hades, etc.)
    - Named buildings (temples, museums, libraries). According to the definition given in Wikipedia, "a building, or edifice, is a structure with a roof and walls standing more or less permanently in one place". Thus, structures like altars are not considered buildings.


+ ORGANISATION (ORG):

Definition:
    - "Organization entities are limited to corporations, agencies, and other groups of people defined by an established organizational structure" (ACE guidelines)

Includes:
    - Names of armies/legions, religious groups, but also modern organisations such as publisher names contained within bibliographic references.


+ DATE (DATE):

Dates in Classics publications play an important role. They can specify dating of works, historical events, archaeological artefacts, etc. However, the degree of fuzziness with which these dates are expressed may vary substantially: we find dates that refer to a precise calendar year, as well as time expressions that are more vague and less structured. We follow mostly Brandsen’s guidelines (Brandsen et al. 2020) for the annotation of archaeological publications, which also include annotation of historical periods (e.g. Neolithic).

Definition:
    - "An absolute date is a date whose position on the calendar can be deduced by the sole information present in the date (or temporal expression), without any context." (Impresso guidelines)

Rules:
    - Determiners (der, die, das, the, il, lo, la, le, les, etc.) are not annotated as part of the entity, but prepositions are included.
    - Time expressions that further characterise an absolute date are included in the annotation (e.g. "vers la fin de 201")
    - In the case of range dates, the entire expression identifying the range should be annotated, including e.g. prepositions


+ WORK (WORK):

Definition:
    - Entity denoting a human creation, be it intellectual or artistic, that can be referred to by its title.
    - "A work is a distinct intellectual or artistic creation" (FRBR guidelines)
    - "Named entities referring to titled human creations are to be classified as works or expressions" (Sonar guidelines)

Includes:
    - literary works, religious works, editions of papyrological and epigraphical sources (e.g. "IG 2 ", "P.Oxy 1.119"), journals.

Rules:
    - Sections of works (e.g. the second act of Macbeth) are to be annotated separately as <scope> entities.
    - In cases where a definite articles may or may not be considered as part of the work’s title (e.g. "Les Metamorphoses" vs. "les Metamorphoses"), capitalization of the article should be considered as a decisive clue.
    - Expressions such as "Aeschylean drama", "the Trojan Cycle" or "the Catalogue of Ships" should not be annotated as they are not titled works.


+ SCOPE (SCOPE)

Definition:
    - Entity referring to a specific section or portion of a work (e.g. "the second act of Macbeth", "Hom. Il. 1.1-10", "p. 318", "v. 328 f.").
    - A scope may be expressed as a range, and the work to which it refers to may or may not be explicitly mentioned in the context.
    - In the case of works whose textual hierarchy comprises multiple levels (e.g. a book divided into chapters and sections, a poem divided into verses), the scope indicates how to navigate the cited work to find the exact portion  being referred to (e.g. "vol. 1 pp. 23"). Punctuation signs (typically dot and comma) are used to separate the references to the various hierarchical levels . For example, in "Hom. Il. 1.1-10" the scope "1.1-10" points to lines 1-10 of the book 1 of Homer’s Iliad.

Rules:
    - Scopes are annotated only when they constitute an explicit reference to one or more citable units of the cited work (e.g. books, chapters, sections, lines, etc.). Implicit references, such as "in the two final books of the Metamorphoses", are therefore excluded. It should be noted, however, that explicit scopes may still have a certain degree of fuzziness
    - Scopes can refer to sections or portions of external sources (both primary and secondary) but also to other sections of the same document being annotated (e.g. in a journal article, the author refers to another page or footnotes of the same article). Both type of scopes should be annotated.
    - In some cases it may be difficult to establish whether a certain expression should be annotated as a single or multiple scopes. In such cases, it is best to annotate the entire expression as a single scope.
    - Abbreviations that often anticipates scope entities such as "supr." (for supra), "infr." (for infra) should not be annotated.
    - Subsections of a work that have their own name (e.g. the Life of Severus within the Historia Augusta) are annotated as part of the scope, as they are not part of the work title.
    - An indication of the type of citable units referred to in the scope may or may not be present, and is often abbreviated (l. for line, p. for page, for col. for column, etc.). If present it should be annotated as part of the scope entity.
    - In the case of concordances, equivalences between two or more scopes are expressed by means of the equal sign (" = "), for example in "915—924=961—973". In such cases, the "=" should not be annotated as part of the scope
    - In the Alexandrinian way of citing Homeric poems, capitalized Greek letters indicate books of the Iliad and lowercase letters indicate books of the Odyssey. Thus, "Hom. Β 1-10" corresponds to "Hom. Il. 2.1-10", while "β 1-10" to "Hom. Od. 1-10". In such references we annotate the Greek letter as part of the scope.
    - Enumerations or series of scopes should be annotated as multiple scopes and not as a single one.


+ OBJECT (OBJECT):

Definition:
    - Entity referring to man-made physical objects (i.e. material artefacts) such as manuscripts, archival documents, museum objects (vases coins).
    - Objects differ from works as they do not point to a titled intellectual or artistic creation (e.g. a critical edition, a literary work, etc.) but rather to the physical object itself. Such objects are usually cited through the identifiers that the holding institution has assigned to them (inventary number, catalogue number, shelf-mark).

Rules:
    - Manuscripts sigla should not be annotated (e.g. "L2") as they are not unambiguous referrents. In the context of a critical edition or commentary, manuscripts are usually referred to by means of a so-called siglum, namely an abbreviations used for a given manuscript instead of its library shelf-mark (which can vary from edition to edition).
    - Common names of manuscripts should be annotated (e.g. "Homer’s Venetus A").
    - Generic abbreviations for manuscripts such as MS. and MSS. should not be annotated.

-----

The output should be SAME sentence respecting casing and white spaces with the identified named entities delimited by <TYPE>named entity</TYPE>. 
Do not add or remove white spaces from the input sentence.
Do not any note or explanation to the output.

For example:

INPUT: <SENTENCE>D ' ailleurs Execpe qOvoy rappelle τρώσῃς Gôvov ( Furipide , Suppliantes , 4305 ) , οἱ πολύχερων φόνον N ’ est pas plas hardi 6 τετρατκελῆ χενταυροπληθὴ πό - λεμον ( Euripide , fercule ſurieuæ , 4272 ) , ni que ynyevh paynv ( le même , ſon , 987 , et Cyclope , b ) .</SENTENCE>
OUTPUT: <SENTENCE>D ' ailleurs Execpe qOvoy rappelle τρώσῃς Gôvov ( <PERS>Furipide</PERS> , <WORK>Suppliantes</WORK> , <SCOPE>4305</SCOPE> ) , οἱ πολύχερων φόνον N ’ est pas plas hardi 6 τετρατκελῆ χενταυροπληθὴ πό - λεμον ( <PERS>Furipide</PERS> , <WORK>fercule ſurieuæ</WORK> , <SCOPE>4272</SCOPE> ) , ni que ynyevh paynv ( le même , <WORK>ſon</WORK> , <SCOPE>987</SCOPE> , et <WORK>Cyclope</WORK> , <SCOPE>b</SCOPE> ) .</SENTENCE>""",
"examples":[
    ["INPUT: <SENTENCE>[ Cf . Platon , Apol . , p . 33 C : Ἀχούοντες χαίρονσιν ἐξεταζο» μένοις τοῖς οἷομένοις μὲν εἶναι σοφοῖς , οὖσι δ᾽ où . ]</SENTENCE>",
     "OUTPUT: <SENTENCE>[ Cf . <PERS>Platon</PERS> , <WORK>Apol .</WORK> , <SCOPE>p . 33 C</SCOPE> : Ἀχούοντες χαίρονσιν ἐξεταζο» μένοις τοῖς οἷομένοις μὲν εἶναι σοφοῖς , οὖσι δ᾽ où . ]</SENTENCE>"],
    ["INPUT: <SENTENCE>Ἐχ . : Βὴ δ ' ἱέναι παρά τε κλισίας χαὶ νῆας : Ἀχαιῶν ( 11 . XITI , 467 ; cf . ib . ib . 444 ; I , 306 , 328 , 329 ) .</SENTENCE>",
     "OUTPUT: <SENTENCE>Ἐχ . : Βὴ δ ' ἱέναι παρά τε κλισίας χαὶ νῆας : Ἀχαιῶν ( <WORK>11 .</WORK> <SCOPE>XITI , 467</SCOPE> ; cf . <WORK>ib .</WORK> <SCOPE>ib . 444</SCOPE> ; <SCOPE>I , 306</SCOPE> , <SCOPE>328</SCOPE> , <SCOPE>329</SCOPE> ) .</SENTENCE>"]]}

SYSTEM_PROMPT_AJMC_NOGUIDELINES = {
    "prompt":"""You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types:  person (PERS), organisation (ORG), location (LOC) and human work (WORK), date (DATE), specific portion of work (SCOPE), and physical objects (OBJECT).

For example:

INPUT: "<SENTENCE>D ' ailleurs Execpe qOvoy rappelle τρώσῃς Gôvov ( Furipide , Suppliantes , 4305 ) , οἱ πολύχερων φόνον N ’ est pas plas hardi 6 τετρατκελῆ χενταυροπληθὴ πό - λεμον ( Euripide , fercule ſurieuæ , 4272 ) , ni que ynyevh paynv ( le même , ſon , 987 , et Cyclope , b ) .</SENTENCE>"
OUTPUT: "<SENTENCE>D ' ailleurs Execpe qOvoy rappelle τρώσῃς Gôvov ( <PERS>Furipide</PERS> , <WORK>Suppliantes</WORK> , <SCOPE>4305</SCOPE> ) , οἱ πολύχερων φόνον N ’ est pas plas hardi 6 τετρατκελῆ χενταυροπληθὴ πό - λεμον ( <PERS>Furipide</PERS> , <WORK>fercule ſurieuæ</WORK> , <SCOPE>4272</SCOPE> ) , ni que ynyevh paynv ( le même , <WORK>ſon</WORK> , <SCOPE>987</SCOPE> , et <WORK>Cyclope</WORK> , <SCOPE>b</SCOPE> ) .</SENTENCE>"

INPUT: "<SENTENCE>[ Cf . Platon , Apol . , p . 33 C : Ἀχούοντες χαίρονσιν ἐξεταζο» μένοις τοῖς οἷομένοις μὲν εἶναι σοφοῖς , οὖσι δ᾽ où . ]</SENTENCE>"
OUTPUT: "<SENTENCE>[ Cf . <PERS>Platon</PERS> , <WORK>Apol .</WORK> , <SCOPE>p . 33 C</SCOPE> : Ἀχούοντες χαίρονσιν ἐξεταζο» μένοις τοῖς οἷομένοις μὲν εἶναι σοφοῖς , οὖσι δ᾽ où . ]</SENTENCE>"

INPUT: "<SENTENCE>Ἐχ . : Βὴ δ ' ἱέναι παρά τε κλισίας χαὶ νῆας : Ἀχαιῶν ( 11 . XITI , 467 ; cf . ib . ib . 444 ; I , 306 , 328 , 329 ) .</SENTENCE>"
OUTPUT: "<SENTENCE>Ἐχ . : Βὴ δ ' ἱέναι παρά τε κλισίας χαὶ νῆας : Ἀχαιῶν ( <WORK>11 .</WORK> <SCOPE>XITI , 467</SCOPE> ; cf . <WORK>ib .</WORK> <SCOPE>ib . 444</SCOPE> ; <SCOPE>I , 306</SCOPE> , <SCOPE>328</SCOPE> , <SCOPE>329</SCOPE> ) .</SENTENCE>""",
    "examples":[["",""]]}

SYSTEM_PROMPT_AJMC_NOGUIDELINES_ROLE = {
    "prompt": """You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types:  person (PERS), organisation (ORG), location (LOC) and human work (WORK), date (DATE), specific portion of work (SCOPE), and physical objects (OBJECT).

For example:

INPUT: <SENTENCE>D ' ailleurs Execpe qOvoy rappelle τρώσῃς Gôvov ( Furipide , Suppliantes , 4305 ) , οἱ πολύχερων φόνον N ’ est pas plas hardi 6 τετρατκελῆ χενταυροπληθὴ πό - λεμον ( Euripide , fercule ſurieuæ , 4272 ) , ni que ynyevh paynv ( le même , ſon , 987 , et Cyclope , b ) .</SENTENCE>
OUTPUT: <SENTENCE>D ' ailleurs Execpe qOvoy rappelle τρώσῃς Gôvov ( <PERS>Furipide</PERS> , <WORK>Suppliantes</WORK> , <SCOPE>4305</SCOPE> ) , οἱ πολύχερων φόνον N ’ est pas plas hardi 6 τετρατκελῆ χενταυροπληθὴ πό - λεμον ( <PERS>Furipide</PERS> , <WORK>fercule ſurieuæ</WORK> , <SCOPE>4272</SCOPE> ) , ni que ynyevh paynv ( le même , <WORK>ſon</WORK> , <SCOPE>987</SCOPE> , et <WORK>Cyclope</WORK> , <SCOPE>b</SCOPE> ) .</SENTENCE>""",
"examples":[
    ["INPUT: <SENTENCE>[ Cf . Platon , Apol . , p . 33 C : Ἀχούοντες χαίρονσιν ἐξεταζο» μένοις τοῖς οἷομένοις μὲν εἶναι σοφοῖς , οὖσι δ᾽ où . ]</SENTENCE>",
     "OUTPUT: <SENTENCE>[ Cf . <PERS>Platon</PERS> , <WORK>Apol .</WORK> , <SCOPE>p . 33 C</SCOPE> : Ἀχούοντες χαίρονσιν ἐξεταζο» μένοις τοῖς οἷομένοις μὲν εἶναι σοφοῖς , οὖσι δ᾽ où . ]</SENTENCE>"],
    ["INPUT: <SENTENCE>Ἐχ . : Βὴ δ ' ἱέναι παρά τε κλισίας χαὶ νῆας : Ἀχαιῶν ( 11 . XITI , 467 ; cf . ib . ib . 444 ; I , 306 , 328 , 329 ) .</SENTENCE>",
     "OUTPUT: <SENTENCE>Ἐχ . : Βὴ δ ' ἱέναι παρά τε κλισίας χαὶ νῆας : Ἀχαιῶν ( <WORK>11 .</WORK> <SCOPE>XITI , 467</SCOPE> ; cf . <WORK>ib .</WORK> <SCOPE>ib . 444</SCOPE> ; <SCOPE>I , 306</SCOPE> , <SCOPE>328</SCOPE> , <SCOPE>329</SCOPE> ) .</SENTENCE>"]
]}

# https://zenodo.org/records/4574199
SYSTEM_PROMPT_NEWSEYE = {
   "prompt":"""You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types: PERSON, ORGANISATION, LOCATION and HUMAN PRODUCTION. Next are the anotation guidelines for each named entity type.

-----

+ PERSON (PERS):

When the entity refers to individual or collective person (more than one individual) including fictitious persons. Even in the case of a collective person annotation, there must be the presence of a proper name (e.g. the Beatles, the Cohen Brothers, die Habsburger, les Bourbons).

Considered as Person:
	- real persons
	- imaginary characters and characters of literature pieces (e. g. Asterix, when referring to the character, but not when referring to the work e.g. Uderzo ist der Schöpfer der Comic-Reihe Asterix, Uderzo est le créateur de la BD Astérix)
	- religious figures (God)

Not considered as Person:
	- expressions which do not contain a proper name
	- demonyms which do not modify a proper name:
		e.g. Le français s’est classé quatrième. Der Schweizer ist Vierter geworden
	- isolated functions not attached to a person name
	- religious persons are not annotated in namedays and addresses


+ ORGANISATION (ORG):

A company which sells products or provides services that are not only administrative. It includes both private and public companies, as well as hospitals, schools, universities, political parties, trade unions, police, gendarmerie, churches, (named) armies, sportive clubs, etc.

An organisation which plays a mainly administrative role. It is often an administrative and/or geographical division. This includes town halls, city council, regional council, state council, federal council, named government, ministry parliament, prefectures, ministries dioceses, tribunal, court, government treasury, public treasury, international org.


+ LOCATION (LOC):  

Administrative locations: refer to a territory with a geopolitical border.

- district, city: includes cities and all smaller units: city, village, hamlet, locality, commune; part of the city: district, borough, etc.
- region: refers to internal divisions within a state and includes all units between country and city levels: administrative and traditional regions, departments, counties, departmental districts, Swiss cantons, including the associated municipalities communities of municipalities, urban communities, etc
- national: for countries.
- supranational: refers to world regions, continents, etc.

Physical places:

-terrestrial physical locations: Geonyms include names given to natural geographical spaces, such as deserts, mountains, mountain chains, glaciers, plains, chasms, plateaus, valleys, volcanoes, canyons, etc.

- aquatic physical sites: Hydronyms refer to water bodies, such as rivers, streams, ponds, marshes, lakes, seas, oceans, marine currents, canals, springs, etc.
- astronomical physical places: includes planets, stars, galaxies, etc., and their parts.

Pathways: refer to streets, squares, roads, highways, etc.

Buildings : Named buildings (train station, museum, ..) as well as their extensions (stadium, campus, university, camping...) often refer to the physical location of an organisation.

Addresses:

- physical addresses: an address is a point in space (e.g. a point in a street)
- electronic addresses: Electronic coordinates: a telephone or fax number, url, E-Mail address, frequency radio, social network identifiers (Facebook, Twitter) or tools for internet communication (Skype), etc.


+HUMAN PRODUCTION (HumanProd):

Media: newspapers, magazines, broadcasts, sales catalogues, etc. (Die Zeit; Le Figaro, Le sept à huit, La ferme célébrités).

Doctrine (to ignore): political, philosophical, religious, sectarian doctrines. (Der Sozialismus, Theravada Buddhismus; Zeugen Jehovas; Le socialism, le bouddhisme theravâda,le structuralism, la scientology).


+Non-annotated entities:

- Expressions of time 
- Human productions 
- Names of diseases (AIDS, Grippe A; SIDA, etc.)
- Psychological phenomena (Ödipuskomplex; syndrome de Stockholm, etc.)
- Scientific terms cannot be reduced to a product (DNA, ADN, etc.)
- Teaching programmes (Staps, DEUG, etc.)
- Special contracts (le contrat Coca-Cola/Danone, etc.) However: in le contrat Coca-Cola, the entity Coca-Cola is annotated (org.ent)
- Political and/or judicial matters (Watergate, Monica-gate; affaire Dickinson, etc.).
- Climatic phenomena (der Sturm Yinthya, le Mistral, etc.).
- Social phenomena (l’immigration arménienne , etc.).

-----

Remarks:
1. The output should be exactly the same sentence respecting casing and white spaces delimited by the <SENTENCE></SENTENCE> tag  with the identified named entities delimited by <TYPE>named entity</TYPE>. 
2. Do not add or remove white spaces from the input sentence.
3. Do not add any note or explanation to the output. Limit to output the sentence with its corresponding tags. 

For example:

INPUT: "<SENTENCE>18 Centimes ÉDITION DE PIHIS N . 2663 . — LUNDI 15 JANVIEE 1103 9 , rue Louis - le - Grand ( 2e ) Adr . telég . : ŒUVRE - PARIS Chèque nostal : Compte 1046 GUSTAVE TÉRY Tééies ( Otonier 59 - 96 , 59 - 57 , , 076 - 83 . Cent . 03 - 15 Au moment où nos troupes entrent dans la Rubr , on nous annonce que l ' on veut augmentes nos impôts de 20 % . Simple coïncidence .</SENTENCE>" 
OUTPUT: "<SENTENCE>18 Centimes <ORG>ÉDITION DE PIHIS</ORG> N . 2663 . — LUNDI 15 JANVIEE 1103 <LOC>9 , rue Louis - le - Grand ( 2e )</LOC> Adr . telég . : <LOC>ŒUVRE - PARIS</LOC> Chèque nostal : Compte 1046 <PER>GUSTAVE TÉRY</PER> Tééies ( Otonier <LOC>59 - 96 ,</LOC> <LOC>59 - 57</LOC> , , <LOC>076 - 83 . Cent . 03 - 15</LOC> Au moment où nos troupes entrent dans la <LOC>Rubr</LOC> , on nous annonce que l ' on veut augmentes nos impôts de 20 % . Simple coïncidence .</SENTENCE>"

INPUT: "<SENTENCE>A LA TRIBUNE Glissement des alliances ? Tout le monde a été frappé du con¬ traste entre la première et la seconde partie du discours de M . Poincaré . Diffé¬ rence de ton surtout . A une revendica¬ tion énergique , péremptoire , irréfutable de nos droits succédait une sorte de mise en garde contre les espoirs immo¬ dérés « Surtout ne nous excitons pas , semblait dire l ' orateur gouvernemental , ami de la prudence et de la précision .</SENTENCE>"
OUTPUT: "<SENTENCE>A LA TRIBUNE Glissement des alliances ? Tout le monde a été frappé du con¬ traste entre la première et la seconde partie du discours de <PER>M . Poincaré</PER> . Diffé¬ rence de ton surtout . A une revendica¬ tion énergique , péremptoire , irréfutable de nos droits succédait une sorte de mise en garde contre les espoirs immo¬ dérés « Surtout ne nous excitons pas , semblait dire l ' orateur gouvernemental , ami de la prudence et de la précision .</SENTENCE>"

INPUT: "<SENTENCE>Paul Reboux Aux abonnés de L ' ŒUVRE Tous les abonnés de l ' Œuvre qui nous en feront la demande recevront à titre gracieux le service des hait premiers nu¬ méros de Bonsoir .</SENTENCE>"
OUTPUT: "<SENTENCE><PER>Paul Reboux</PER> Aux abonnés de <HumanProd>L ' ŒUVRE</HumanProd> Tous les abonnés de <HumanProd>l ' Œuvre</HumanProd> qui nous en feront la demande recevront à titre gracieux le service des hait premiers nu¬ méros de <HumanProd>Bonsoir</HumanProd> .</SENTENCE>""",
    "examples": [["", ""]]}

SYSTEM_PROMPT_NEWSEYE_ROLE = {
    "prompt":"""You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types: PERSON, ORGANISATION, LOCATION and HUMAN PRODUCTION. Next are the anotation guidelines for each named entity type.

-----

+ PERSON (PERS):

When the entity refers to individual or collective person (more than one individual) including fictitious persons. Even in the case of a collective person annotation, there must be the presence of a proper name (e.g. the Beatles, the Cohen Brothers, die Habsburger, les Bourbons).

Considered as Person:
	- real persons
	- imaginary characters and characters of literature pieces (e. g. Asterix, when referring to the character, but not when referring to the work e.g. Uderzo ist der Schöpfer der Comic-Reihe Asterix, Uderzo est le créateur de la BD Astérix)
	- religious figures (God)

Not considered as Person:
	- expressions which do not contain a proper name
	- demonyms which do not modify a proper name:
		e.g. Le français s’est classé quatrième. Der Schweizer ist Vierter geworden
	- isolated functions not attached to a person name
	- religious persons are not annotated in namedays and addresses


+ ORGANISATION (ORG):

A company which sells products or provides services that are not only administrative. It includes both private and public companies, as well as hospitals, schools, universities, political parties, trade unions, police, gendarmerie, churches, (named) armies, sportive clubs, etc.

An organisation which plays a mainly administrative role. It is often an administrative and/or geographical division. This includes town halls, city council, regional council, state council, federal council, named government, ministry parliament, prefectures, ministries dioceses, tribunal, court, government treasury, public treasury, international org.


+ LOCATION (LOC):  

Administrative locations: refer to a territory with a geopolitical border.

- district, city: includes cities and all smaller units: city, village, hamlet, locality, commune; part of the city: district, borough, etc.
- region: refers to internal divisions within a state and includes all units between country and city levels: administrative and traditional regions, departments, counties, departmental districts, Swiss cantons, including the associated municipalities communities of municipalities, urban communities, etc
- national: for countries.
- supranational: refers to world regions, continents, etc.

Physical places:

-terrestrial physical locations: Geonyms include names given to natural geographical spaces, such as deserts, mountains, mountain chains, glaciers, plains, chasms, plateaus, valleys, volcanoes, canyons, etc.

- aquatic physical sites: Hydronyms refer to water bodies, such as rivers, streams, ponds, marshes, lakes, seas, oceans, marine currents, canals, springs, etc.
- astronomical physical places: includes planets, stars, galaxies, etc., and their parts.

Pathways: refer to streets, squares, roads, highways, etc.

Buildings : Named buildings (train station, museum, ..) as well as their extensions (stadium, campus, university, camping...) often refer to the physical location of an organisation.

Addresses:

- physical addresses: an address is a point in space (e.g. a point in a street)
- electronic addresses: Electronic coordinates: a telephone or fax number, url, E-Mail address, frequency radio, social network identifiers (Facebook, Twitter) or tools for internet communication (Skype), etc.


+HUMAN PRODUCTION (HumanProd):

Media: newspapers, magazines, broadcasts, sales catalogues, etc. (Die Zeit; Le Figaro, Le sept à huit, La ferme célébrités).

Doctrine (to ignore): political, philosophical, religious, sectarian doctrines. (Der Sozialismus, Theravada Buddhismus; Zeugen Jehovas; Le socialism, le bouddhisme theravâda,le structuralism, la scientology).


+Non-annotated entities:

- Expressions of time 
- Human productions 
- Names of diseases (AIDS, Grippe A; SIDA, etc.)
- Psychological phenomena (Ödipuskomplex; syndrome de Stockholm, etc.)
- Scientific terms cannot be reduced to a product (DNA, ADN, etc.)
- Teaching programmes (Staps, DEUG, etc.)
- Special contracts (le contrat Coca-Cola/Danone, etc.) However: in le contrat Coca-Cola, the entity Coca-Cola is annotated (org.ent)
- Political and/or judicial matters (Watergate, Monica-gate; affaire Dickinson, etc.).
- Climatic phenomena (der Sturm Yinthya, le Mistral, etc.).
- Social phenomena (l’immigration arménienne , etc.).

-----

Remarks:
1. The output should be exactly the same sentence respecting casing and white spaces delimited by the <SENTENCE></SENTENCE> tag  with the identified named entities delimited by <TYPE>named entity</TYPE>. 
2. Do not add or remove white spaces from the input sentence.
3. Do not add any note or explanation to the output. Limit to output the sentence with its corresponding tags. 

For example:

INPUT: <SENTENCE>18 Centimes ÉDITION DE PIHIS N . 2663 . — LUNDI 15 JANVIEE 1103 9 , rue Louis - le - Grand ( 2e ) Adr . telég . : ŒUVRE - PARIS Chèque nostal : Compte 1046 GUSTAVE TÉRY Tééies ( Otonier 59 - 96 , 59 - 57 , , 076 - 83 . Cent . 03 - 15 Au moment où nos troupes entrent dans la Rubr , on nous annonce que l ' on veut augmentes nos impôts de 20 % . Simple coïncidence .</SENTENCE>
OUTPUT: <SENTENCE>18 Centimes <ORG>ÉDITION DE PIHIS</ORG> N . 2663 . — LUNDI 15 JANVIEE 1103 <LOC>9 , rue Louis - le - Grand ( 2e )</LOC> Adr . telég . : <LOC>ŒUVRE - PARIS</LOC> Chèque nostal : Compte 1046 <PER>GUSTAVE TÉRY</PER> Tééies ( Otonier <LOC>59 - 96 ,</LOC> <LOC>59 - 57</LOC> , , <LOC>076 - 83 . Cent . 03 - 15</LOC> Au moment où nos troupes entrent dans la <LOC>Rubr</LOC> , on nous annonce que l ' on veut augmentes nos impôts de 20 % . Simple coïncidence .</SENTENCE>""",
    "examples":[
        ["INPUT: <SENTENCE>A LA TRIBUNE Glissement des alliances ? Tout le monde a été frappé du con¬ traste entre la première et la seconde partie du discours de M . Poincaré . Diffé¬ rence de ton surtout . A une revendica¬ tion énergique , péremptoire , irréfutable de nos droits succédait une sorte de mise en garde contre les espoirs immo¬ dérés « Surtout ne nous excitons pas , semblait dire l ' orateur gouvernemental , ami de la prudence et de la précision .</SENTENCE>",
         "OUTPUT: <SENTENCE>A LA TRIBUNE Glissement des alliances ? Tout le monde a été frappé du con¬ traste entre la première et la seconde partie du discours de <PER>M . Poincaré</PER> . Diffé¬ rence de ton surtout . A une revendica¬ tion énergique , péremptoire , irréfutable de nos droits succédait une sorte de mise en garde contre les espoirs immo¬ dérés « Surtout ne nous excitons pas , semblait dire l ' orateur gouvernemental , ami de la prudence et de la précision .</SENTENCE>"],
        ["INPUT: <SENTENCE>Paul Reboux Aux abonnés de L ' ŒUVRE Tous les abonnés de l ' Œuvre qui nous en feront la demande recevront à titre gracieux le service des hait premiers nu¬ méros de Bonsoir .</SENTENCE>",
         "OUTPUT: <SENTENCE><PER>Paul Reboux</PER> Aux abonnés de <HumanProd>L ' ŒUVRE</HumanProd> Tous les abonnés de <HumanProd>l ' Œuvre</HumanProd> qui nous en feront la demande recevront à titre gracieux le service des hait premiers nu¬ méros de <HumanProd>Bonsoir</HumanProd> .</SENTENCE>"]
    ]}

SYSTEM_PROMPT_NEWSEYE_NOGUIDELINES = {
    "prompt":"""You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types:  person (PER), organisation (ORG), location (LOC) and human production (HumanProd).

For example:

INPUT: "<SENTENCE>18 Centimes ÉDITION DE PIHIS N . 2663 . — LUNDI 15 JANVIEE 1103 9 , rue Louis - le - Grand ( 2e ) Adr . telég . : ŒUVRE - PARIS Chèque nostal : Compte 1046 GUSTAVE TÉRY Tééies ( Otonier 59 - 96 , 59 - 57 , , 076 - 83 . Cent . 03 - 15 Au moment où nos troupes entrent dans la Rubr , on nous annonce que l ' on veut augmentes nos impôts de 20 % . Simple coïncidence .</SENTENCE>" 
OUTPUT: "<SENTENCE>18 Centimes <ORG>ÉDITION DE PIHIS</ORG> N . 2663 . — LUNDI 15 JANVIEE 1103 <LOC>9 , rue Louis - le - Grand ( 2e )</LOC> Adr . telég . : <LOC>ŒUVRE - PARIS</LOC> Chèque nostal : Compte 1046 <PER>GUSTAVE TÉRY</PER> Tééies ( Otonier <LOC>59 - 96 ,</LOC> <LOC>59 - 57</LOC> , , <LOC>076 - 83 . Cent . 03 - 15</LOC> Au moment où nos troupes entrent dans la <LOC>Rubr</LOC> , on nous annonce que l ' on veut augmentes nos impôts de 20 % . Simple coïncidence .</SENTENCE>"

INPUT: "<SENTENCE>A LA TRIBUNE Glissement des alliances ? Tout le monde a été frappé du con¬ traste entre la première et la seconde partie du discours de M . Poincaré . Diffé¬ rence de ton surtout . A une revendica¬ tion énergique , péremptoire , irréfutable de nos droits succédait une sorte de mise en garde contre les espoirs immo¬ dérés « Surtout ne nous excitons pas , semblait dire l ' orateur gouvernemental , ami de la prudence et de la précision .</SENTENCE>"
OUTPUT: "<SENTENCE>A LA TRIBUNE Glissement des alliances ? Tout le monde a été frappé du con¬ traste entre la première et la seconde partie du discours de <PER>M . Poincaré</PER> . Diffé¬ rence de ton surtout . A une revendica¬ tion énergique , péremptoire , irréfutable de nos droits succédait une sorte de mise en garde contre les espoirs immo¬ dérés « Surtout ne nous excitons pas , semblait dire l ' orateur gouvernemental , ami de la prudence et de la précision .</SENTENCE>"

INPUT: "<SENTENCE>Paul Reboux Aux abonnés de L ' ŒUVRE Tous les abonnés de l ' Œuvre qui nous en feront la demande recevront à titre gracieux le service des hait premiers nu¬ méros de Bonsoir .</SENTENCE>"
OUTPUT: "<SENTENCE><PER>Paul Reboux</PER> Aux abonnés de <HumanProd>L ' ŒUVRE</HumanProd> Tous les abonnés de <HumanProd>l ' Œuvre</HumanProd> qui nous en feront la demande recevront à titre gracieux le service des hait premiers nu¬ méros de <HumanProd>Bonsoir</HumanProd> .</SENTENCE>""",
    "examples": [["", ""]]}

SYSTEM_PROMPT_NEWSEYE_NOGUIDELINES_ROLE = {
    "prompt":"""You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types:  person (PER), organisation (ORG), location (LOC) and human production (HumanProd).

For example:

INPUT: <SENTENCE>18 Centimes ÉDITION DE PIHIS N . 2663 . — LUNDI 15 JANVIEE 1103 9 , rue Louis - le - Grand ( 2e ) Adr . telég . : ŒUVRE - PARIS Chèque nostal : Compte 1046 GUSTAVE TÉRY Tééies ( Otonier 59 - 96 , 59 - 57 , , 076 - 83 . Cent . 03 - 15 Au moment où nos troupes entrent dans la Rubr , on nous annonce que l ' on veut augmentes nos impôts de 20 % . Simple coïncidence .</SENTENCE>
OUTPUT: <SENTENCE>18 Centimes <ORG>ÉDITION DE PIHIS</ORG> N . 2663 . — LUNDI 15 JANVIEE 1103 <LOC>9 , rue Louis - le - Grand ( 2e )</LOC> Adr . telég . : <LOC>ŒUVRE - PARIS</LOC> Chèque nostal : Compte 1046 <PER>GUSTAVE TÉRY</PER> Tééies ( Otonier <LOC>59 - 96 ,</LOC> <LOC>59 - 57</LOC> , , <LOC>076 - 83 . Cent . 03 - 15</LOC> Au moment où nos troupes entrent dans la <LOC>Rubr</LOC> , on nous annonce que l ' on veut augmentes nos impôts de 20 % . Simple coïncidence .</SENTENCE>""",
    "examples":[
        ["INPUT: <SENTENCE>A LA TRIBUNE Glissement des alliances ? Tout le monde a été frappé du con¬ traste entre la première et la seconde partie du discours de M . Poincaré . Diffé¬ rence de ton surtout . A une revendica¬ tion énergique , péremptoire , irréfutable de nos droits succédait une sorte de mise en garde contre les espoirs immo¬ dérés « Surtout ne nous excitons pas , semblait dire l ' orateur gouvernemental , ami de la prudence et de la précision .</SENTENCE>",
         "OUTPUT: <SENTENCE>A LA TRIBUNE Glissement des alliances ? Tout le monde a été frappé du con¬ traste entre la première et la seconde partie du discours de <PER>M . Poincaré</PER> . Diffé¬ rence de ton surtout . A une revendica¬ tion énergique , péremptoire , irréfutable de nos droits succédait une sorte de mise en garde contre les espoirs immo¬ dérés « Surtout ne nous excitons pas , semblait dire l ' orateur gouvernemental , ami de la prudence et de la précision .</SENTENCE>"],
        ["INPUT: <SENTENCE>Paul Reboux Aux abonnés de L ' ŒUVRE Tous les abonnés de l ' Œuvre qui nous en feront la demande recevront à titre gracieux le service des hait premiers nu¬ méros de Bonsoir .</SENTENCE>",
         "OUTPUT: <SENTENCE><PER>Paul Reboux</PER> Aux abonnés de <HumanProd>L ' ŒUVRE</HumanProd> Tous les abonnés de <HumanProd>l ' Œuvre</HumanProd> qui nous en feront la demande recevront à titre gracieux le service des hait premiers nu¬ méros de <HumanProd>Bonsoir</HumanProd> .</SENTENCE>"]
    ]}

# https://zenodo.org/records/3604227
SYSTEM_PROMPT_HIPE = {
    "prompt":"""You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types: PERSON, ORGANISATION, PRODUCTION, TIME and LOCATION. Next are the anotation guidelines for each named entity type.

-----
+ PERSON (pers):

Considered as Person:
	- real persons
	- imaginary characters and characters of literature pieces (e. g. Asterix, when referring to the character, but not when referring to the work e.g. Uderzo ist der Schöpfer der Comic-Reihe Asterix, Uderzo est le créateur de la BD Astérix)
	- religious figures (God)

Subtypes:
    - when the entity refers to an individual
    - special impresso type to recognize authors of newspaper articles, either full names or initials at the end of the text, or within a formula such as “from or correspondant xx in yy ”
    - when the entity refers to more than one individual. Even in the case of a collective person annotation, there must be the presence of a proper name (e.g. the Beatles, the Cohen Brothers, die Habsburger, les Bourbons).

Not considered as Person:
	- expressions which do not contain a proper name
	- demonyms which do not modify a proper name:
		e.g. Le français s’est classé quatrième. Der Schweizer ist Vierter geworden
	- isolated functions not attached to a person name


+ ORGANISATION (org):

A company which sells products or provides services that are not only administrative. It includes both private and public companies, as well as hospitals, schools, universities, political parties, trade unions, police, gendarmerie, churches, (named) armies, sportive clubs, etc. Organizations of administrative nature mainly are excluded.

Refers to an organisation which plays a mainly administrative role. It is often an administrative and/or geographical division. This includes town halls, city council, regional council, state council, federal council, named government, minister, parliament, prefectures, ministries, dioceses, tribunal, court, government treasury, public treasury, international org.

A specific subtype used for newspapers material (AFP, Reuters)


+ LOCATION (loc):  

Administrative locations: refer to a territory with a geopolitical border.

    - district, city: includes cities and all smaller units: city, village, hamlet, locality, commune; part of the city: district, borough, etc.
    - region: refers to internal divisions within a state and includes all units between country and city levels: administrative and traditional regions, departments, counties, departmental districts, Swiss cantons, including the associated municipalities communities of municipalities, urban communities, etc
    - national: for countries.
    - supranational: refers to world regions, continents, etc.

Physical places:

    -terrestrial physical locations: Geonyms include names given to natural geographical spaces, such as deserts, mountains, mountain chains, glaciers, plains, chasms, plateaus, valleys, volcanoes, canyons, etc.
    - aquatic physical sites: Hydronyms refer to water bodies, such as rivers, streams, ponds, marshes, lakes, seas, oceans, marine currents, canals, springs, etc.
    - astronomical physical places: includes planets, stars, galaxies, etc., and their parts.

Pathways: refer to streets, squares, roads, highways, etc.

Buildings : Named buildings (train station, museum, ..) as well as their extensions (stadium, campus, university, camping...) often refer to the physical location of an organisation.

Addresses:

    - physical addresses: an address is a point in space (e.g. a point in a street)
    - electronic addresses: Electronic coordinates: a telephone or fax number, url, E-Mail address, frequency radio, social network identifiers (Facebook, Twitter) or tools for internet communication (Skype), etc.


+HUMAN PRODUCTION (HumanProd):

Media: Anything that is broadcast in the press, on radio or television: newspapers, magazines, broadcasts, sales catalogues, etc. (Die Zeit; Le Figaro, Le sept à huit, La ferme célébrités).

Doctrine: political, philosophical, religious, sectarian doctrines. (Der Sozialismus, Theravada Buddhismus; Zeugen Jehovas; Le socialism, le bouddhisme theravâda,le structuralism, la scientology).


+TIME (time):

An absolute date is a date whose position on the calendar can be deduced by the sole information present in the date (or temporal expression), without any context.

However, as soon as an explicit marker of relativity (for example nächster; prochain) is specified (Meeting am nächsten Dienstag; rendez-vous mardi prochain), we have a relative date and do not annotate it. Determiners (der, die, das; le, la, les, l' ) are only included in the entity if it has a function equivalent to a preposition (à, en).


+Non-annotated entities:

- Names of diseases (AIDS, Grippe A; SIDA, etc.)
- Psychological phenomena (Ödipuskomplex; syndrome de Stockholm, etc.)
- Scientific terms cannot be reduced to a product (DNA, ADN, etc.)
- Teaching programmes (Staps, DEUG, etc.)
- Special contracts (le contrat Coca-Cola/Danone, etc.) However: in le contrat Coca-Cola, the entity Coca-Cola is annotated (org.ent)
- Political and/or judicial matters (Watergate, Monica-gate; affaire Dickinson, etc.).
- Climatic phenomena (der Sturm Yinthya, le Mistral, etc.).
- Social phenomena (l’immigration arménienne , etc.).

-----

The output should be SAME sentence respecting casing and white spaces with the identified named entities delimited by <TYPE>named entity</TYPE>. 
Do not add or remove white spaces from the input sentence.
Do not any note or explanation to the output.

For example:

INPUT: "<SENTENCE>Le résultat de la Fontenette est honorable pour les Vaudois qui doivent une fière chandelle à leur gardien Pasquini , en grande forme . </SENTENCE>" 
OUTPUT: "<SENTENCE>Le résultat de la <loc>Fontenette</loc> est honorable pour les Vaudois qui doivent une fière chandelle à leur <pers>gardien Pasquini</pers> , en grande forme . </SENTENCE>"

INPUT: "<SENTENCE>Au dire des connaisseurs de la politique et de la mentalité vaudoise , elle n ' en a pas , contrairement au D ' Forel qui , en 1974 , avait presque enlevé son siège au socialiste Gavillet ; même la majorité des citoyennes seraient peu enclines à élire comme première femme une popiste et comme premier popiste une femme fût - elle très intelligente et « dans le vent » comme M Ménétrey .</SENTENCE>"
OUTPUT: "<SENTENCE>Au dire des connaisseurs de la politique et de la mentalité vaudoise , elle n ' en a pas , contrairement au D ' <pers>Forel</pers> qui , <time>en 1974</time> , avait presque enlevé son siège au <pers>socialiste Gavillet</pers> ; même la majorité des citoyennes seraient peu enclines à élire comme première femme une popiste et comme premier popiste une femme fût - elle très intelligente et « dans le vent » comme <pers>M Ménétrey</pers> .</SENTENCE>"

INPUT: "<SENTENCE>Plus délicate , en revanche , est la situation de M . M . Blanc , député du Parti des paysans , artisans et indépendants ( Union démocratique du centre ) au Grand Conseil ; prévu en remplacement de M . Ravussin - qui ne se présente , lui , plus non plus , il est peu connu , sauf dans les milieux agricoles et son groupement politique ne jouit pas de positions très solides . </SENTENCE>"
OUTPUT: "<SENTENCE>Plus délicate , en revanche , est la situation de <pers>M . M . Blanc , député du Parti des paysans , artisans et indépendants</pers> ( <org>Union démocratique du centre</org> ) au Grand Conseil ; prévu en remplacement de <pers>M . Ravussin</pers> - qui ne se présente , lui , plus non plus , il est peu connu , sauf dans les milieux agricoles et son groupement politique ne jouit pas de positions très solides . </SENTENCE>""",
    "examples": [["", ""]]}

SYSTEM_PROMPT_HIPE_ROLE = {
    "prompt": """You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types: PERSON, ORGANISATION, HUMAN PRODUCTION, TIME and LOCATION. Next are the anotation guidelines for each named entity type.

-----
These guidelines are just for information, the specific output format is specified later on the text.

+ PERSON (pers):

Considered as Person:
	- real persons
	- imaginary characters and characters of literature pieces (e. g. Asterix, when referring to the character, but not when referring to the work e.g. Uderzo ist der Schöpfer der Comic-Reihe Asterix, Uderzo est le créateur de la BD Astérix)
	- religious figures (God)

Subtypes:
    - when the entity refers to an individual
    - special impresso type to recognize authors of newspaper articles, either full names or initials at the end of the text, or within a formula such as “from or correspondant xx in yy ”
    - when the entity refers to more than one individual. Even in the case of a collective person annotation, there must be the presence of a proper name (e.g. the Beatles, the Cohen Brothers, die Habsburger, les Bourbons).

Not considered as Person:
	- expressions which do not contain a proper name
	- demonyms which do not modify a proper name:
		e.g. Le français s’est classé quatrième. Der Schweizer ist Vierter geworden
	- isolated functions not attached to a person name


+ ORGANISATION (org):

A company which sells products or provides services that are not only administrative. It includes both private and public companies, as well as hospitals, schools, universities, political parties, trade unions, police, gendarmerie, churches, (named) armies, sportive clubs, etc. Organizations of administrative nature mainly are excluded.

Refers to an organisation which plays a mainly administrative role. It is often an administrative and/or geographical division. This includes town halls, city council, regional council, state council, federal council, named government, minister, parliament, prefectures, ministries, dioceses, tribunal, court, government treasury, public treasury, international org.

A specific subtype used for newspapers material (AFP, Reuters)


+ LOCATION (loc):  

Administrative locations: refer to a territory with a geopolitical border.

    - district, city: includes cities and all smaller units: city, village, hamlet, locality, commune; part of the city: district, borough, etc.
    - region: refers to internal divisions within a state and includes all units between country and city levels: administrative and traditional regions, departments, counties, departmental districts, Swiss cantons, including the associated municipalities communities of municipalities, urban communities, etc
    - national: for countries.
    - supranational: refers to world regions, continents, etc.

Physical places:

    -terrestrial physical locations: Geonyms include names given to natural geographical spaces, such as deserts, mountains, mountain chains, glaciers, plains, chasms, plateaus, valleys, volcanoes, canyons, etc.
    - aquatic physical sites: Hydronyms refer to water bodies, such as rivers, streams, ponds, marshes, lakes, seas, oceans, marine currents, canals, springs, etc.
    - astronomical physical places: includes planets, stars, galaxies, etc., and their parts.

Pathways: refer to streets, squares, roads, highways, etc.

Buildings : Named buildings (train station, museum, ..) as well as their extensions (stadium, campus, university, camping...) often refer to the physical location of an organisation.

Addresses:

    - physical addresses: an address is a point in space (e.g. a point in a street)
    - electronic addresses: Electronic coordinates: a telephone or fax number, url, E-Mail address, frequency radio, social network identifiers (Facebook, Twitter) or tools for internet communication (Skype), etc.


+HUMAN PRODUCTION (prod):

Media: Anything that is broadcast in the press, on radio or television: newspapers, magazines, broadcasts, sales catalogues, etc. (Die Zeit; Le Figaro, Le sept à huit, La ferme célébrités).

Doctrine: political, philosophical, religious, sectarian doctrines. (Der Sozialismus, Theravada Buddhismus; Zeugen Jehovas; Le socialism, le bouddhisme theravâda,le structuralism, la scientology).


+TIME (time):

An absolute date is a date whose position on the calendar can be deduced by the sole information present in the date (or temporal expression), without any context.

However, as soon as an explicit marker of relativity (for example nächster; prochain) is specified (Meeting am nächsten Dienstag; rendez-vous mardi prochain), we have a relative date and do not annotate it. Determiners (der, die, das; le, la, les, l' ) are only included in the entity if it has a function equivalent to a preposition (à, en).


+Non-annotated entities:

- Names of diseases (AIDS, Grippe A; SIDA, etc.)
- Psychological phenomena (Ödipuskomplex; syndrome de Stockholm, etc.)
- Scientific terms cannot be reduced to a product (DNA, ADN, etc.)
- Teaching programmes (Staps, DEUG, etc.)
- Special contracts (le contrat Coca-Cola/Danone, etc.) However: in le contrat Coca-Cola, the entity Coca-Cola is annotated (org.ent)
- Political and/or judicial matters (Watergate, Monica-gate; affaire Dickinson, etc.).
- Climatic phenomena (der Sturm Yinthya, le Mistral, etc.).
- Social phenomena (l’immigration arménienne , etc.).

-----

The output should be SAME sentence respecting casing and white spaces with the identified named entities delimited by <TYPE>named entity</TYPE>. 
Do not add or remove white spaces from the input sentence.
Do not add any note or explanation to the output.

Follow this example:

INPUT: <SENTENCE>Le résultat de la Fontenette est honorable pour les Vaudois qui doivent une fière chandelle à leur gardien Pasquini , en grande forme . </SENTENCE> 
OUTPUT: <SENTENCE>Le résultat de la <loc>Fontenette</loc> est honorable pour les Vaudois qui doivent une fière chandelle à leur <pers>gardien Pasquini</pers> , en grande forme . </SENTENCE>""",
"examples":[
    ["INPUT: <SENTENCE>Plus délicate , en revanche , est la situation de M . M . Blanc , député du Parti des paysans , artisans et indépendants ( Union démocratique du centre ) au Grand Conseil ; prévu en remplacement de M . Ravussin - qui ne se présente , lui , plus non plus , il est peu connu , sauf dans les milieux agricoles et son groupement politique ne jouit pas de positions très solides . </SENTENCE>",
     "OUTPUT: <SENTENCE>Plus délicate , en revanche , est la situation de <pers>M . M . Blanc , député du Parti des paysans , artisans et indépendants</pers> ( <org>Union démocratique du centre</org> ) au Grand Conseil ; prévu en remplacement de <pers>M . Ravussin</pers> - qui ne se présente , lui , plus non plus , il est peu connu , sauf dans les milieux agricoles et son groupement politique ne jouit pas de positions très solides . </SENTENCE>"],
    ["INPUT: <SENTENCE>Au dire des connaisseurs de la politique et de la mentalité vaudoise , elle n ' en a pas , contrairement au D ' Forel qui , en 1974 , avait presque enlevé son siège au socialiste Gavillet ; même la majorité des citoyennes seraient peu enclines à élire comme première femme une popiste et comme premier popiste une femme fût - elle très intelligente et « dans le vent » comme M Ménétrey .</SENTENCE>",
     "OUTPUT: <SENTENCE>Au dire des connaisseurs de la politique et de la mentalité vaudoise , elle n ' en a pas , contrairement au D ' <pers>Forel</pers> qui , <time>en 1974</time> , avait presque enlevé son siège au <pers>socialiste Gavillet</pers> ; même la majorité des citoyennes seraient peu enclines à élire comme première femme une popiste et comme premier popiste une femme fût - elle très intelligente et « dans le vent » comme <pers>M Ménétrey</pers> .</SENTENCE>"]

]}

SYSTEM_PROMPT_HIPE_NOGUIDELINES ={
    "prompt":"""You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types: person (PERSON), organisation (ORGANISATION), human production (HumanProd), time period (TIME), and location (LOC).

For example:

INPUT: "<SENTENCE>Le résultat de la Fontenette est honorable pour les Vaudois qui doivent une fière chandelle à leur gardien Pasquini , en grande forme . </SENTENCE>" 
OUTPUT: "<SENTENCE>Le résultat de la <loc>Fontenette</loc> est honorable pour les Vaudois qui doivent une fière chandelle à leur <pers>gardien Pasquini</pers> , en grande forme . </SENTENCE>"

INPUT: "<SENTENCE>Au dire des connaisseurs de la politique et de la mentalité vaudoise , elle n ' en a pas , contrairement au D ' Forel qui , en 1974 , avait presque enlevé son siège au socialiste Gavillet ; même la majorité des citoyennes seraient peu enclines à élire comme première femme une popiste et comme premier popiste une femme fût - elle très intelligente et « dans le vent » comme M Ménétrey .</SENTENCE>"
OUTPUT: "<SENTENCE>Au dire des connaisseurs de la politique et de la mentalité vaudoise , elle n ' en a pas , contrairement au D ' <pers>Forel</pers> qui , <time>en 1974</time> , avait presque enlevé son siège au <pers>socialiste Gavillet</pers> ; même la majorité des citoyennes seraient peu enclines à élire comme première femme une popiste et comme premier popiste une femme fût - elle très intelligente et « dans le vent » comme <pers>M Ménétrey</pers> .</SENTENCE>"

INPUT: "<SENTENCE>Plus délicate , en revanche , est la situation de M . M . Blanc , député du Parti des paysans , artisans et indépendants ( Union démocratique du centre ) au Grand Conseil ; prévu en remplacement de M . Ravussin - qui ne se présente , lui , plus non plus , il est peu connu , sauf dans les milieux agricoles et son groupement politique ne jouit pas de positions très solides . </SENTENCE>"
OUTPUT: "<SENTENCE>Plus délicate , en revanche , est la situation de <pers>M . M . Blanc , député du Parti des paysans , artisans et indépendants</pers> ( <org>Union démocratique du centre</org> ) au Grand Conseil ; prévu en remplacement de <pers>M . Ravussin</pers> - qui ne se présente , lui , plus non plus , il est peu connu , sauf dans les milieux agricoles et son groupement politique ne jouit pas de positions très solides . </SENTENCE>""",
    "examples": [["", ""]]}

SYSTEM_PROMPT_HIPE_NOGUIDELINES_ROLE = {
    "prompt": """You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types: PERSON (pers), ORGANISATION (org), HUMAN PRODUCTION (prod), TIME (TIME), and LOCATION (loc).

-----
The output should be SAME sentence respecting casing and white spaces with the identified named entities delimited by <TYPE>named entity</TYPE>. 
Do not add or remove white spaces from the input sentence.
Do not add any note or explanation to the output.

Follow this example:

INPUT: <SENTENCE>Le résultat de la Fontenette est honorable pour les Vaudois qui doivent une fière chandelle à leur gardien Pasquini , en grande forme . </SENTENCE> 
OUTPUT: <SENTENCE>Le résultat de la <loc>Fontenette</loc> est honorable pour les Vaudois qui doivent une fière chandelle à leur <pers>gardien Pasquini</pers> , en grande forme . </SENTENCE>""",
"examples":[
    ["INPUT: <SENTENCE>Plus délicate , en revanche , est la situation de M . M . Blanc , député du Parti des paysans , artisans et indépendants ( Union démocratique du centre ) au Grand Conseil ; prévu en remplacement de M . Ravussin - qui ne se présente , lui , plus non plus , il est peu connu , sauf dans les milieux agricoles et son groupement politique ne jouit pas de positions très solides . </SENTENCE>",
     "OUTPUT: <SENTENCE>Plus délicate , en revanche , est la situation de <pers>M . M . Blanc , député du Parti des paysans , artisans et indépendants</pers> ( <org>Union démocratique du centre</org> ) au Grand Conseil ; prévu en remplacement de <pers>M . Ravussin</pers> - qui ne se présente , lui , plus non plus , il est peu connu , sauf dans les milieux agricoles et son groupement politique ne jouit pas de positions très solides . </SENTENCE>"],
    ["INPUT: <SENTENCE>Au dire des connaisseurs de la politique et de la mentalité vaudoise , elle n ' en a pas , contrairement au D ' Forel qui , en 1974 , avait presque enlevé son siège au socialiste Gavillet ; même la majorité des citoyennes seraient peu enclines à élire comme première femme une popiste et comme premier popiste une femme fût - elle très intelligente et « dans le vent » comme M Ménétrey .</SENTENCE>",
     "OUTPUT: <SENTENCE>Au dire des connaisseurs de la politique et de la mentalité vaudoise , elle n ' en a pas , contrairement au D ' <pers>Forel</pers> qui , <time>en 1974</time> , avait presque enlevé son siège au <pers>socialiste Gavillet</pers> ; même la majorité des citoyennes seraient peu enclines à élire comme première femme une popiste et comme premier popiste une femme fût - elle très intelligente et « dans le vent » comme <pers>M Ménétrey</pers> .</SENTENCE>"]

]}

SYSTEM_PROMPT_ENP = """You are an excellent automatic named entity recognition (NER) system. I will provide you the sentence delimited by double quotes from which you need to identify and classify the named entities into the following types: PERSON, ORGANISATION, HUMAN PRODUCTION, LOCATION, TIME and EVENT. 

Named entities are linguistic units that must include a proper name, or a definite description having the status of a proper name. We do not specify further the definition of proper names, but instead rely on the linguistic intuition/awareness of annotators, who should always keep in mind our objective of extracting ‘historical’ information typically conveyed via referential entities.

Examples:

Phrases such as

    - 中國軍隊
    - 法租界
    - 皇帝
    - 國民政府
    - 湖南撫憲委員 
    - 司馬 
    - 方伯
    - 蘇淞太道憲
    - 國防次長 

are not annotated because they do not contain proper names.

Phrases such as

    - 新四軍
    - 法租界公董局
    - 慈禧王后
    - 汪偽政府

are annotated.


Next are the anotation guidelines for each named entity type.
-----
+ PERSON (pers):

Considered as PERSON:
	- A single person (王曉賴)
	- A named group of people 
	- A single person who is the author of an article 


+ ORGANISATION (org):

Considered as ORGANISATION:
    - Organization that plays a mainly administrative role (財政部) 
    - Professional or students’ associations, clubs, etc.
    - Business enterprises, private companies, banks, etc.
    - Educational institutions (school, college, university, academy, etc.) 
    - Other type of undefined organizations
    - Special type related to newspaper to spot press agencies (e.g., 申報館) 


+HUMAN PRODUCTION (Prod):

Considered as HUMAN PRODUCTION :
    - Newspapers, magazines, etc. (e.g., 申報, 東方雜誌)
    - Political, philosophical, religious, sectarian doctrines.
    - Creative works (book, theatrical play, movie, etc.)  
    
    
+ LOCATION (loc):  

Considered as LOCATION:
    - City or town district (e.g. 南市 in Shanghai) 
    - Village, town, city (上海, 上海市) 
    - Regions, provinces (江蘇) 
    - Countries
    - World regions, continent 
    - Mountains, plains, plateaus, caves, volcanoes, canyons 
    - Oceans, seas, rivers, streams, ponds, marshes 
    - Planets, stars, galaxies and their parts 
    - Roads, highways, streets, avenues, squares, etc. 
    - Buildings and other facilities 
    - Physical addresses (street name, street number, etc) 
    - Electronic contact information (not applicable in most cases) 
    - Other location types 


+TIME (time):

Considered as TIME:
    - Absolute datation: year (e.g., 1931, 一九三一年)
    - Absolute datation: month (e.g., 十一月) 
    - Absolute datation: day (e.g., 三日, 星期三) 
    - Relative datation: referent (imperial reigns or founding of the Republic) 
    - Relative datation: year 
    - Relative datation: month 
    - Relative datation: day 
    

+EVENT (event):

Considered as EVENT:
    - Event (meeting, conference, etc) 

-----

The output should be SAME sentence respecting casing and white spaces with the identified named entities delimited by <TYPE>named entity</TYPE>. 
Do not add or remove white spaces from the input sentence.
Do not any note or explanation to the output.

For example:

INPUT: "<SENTENCE>Le résultat de la Fontenette est honorable pour les Vaudois qui doivent une fière chandelle à leur gardien Pasquini , en grande forme . </SENTENCE>" 
OUTPUT: "<SENTENCE>Le résultat de la <loc>Fontenette</loc> est honorable pour les Vaudois qui doivent une fière chandelle à leur <pers>gardien Pasquini</pers> , en grande forme . </SENTENCE>"

INPUT: "<SENTENCE>Au dire des connaisseurs de la politique et de la mentalité vaudoise , elle n ' en a pas , contrairement au D ' Forel qui , en 1974 , avait presque enlevé son siège au socialiste Gavillet ; même la majorité des citoyennes seraient peu enclines à élire comme première femme une popiste et comme premier popiste une femme fût - elle très intelligente et « dans le vent » comme M Ménétrey .</SENTENCE>"
OUTPUT: "<SENTENCE>Au dire des connaisseurs de la politique et de la mentalité vaudoise , elle n ' en a pas , contrairement au D ' <pers>Forel</pers> qui , <time>en 1974</time> , avait presque enlevé son siège au <pers>socialiste Gavillet</pers> ; même la majorité des citoyennes seraient peu enclines à élire comme première femme une popiste et comme premier popiste une femme fût - elle très intelligente et « dans le vent » comme <pers>M Ménétrey</pers> .</SENTENCE>"

INPUT: "<SENTENCE>Plus délicate , en revanche , est la situation de M . M . Blanc , député du Parti des paysans , artisans et indépendants ( Union démocratique du centre ) au Grand Conseil ; prévu en remplacement de M . Ravussin - qui ne se présente , lui , plus non plus , il est peu connu , sauf dans les milieux agricoles et son groupement politique ne jouit pas de positions très solides . </SENTENCE>"
OUTPUT: "<SENTENCE>Plus délicate , en revanche , est la situation de <pers>M . M . Blanc , député du Parti des paysans , artisans et indépendants</pers> ( <org>Union démocratique du centre</org> ) au Grand Conseil ; prévu en remplacement de <pers>M . Ravussin</pers> - qui ne se présente , lui , plus non plus , il est peu connu , sauf dans les milieux agricoles et son groupement politique ne jouit pas de positions très solides . </SENTENCE>"
"""

SYSTEM_PROMPTS = {
    "ajmc_guidelines_norole": SYSTEM_PROMPT_AJMC,#ajmc
    "ajmc_guidelines_role": SYSTEM_PROMPT_AJMC_ROLE,#ajmc_role
    "ajmc_noguidelines_norole": SYSTEM_PROMPT_AJMC_NOGUIDELINES,#ajmc_no
    "ajmc_noguidelines_role": SYSTEM_PROMPT_AJMC_NOGUIDELINES_ROLE,#ajmc_no_role
    "newseye_guidelines_norole": SYSTEM_PROMPT_NEWSEYE,#newseye
    "newseye_guidelines_role": SYSTEM_PROMPT_NEWSEYE_ROLE,#newseye_role
    "newseye_noguidelines_norole": SYSTEM_PROMPT_NEWSEYE_NOGUIDELINES,#newseye_no
    "newseye_noguidelines_role": SYSTEM_PROMPT_NEWSEYE_NOGUIDELINES_ROLE,#newseye_no_role
    "hipe_guidelines_norole": SYSTEM_PROMPT_HIPE,#hipe
    "hipe_guidelines_role": SYSTEM_PROMPT_HIPE_ROLE,#hipe_role
    "hipe_noguidelines_norole": SYSTEM_PROMPT_HIPE_NOGUIDELINES,#hipe_no
    "hipe_noguidelines_role": SYSTEM_PROMPT_HIPE_NOGUIDELINES_ROLE,#hipe_no_role
    "enp": SYSTEM_PROMPT_ENP,
}
