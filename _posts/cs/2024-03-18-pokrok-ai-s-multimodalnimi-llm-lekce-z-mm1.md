---
title: "Pokrok v AI s multimodálními LLM: poznatky z MM1"
subtitle: "Budoucnost AI: jak studie MM1 od Apple mění multimodální učení"
description: "Studie MM1 od Apple o multimodálních velkých jazykových modelech (MLLM). Architektura, strategie předtrénování a možnosti AI."
date: "March 18, 2024"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/mm1-visual.webp"
banner_alt: "Banner pro MM1 od Apple"
keywords: "multimodální LLM, studie MM1, pokrok v AI, strategie předtrénování, rozpoznávání obrazu, zpracování přirozeného jazyka, aplikace AI, budoucnost AI, multimodální učení, výzkum AI"
---

## Úvod

Propojení zpracování přirozeného jazyka a rozpoznávání obrazu vedlo k vývoji multimodálních velkých jazykových modelů (MLLM). Ve svém článku Apple představuje MM1, soubor multimodálních modelů AI, které kombinují porozumění obrazu a jazyku. Prostřednictvím rozsáhlých experimentů autoři zkoumali faktory, které přispívají k výkonu těchto modelů, a prověřili různá architektonická rozhodnutí a kombinace předtrénovacích dat. Článek MM1 poskytuje zásadní informace o tom, jak jsou modely MLLM strukturovány a trénovány. Popisuje přístup studie a její klíčová zjištění a ukazuje jejich možný dopad na budoucnost AI.

![divider][divider].class=\"m-10 w-100\"

## Nástup multimodální AI

Oblast AI zaznamenala v posledních letech výrazný pokrok, zejména ve zpracování přirozeného jazyka (NLP) a v počítačovém vidění. Velké jazykové modely (LLM) změnily způsob, jakým stroje rozumějí lidskému jazyku a jak jej generují, a umožnily jim provádět složité úlohy, jako je překlad jazyka, shrnutí textu i tvůrčí psaní. Podobně konvoluční neuronové sítě (CNN) zásadně změnily rozpoznávání obrazu a umožnily strojům vnímat a interpretovat vizuální data s dosud nevídanou přesností.

Modely MLLM představují další krok ve vývoji AI. Spojují silné stránky NLP i počítačového vidění a vytvářejí modely, které dokážou plynule zpracovávat a generovat informace napříč textem a obrazem. Toto propojení modalit otevírá řadu možností, od zajímavějších virtuálních asistentů po inteligentní nástroje pro tvorbu obsahu, které dokážou vytvářet poutavé multimediální výstupy.

![divider][divider].class=\"m-10 w-100\"

## Studie MM1: milník ve výzkumu multimodální AI

Studie [**MM1: Methods Analysis & Insights from Multimodal LLM Pre-training ⧉**][00] představuje klíčový okamžik ve vývoji modelů MLLM. Tým uznávaných výzkumníků si v ní kladl za cíl odhalit hlavní komponenty a strategie nezbytné pro účinné předtrénování MLLM, přičemž se zaměřil na model MM1 jako referenční bod pro multimodální AI.

### Metodika a cíle

Publikace MM1 využila důsledný experimentální přístup ke zkoumání složitostí multimodální architektury a strategií předtrénování. Výzkumníci prozkoumali různé aspekty modelu, včetně kodéru obrazu, vizuálně-jazykového konektoru a výběru rozmanitých předtrénovacích datových sad. Systematickou analýzou těchto komponent studie usilovala o určení kritických faktorů, které přispívají k vyššímu výkonu MLLM.

Jedním z hlavních cílů výzkumu bylo určit optimální složení předtrénovacích dat pro dosažení lepších schopností učení few-shot. Učení few-shot označuje schopnost modelu přizpůsobit se a učit se z omezeného počtu příkladů, což je zásadní vlastnost systémů AI, které musí být pružné a efektivní v reálném nasazení.

![divider][divider].class=\"m-10 w-100\"

## Klíčová zjištění a poznatky

Studie MM1 přinesla několik významných poznatků, které utvářely naše chápání modelů MLLM a jejich možností. Jedním z nejdůležitějších zjištění byl význam pečlivě sestaveného složení předtrénovacích dat. Výzkumníci zjistili, že kombinace dat obraz-popisek, prokládaných dat obraz-text a dat pouze s textem byla nezbytná pro dosažení optimálního výkonu při učení few-shot. Toto zjištění zdůrazňuje potřebu rozmanitých a komplexních předtrénovacích datových sad, které dokážou zachytit nuance multimodální komunikace.

Dalším pozoruhodným aspektem studie MM1 je zahrnutí jak hustých modelů s až 30 miliardami parametrů, tak variant mixture-of-experts (MoE), což dokládá škálovatelnost a flexibilitu architektury. Studie ukázala, že rozlišení obrazu má na výkon modelu nejvýznamnější vliv, ještě větší než velikost modelu, což zdůrazňuje význam kvalitního vizuálního vstupu v multimodálním učení.

Volba architektury kodéru obrazu, například ResNet nebo ViT, výrazně ovlivnila schopnost modelu získávat smysluplné rysy z vizuálních dat a propojovat je s textovými informacemi. Rozlišení vstupních obrazů navíc hrálo zásadní roli při určování kvality a granularity vizuálních rysů zachycených modelem.

Studie MM1 rovněž objasňuje význam vizuálně-jazykového konektoru pro plynulou interakci mezi vizuální a textovou modalitou. Výzkumníci vyzkoušeli různé přístupy ke sloučení informací z kodéru obrazu a jazykového modelu a identifikovali mechanismy křížové pozornosti (cross-attention) a vícehlavovou pozornost (multi-head attention) jako účinné strategie pro dosažení bohatých a kontextově relevantních interakcí.

![divider][divider].class=\"m-10 w-100\"

## Architektura modelu MM1 a proces multimodálního učení

![MM1 Model Architecture][architecture].class=\"m-10 w-100\"

Diagram znázorňuje architekturu a proces učení modelu MM1. Předtrénovací data se skládají z obrazového a textového vstupu; obrazový vstup zpracovává Image Encoder a textový vstup přímo vstupuje do předtrénovaného transformeru LLM. Image Encoder získává vizuální rysy ze vstupních obrazů, které jsou následně předány do VL Connectoru (Vision-Language Connector). VL Connector propojuje vizuální rysy s textovými informacemi z předtrénovaného transformeru LLM. Toto multimodální propojení umožňuje modelu generovat výstup titulkování VQA (Visual Question Answering) prostřednictvím řízeného doladění (supervised fine-tuning).

Složení předtrénovacích dat zahrnuje 45 % prokládaných dat, 45 % popisků a 10 % dat pouze s textem, což zdůrazňuje význam rozmanitých typů dat při trénování modelu MM1.

![divider][divider].class=\"m-10 w-100\"

## MM1: referenční bod pro multimodální AI

Model MM1, vyvinutý v rámci studie, slouží jako referenční bod pro multimodální AI a ukazuje možnosti modelů MLLM v různých aplikacích. Díky pečlivě navržené architektuře a režimu předtrénování dosahuje MM1 vynikajícího výkonu v řadě úloh, od vizuálního odpovídání na otázky (visual question answering) po titulkování obrazů.

Jednou z klíčových předností MM1 je jeho schopnost generovat souvislý a kontextově relevantní text na základě vizuálního vstupu. Například při zobrazení rušné městské ulice dokáže MM1 vytvořit podrobný a přesný popis, který zachytí podstatu scény a zdůrazní klíčové prvky, jako je architektura, lidé a jejich činnosti.

### Důsledky a budoucí směřování

Zjištění studie MM1 mají dalekosáhlé důsledky pro budoucnost AI a multimodálního učení. Poznatky získané tímto výzkumem poskytují pevný základ pro vývoj pokročilejších a schopnějších architektur MLLM a otevírají cestu systémům AI, které dokážou plynule procházet a interpretovat multimodální svět, v němž žijeme.

> Pojďme vymýšlet zítřek, místo abychom se trápili tím, co se stalo včera. - **Steve Jobs**

Jednou z podnětných oblastí budoucího výzkumu je hledání nových přístupů k propojení vizuálních a textových informací v modelech MLLM. Studie MM1 zdůraznila účinnost mechanismů křížové pozornosti a vícehlavové pozornosti, prostor pro další inovace v této oblasti však zůstává značný. Výzkumníci mohou zkoumat nové architektury, které se dokážou dynamicky přizpůsobit obsahu a struktuře vstupních dat a umožnit tak ještě pružnější a kontextově vnímavější multimodální interakce.

Dalším slibným směrem je nasazení modelů MLLM v reálných scénářích, jako jsou inteligentní virtuální asistenti, vzdělávací nástroje a tvorba kreativního obsahu. Schopnost modelů MLLM zpracovávat a generovat informace napříč textem a obrazem otevírá širokou škálu možností pro zlepšení komunikace mezi člověkem a strojem a pro tvorbu poutavějších a pohlcujících zážitků.

> Dalším velkým krokem v AI budou stroje, které mnohem lépe rozumějí světu kolem sebe, protože dokážou chápat data, jež dosud neviděly, a uvažovat o nich. - **Yann LeCun**

![divider][divider].class=\"m-10 w-100\"

## Závěr

Studie MM1 představuje významný milník ve vývoji multimodálních velkých jazykových modelů a nabízí cenné poznatky o architektuře, strategiích předtrénování a možnostech těchto výkonných systémů AI. Pečlivou analýzou klíčových komponent a metodik nezbytných pro účinné předtrénování MLLM položila studie základ pro budoucí inovace v multimodální AI.

Poznatky ze studie MM1 nepochybně ovlivní vývoj propracovanějších a schopnějších modelů MLLM. Tyto modely mohou zásadně změnit způsob, jakým komunikujeme se stroji, a umožnit přirozenější, intuitivnější a kontextově vnímavější komunikaci napříč textovou a vizuální modalitou.

Samotný model MM1 dokládá značné možnosti modelů MLLM, neboť dosahuje vynikajícího výkonu v řadě úloh a stanovuje nový referenční bod pro multimodální AI. Jak budou výzkumníci dále stavět na poznatcích z této studie, můžeme očekávat budoucnost, v níž systémy AI dokážou plynule procházet a interpretovat složitý multimodální svět, který obýváme, a přiblíží nás tak vizi skutečně inteligentních strojů.

Chcete-li se o studii MM1 dozvědět více a prozkoumat oblast multimodálních velkých jazykových modelů, doporučuji přečíst si původní výzkumný článek: [**MM1: Methods Analysis & Insights from Multimodal LLM Pre-training ⧉**][00]

[00]: https://arxiv.org/abs/2403.09611 "MM1: Methods Analysis & Insights from Multimodal LLM Pre-training"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
[architecture]: https://cloudcdn.pro/stocks/diagrams/mm1_model_architecture.svg "MM1 Model Architecture"
