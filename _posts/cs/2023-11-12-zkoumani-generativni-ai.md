---
title: "Generativní AI v roce 2023: jak funguje a kde nachází uplatnění"
subtitle: "Aplikovaná umělá inteligence v bankovnictví a finančních službách."
description: "Generativní AI v roce 2023: jak funguje, kde se ve finančních službách uplatňuje jako první a jaké etické a architektonické otázky je třeba klást."
date: "November 12, 2023"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp"
banner_alt: "Abstraktní vizualizace neuronové sítě v modrých a fialových tónech znázorňující zpracování AI"
keywords: "generativní AI, velký jazykový model, architektura transformer, GPT-4, AI ve finančních službách, halucinace, generování rozšířené o vyhledávání, governance AI, základový model, doladění"
---


![Abstraktní vizualizace neuronové sítě v modrých a fialových tónech znázorňující zpracování AI](https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp).class=\"img-fluid clearfix\"

> **Shrnutí pro vedení / Klíčové body**
>
> - **Architektura, která vše změnila.** Práce o architektuře transformer z roku 2017 zavedla mechanismus self-attention: ten počítá váhy relevance mezi každou dvojicí tokenů na vstupu a nahrazuje sekvenční zpracování sítí RNN paralelizovatelnými maticovými operacemi. Každý významný jazykový model z roku 2023 je variantou architektury transformer ([Vaswani et al., 2017](https://arxiv.org/abs/1706.03762 "Attention Is All You Need")).
> - **GPT-4 jako měřítko roku 2023.** GPT-4, vydaný v březnu 2023, dosáhl na advokátní zkoušce v USA 90. percentilu, na testu GRE Verbal 99. percentilu a prokázal vícekrokové uvažování napříč dlouhými dokumenty. Stanovil měřítko schopností, na které následující modely usilovaly dosáhnout nebo je překonat ([OpenAI, 2023](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report")).
> - **Modely s otevřenými váhami zpřístupnily technologii.** Llama 2 od Meta (červenec 2023) a Mistral 7B od Mistral AI (září 2023) ukázaly, že modely konkurenceschopné se schopnostmi třídy GPT-3.5 mohou běžet na privátní infrastruktuře, což řeší požadavky regulovaných odvětví na lokalizaci dat.
> - **Pilotní projekty ve finančních službách v roce 2023.** Mezi rozšířená nasazení do konce roku 2023 patřila revize právních smluv (výzkum DocLLM od JPMorgan), monitorování regulatorních změn a nástroje pro produktivitu vývojářů. Goldman Sachs uvedl interní využití asistentů AI pro psaní kódu u 10 000 vývojářů.
> - **Halucinace jsou překážkou pro nasazení do produkce.** LLM generují věrohodně znějící, ale fakticky nesprávné výstupy v netriviální míře. V regulovaných případech použití, jako jsou úvěrová rozhodnutí, stanoviska k souladu s předpisy a informování zákazníků, není halucinace kosmetickou vadou; jde o regulatorní a odpovědnostní riziko, které vyžaduje architektonická zmírnění, například generování rozšířené o vyhledávání (RAG).

---

## Jak funguje architektura transformer

Každý významný jazykový model nasazený v roce 2023, ať jde o GPT-4, Claude 2, Llama 2, Mistral či Falcon, je postaven na architektuře transformer představené v práci z roku 2017 nazvané „Attention Is All You Need". Pochopení základního mechanismu vysvětluje jak to, proč tyto modely fungují, tak to, kde selhávají.

**Tokeny a embeddingy.** Model začíná rozdělením vstupního textu na dílčí slovní tokeny (obvykle pomocí byte-pair encoding). Každý token je namapován na vysokorozměrný vektor (embedding), který kóduje jeho sémantické vztahy k ostatním tokenům a je naučen během předtrénování.

**Self-attention.** Pro každý token model počítá tři vektory: dotaz (Query, co tento token hledá), klíč (Key, co tento token nabízí) a hodnotu (Value, čím tento token přispívá). Skóre pozornosti se počítá jako skalární součin každého dotazu se všemi klíči, na který se aplikuje softmax pro získání vah, a hodnoty se sečtou vážené těmito skóre. To znamená, že každý token současně věnuje pozornost každému dalšímu tokenu v kontextovém okně, což je mechanismus, který transformerům dává schopnost zpracovávat závislosti na velkou vzdálenost.

**Vícehlavá pozornost (multi-head attention).** Několik hlav pozornosti běží paralelně, přičemž každá se učí jiné typy vztahů (syntaktické, sémantické, poziční). Jejich výstupy se zřetězí a lineárně promítnou.

**Dopředné vrstvy (feed-forward).** Po pozornosti prochází každá pozice dvěma lineárními transformacemi s nelineární aktivací. Tato vrstva provádí výpočet pro každý token nezávisle a zachycuje lokální transformace příznaků.

**Škála.** GPT-4 se odhaduje na více než jeden bilion parametrů (společnost OpenAI to nepotvrdila). Llama 2 70B používá 70 miliard. Mistral 7B používá 7 miliard, s grouped-query attention a sliding window attention pro vyšší efektivitu. Větší modely obecně vykazují lepší uvažování v režimu zero-shot a few-shot, což jsou emergentní schopnosti, které je činí užitečnými pro úlohy, na které nebyly explicitně trénovány.

## Přehled modelů roku 2023

Rok 2023 přinesl více významných vydání modelů než kterýkoli předchozí rok:

**GPT-4 (OpenAI, březen 2023).** Multimodální (vstup text i obraz), kontextové okno až 128 000 tokenů v pozdější variantě GPT-4 Turbo, silné vícekrokové uvažování. Stanovil měřítko pro úlohy z profesních oblastí.

**Claude 2 (Anthropic, červenec 2023).** Kontextové okno 100 000 tokenů (v době uvedení nejdelší), silný výkon u úloh s dlouhými dokumenty, jako je revize smluv a regulatorní analýza. Trénink metodou Constitutional AI pro omezení škodlivých výstupů.

**Llama 2 (Meta, červenec 2023).** Vydání s otevřenými váhami ve variantách 7B, 13B, 34B a 70B parametrů. Komerční použití povoleno. Umožnilo nasazení on-premise pro regulovaná odvětví. Dalo vzniknout stovkám doladěných variant (Code Llama, Vicuna, WizardLM).

**Mistral 7B (Mistral AI, září 2023).** 7 miliard parametrů překonávajících Llama 2 13B na většině benchmarků. Grouped-query attention a sliding window attention snižují náklady na inferenci. První významný evropský špičkový model, relevantní v kontextu GDPR a EU AI Act.

**Falcon 180B (TII, září 2023).** Model s otevřenými váhami se 180 miliardami parametrů, trénovaný na 3,5 bilionu tokenů dat RefinedWeb. Prokázal, že modely s otevřenými váhami se mohou přiblížit škále třídy GPT-4.

## Kde se generativní AI ve finančních službách uplatnila jako první

Do konce roku 2023 finanční instituce přešly od interního experimentování ke strukturovaným pilotním programům v několika odlišných případech použití:

**Produktivita vývojářů.** Nástroje pro generování kódu (GitHub Copilot, Amazon CodeWhisperer, interně doladěné modely) se staly nejšíře nasazenou kategorií. Goldman Sachs uvedl, že 10 000 vývojářů mělo přístup k asistenci AI pro psaní kódu. Morgan Stanley nasadil interně GPT-4, aby finančním poradcům pomohl vyhledávat informace ve znalostní bázi o 100 000 dokumentech.

**Zpracování právních a regulatorních dokumentů.** Nejhodnotnějšími piloty byly extrakce smluvních klauzulí, monitorování regulatorních změn a mapování souladu s předpisy. Výzkum DocLLM od JPMorgan prokázal, že jazykové modely zohledňující rozvržení dokumentu překonávají obecné LLM v úlohách porozumění finančním dokumentům.

**Rozšíření zákaznického servisu.** Banky nasadily asistenty poháněné LLM pro dotazy zákazníků na první úrovni, s eskalací na člověka u regulovaného poradenství. Klíčová omezení: model nesmí poskytovat regulované poradenství, nesmí halucinovat podmínky produktu a musí být auditovatelný.

**Generování textů pro KYC a AML.** Shrnování složitých transakčních vzorců a profilů zákazníků pro revizi analytikem, které nahrazuje dosud ruční sepisování, se ukázalo jako věrohodný případ použití s nižším rizikem halucinací, protože model shrnuje poskytnutá data namísto generování nových tvrzení.

## Rizika, která odhalila produkce

Přechod od dema k produkci ve finančních službách odhalil soubor rizik, která vyžadovala architektonické odpovědi:

**Halucinace.** LLM generují sebejistě znějící nesprávné výstupy v míře, která se liší podle typu úlohy a modelu. U úloh faktického vybavování halucinuje i GPT-4 v míře, která je pro stanoviska k souladu s předpisy nebo úvěrové informování nepřijatelná. Hlavním zmírněním je generování rozšířené o vyhledávání (RAG): výstup modelu se ukotví v nalezených, ověřitelných dokumentech namísto spoléhání se pouze na parametrické znalosti.

**Prompt injection.** Nepřátelské vstupy vložené do dokumentů nebo uživatelských zpráv mohou přesměrovat chování modelu. Ve finančních službách, kde LLM zpracovávají nedůvěryhodné dokumenty (smlouvy, e-maily, podání zákazníků), je prompt injection produkčním bezpečnostním rizikem, nikoli teoretickým.

**Únik dat.** Modely doladěné nebo promptované na důvěrných datech mohou tato data reprodukovat ve výstupu, což je významné riziko pro PII, obchodní pozice a informace o klientech. Architektonické kontroly (privátní nasazení, správa dat v kontextu, filtrování výstupů) jsou nezbytné, nikoli volitelné.

**Původ modelu a auditovatelnost.** Regulátoři očekávají, že finanční instituce vysvětlí automatizovaná rozhodnutí. LLM, který vytvoří úvěrové posouzení bez auditovatelné stopy uvažování, nesplňuje požadavky na vysvětlitelnost podle článku 22 GDPR, ustanovení EU AI Act o vysoce rizikové AI a stávající pokyny FCA k modelovému riziku.

**Zastaralé znalosti.** LLM mají hranici trénovacích dat. Model trénovaný na datech do počátku roku 2023 neví o regulatorních změnách, rozhodnutích o sazbách ani tržních událostech po tomto datu, což je významné omezení pro použití v reálném čase, jako je průběžný soulad s předpisy nebo komentář k trhu, bez RAG nebo vyhledávání v reálném čase.

## Požadavky na governance před nasazením

Odborníci ve finančních službách působící v roce 2023 s nasazením nečekali na regulatorní jistotu, přední instituce však přijaly rámce řízení modelového rizika (MRM) upravené podle pokynů SR 11-7 a SS3/18:

**Evidence a dokumentace modelů.** LLM nasazené pro obchodní funkce vyžadují dokumentaci původu trénovacích dat, metodiky doladění, známých režimů selhání a výkonu na doménově specifických validačních sadách.

**Kontrolní body s člověkem ve smyčce.** U regulovaných výstupů (úvěrová rozhodnutí, stanoviska k souladu s předpisy, informování zákazníků) zůstala v roce 2023 revize člověkem povinná. Automatizace se uplatnila u konceptů a shrnutí; konečné schválení zůstalo na člověku.

**Riziko dodavatele.** Použití API modelu třetí strany (OpenAI, Anthropic, Google) přináší riziko koncentrace dodavatelů, riziko lokalizace dat a riziko změny modelu (poskytovatelé mohou modely aktualizovat bez upozornění). Podnikové smlouvy a privátní nasazení tato rizika částečně zmírňují.

**Zapojení regulátorů.** FCA, PRA, ECB i FINRA v roce 2023 vydaly dokumenty nebo projevy o governance AI. Konzistentní sdělení: na AI se vztahují stávající rámce modelového rizika a firmy by měly být proaktivní v dokumentaci svého přístupu ke governance ještě před formálními pokyny.

## Často kladené otázky

**Jaký je rozdíl mezi velkým jazykovým modelem a základovým modelem?**

Velký jazykový model (LLM) je model trénovaný na textových datech ve velkém měřítku k predikci a generování jazyka. Základový model (foundation model) je širší pojem pro jakýkoli velký předtrénovaný model, který lze přizpůsobit (doladěním nebo promptováním) pro více navazujících úloh, včetně LLM, ale také modelů pro obraz, kód a multimodálních modelů. GPT-4 je zároveň LLM i základový model. DALL-E 3 je základový model, ale nikoli LLM. V praxi se tyto pojmy často používají zaměnitelně, když se hovoří o systémech pro generování textu.

**Co je generování rozšířené o vyhledávání a proč je důležité pro finanční služby?**

RAG kombinuje jazykový model s vyhledávacím systémem: namísto spoléhání se výhradně na parametrické znalosti modelu (to, co se naučil během tréninku) RAG načte relevantní dokumenty v době inference a poskytne je jako kontext. To výrazně snižuje halucinace u faktických úloh, protože model syntetizuje poskytnutý text namísto vybavování naučených faktů. Pro finanční služby RAG umožňuje případy použití, jako je monitorování regulatorních změn (vždy načte aktuální pravidla) a revize smluv (ukotví model ve skutečném textu smlouvy), které by byly u čistě generativního přístupu příliš náchylné k halucinacím.

**Jak by měly finanční instituce přistupovat k EU AI Act ve vztahu k nasazení generativní AI v roce 2023?**

EU AI Act byl v roce 2023 stále v legislativním procesu (schválen Evropským parlamentem v březnu 2024, v platnost vstoupil v srpnu 2024). Instituce s evropskými operacemi nebo evropskými zákazníky však již posuzovaly své pipeline. Vysoce rizikové systémy AI v úvěrovém skóringu, rozhodnutích o zaměstnávání a kritické infrastruktuře vyžadují posouzení shody, mechanismy lidského dohledu a auditní protokolování. Modely AI pro obecné účely (GPAI), mezi které patří základové modely jako GPT-4, mají vlastní úroveň požadavků na transparentnost a systémové riziko. Firmy, které zahájily práci na dokumentaci a governance v roce 2023, byly na termíny implementace lépe připraveny.

**Jaký je praktický rozdíl mezi doladěním a prompt engineeringem u podnikových nasazení LLM?**

Doladění (fine-tuning) upravuje váhy modelu pokračováním tréninku na doménově specifických datech, učí model nové znalosti a vzorce chování. Vyžaduje označená trénovací data, výpočetní rozpočet a průběžnou údržbu s aktualizací základních modelů. Prompt engineering (včetně few-shot příkladů a systémových promptů) formuje chování v době inference bez změny vah, je rychlejší na implementaci a aktualizaci, ale je omezen tím, co základní model již zná. Pro většinu nasazení ve finančních službách v roce 2023 byla preferovaným výchozím bodem kombinace RAG a prompt engineeringu; doladění bylo vyhrazeno pro případy, kdy se model potřeboval naučit proprietární terminologii nebo přijmout striktní formáty výstupu.

## Reference

- Vaswani, A., et al., (2017). [Attention Is All You Need ⧉](https://arxiv.org/abs/1706.03762 "Attention Is All You Need").
- OpenAI, (2023). [GPT-4 Technical Report ⧉](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report").
- Touvron, H., et al., Meta AI, (2023). [Llama 2: Open Foundation and Fine-Tuned Chat Models ⧉](https://arxiv.org/abs/2307.09288 "Llama 2").
- Jiang, A., et al., Mistral AI, (2023). [Mistral 7B ⧉](https://arxiv.org/abs/2310.06825 "Mistral 7B").
