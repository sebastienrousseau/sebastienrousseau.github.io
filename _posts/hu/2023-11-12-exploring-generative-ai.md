---
title: "A generatív MI 2023-ban: hogyan működik, és hol jelenik meg először"
tags: "generative AI, LLM, GPT-4, transformer, financial services, hallucination, RAG, AI governance, foundation model, fine-tuning, ISO 20022, DORA, post-quantum cryptography, quantum computing, AI"
subtitle: "Alkalmazott mesterséges intelligencia a bankszektorban és a pénzügyi szolgáltatásokban."
description: "Fedezze fel a generatív MI-t 2023-ban: hogyan működik, hol jelenik meg először a pénzügyi szolgáltatásokban, és milyen etikai és architekturális kérdéseket érdemes feltenni."
date: "Nov 12, 2023"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp"
banner_alt: "Absztrakt neurálishálózat-vizualizáció kék és lila tónusokban, amely az MI-feldolgozást ábrázolja"
keywords: "generatív MI, nagy nyelvi modell, transzformer architektúra, GPT-4, pénzügyi szolgáltatási MI, hallucináció, visszakereséssel bővített generálás, MI-irányítás, alapmodell, finomhangolás"
---

![Absztrakt neurálishálózat-vizualizáció kék és lila tónusokban, amely az MI-feldolgozást ábrázolja](https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp).class=\"img-fluid clearfix\"

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - **Az architektúra, amely mindent megváltoztatott.** A 2017-es transzformer tanulmány bevezette az önfigyelmet (self-attention): egy mechanizmust, amely a bemenet minden tokenpárja között relevanciasúlyokat számít, és az RNN-ek szekvenciális feldolgozását párhuzamosítható mátrixműveletekkel váltja fel. 2023 minden jelentős nyelvi modellje transzformervariáns ([Vaswani et al., 2017](https://arxiv.org/abs/1706.03762 "Attention Is All You Need")).
> - **A GPT-4 mint a 2023-as referenciapont.** A 2023 márciusában kiadott GPT-4 az amerikai ügyvédi (Bar) vizsgán a 90. percentilisbe, a GRE Verbal teszten a 99. percentilisbe került, és hosszú dokumentumokon átívelő, többlépéses érvelést mutatott. Ez határozta meg azt a képességi referenciapontot, amelyet a későbbi modellek elérni vagy meghaladni igyekeztek ([OpenAI, 2023](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report")).
> - **A nyílt súlyú modellek demokratizálták a hozzáférést.** A Meta Llama 2 modellje (2023 júliusa) és a Mistral AI Mistral 7B modellje (2023 szeptembere) megmutatta, hogy a GPT-3.5 osztályú képességekkel versenyképes modellek privát infrastruktúrán is futtathatók, ami megválaszolja a szabályozott iparágak adatlokalizációs követelményeit.
> - **Pénzügyi szolgáltatási pilotok 2023-ban.** 2023 végére a széles körű bevezetések közé tartozott a jogi szerződések felülvizsgálata (a JPMorgan DocLLM-kutatása), a szabályozási változások figyelése és a fejlesztői produktivitási eszközök. A Goldman Sachs 10 000 fejlesztőre kiterjedő belső MI-kódolási asszisztens használatáról számolt be.
> - **A hallucináció az éles üzem akadálya.** Az LLM-ek nem elhanyagolható arányban generálnak hihetően hangzó, de tényszerűen hibás kimeneteket. A szabályozott felhasználási esetekben, mint a hitelezési döntések, a megfelelőségi vélemények és az ügyfél-tájékoztatások, a hallucináció nem kozmetikai hiba: szabályozási és felelősségi kockázat, amely architekturális enyhítéseket, például visszakereséssel bővített generálást (RAG) igényel.

---

## Hogyan működik a transzformer architektúra

Minden jelentős, 2023-ban telepített nyelvi modell, a GPT-4, a Claude 2, a Llama 2, a Mistral és a Falcon, a 2017-es „Attention Is All You Need" tanulmányban bemutatott transzformer architektúrára épül. Az alapmechanizmus megértése megmagyarázza, hogy miért működnek ezek a modellek, és hol hibáznak.

**Tokenek és beágyazások.** A modell először szó alatti (sub-word) tokenekre bontja a bemeneti szöveget (jellemzően bájtpár-kódolással). Minden tokent egy nagy dimenziós vektorhoz (beágyazáshoz) rendel, amely a többi tokennel való szemantikai kapcsolatait kódolja, és amelyet az előtanítás során tanult meg.

**Önfigyelem.** Minden tokenhez a modell három vektort számít: egy lekérdezést (Query, azt, amit a token keres), egy kulcsot (Key, azt, amit a token kínál) és egy értéket (Value, azt, amivel a token hozzájárul). A figyelmi pontszámokat úgy számítja ki, hogy minden lekérdezés és az összes kulcs skaláris szorzatát veszi, softmaxot alkalmaz a súlyok előállításához, majd az értékeket ezekkel a pontszámokkal súlyozva összegzi. Ez azt jelenti, hogy minden token egyszerre figyel a kontextusablak minden más tokenjére: ez az a mechanizmus, amely a transzformereknek a nagy hatótávolságú függőségek kezelésének képességét adja.

**Többfejű figyelem.** Több figyelmi fej fut párhuzamosan, mindegyik különböző típusú kapcsolatokat (szintaktikai, szemantikai, pozicionális) tanul meg. Kimeneteiket összefűzik és lineárisan vetítik.

**Előrecsatolt rétegek.** A figyelem után minden pozíció két lineáris transzformáción halad át egy nemlineáris aktivációval. Ez a réteg tokenenként, egymástól függetlenül végez számítást, és a lokális jellemzőtranszformációkat ragadja meg.

**Méret.** A GPT-4 becslések szerint több mint egybillió paraméterrel rendelkezik (az OpenAI ezt nem erősítette meg). A Llama 2 70B 70 milliárdot használ. A Mistral 7B 7 milliárdot, a hatékonyság érdekében csoportosított lekérdezésű figyelemmel (grouped-query attention) és csúszóablakos figyelemmel (sliding window attention). A nagyobb modellek általában jobb zero-shot és few-shot érvelést mutatnak: ezek azok az emergens képességek, amelyek hasznossá teszik őket olyan feladatokra, amelyekre nem kifejezetten tanították be őket.

## A 2023-as modellek tájképe

2023 több jelentős modellkiadást hozott, mint bármely korábbi év:

**GPT-4 (OpenAI, 2023 márciusa).** Multimodális (szöveg + kép bemenet), a kontextusablak a későbbi GPT-4 Turbo variánsban akár 128 000 token, erős többlépéses érvelés. Referenciapontot állított a szakmai területek feladataihoz.

**Claude 2 (Anthropic, 2023 júliusa).** 100 000 tokenes kontextusablak (a leghosszabb a kiadáskor), erős teljesítmény hosszú dokumentumokat érintő feladatokban, például szerződések felülvizsgálatában és szabályozási elemzésben. Constitutional AI tanítás a káros kimenetek csökkentésére.

**Llama 2 (Meta, 2023 júliusa).** Nyílt súlyú kiadás 7B, 13B, 34B és 70B paraméteres variánsokban. Kereskedelmi használat engedélyezett. Lehetővé tette a helyben (on-premise) telepítést a szabályozott iparágak számára. Több száz finomhangolt variánst hívott életre (Code Llama, Vicuna, WizardLM).

**Mistral 7B (Mistral AI, 2023 szeptembere).** 7 milliárd paraméter, amely a legtöbb benchmarkon felülmúlja a Llama 2 13B-t. A csoportosított lekérdezésű figyelem és a csúszóablakos figyelem csökkenti a következtetési költséget. Az első jelentős európai élvonalbeli modell, ami a GDPR és az EU AI Act kontextusában releváns.

**Falcon 180B (TII, 2023 szeptembere).** 180 milliárd paraméteres nyílt súlyú modell, amelyet 3,5 billió tokennyi RefinedWeb adaton tanítottak. Bemutatta, hogy a nyílt súlyú modellek megközelíthetik a GPT-4 osztályú méretet.

## Hol jelent meg először a generatív MI a pénzügyi szolgáltatásokban

2023 végére a pénzügyi intézmények a belső kísérletezéstől a strukturált pilotprogramok felé mozdultak el több különálló felhasználási esetben:

**Fejlesztői produktivitás.** A kódgeneráló eszközök (GitHub Copilot, Amazon CodeWhisperer, belsőleg finomhangolt modellek) váltak a legszélesebb körben telepített kategóriává. A Goldman Sachs arról számolt be, hogy 10 000 fejlesztő fért hozzá MI-alapú kódolási segítséghez. A Morgan Stanley belsőleg vezette be a GPT-4-et, hogy segítse a pénzügyi tanácsadókat az információk visszakeresésében egy 100 000 dokumentumból álló tudásbázisból.

**Jogi és szabályozási dokumentumfeldolgozás.** A szerződési kikötések kinyerése, a szabályozási változások figyelése és a megfelelőség feltérképezése voltak a legnagyobb értékű pilotok. A JPMorgan DocLLM-en végzett kutatása bemutatta, hogy a dokumentumelrendezést figyelembe vevő nyelvi modellek felülmúlták az általános LLM-eket a pénzügyi dokumentumok megértését érintő feladatokban.

**Ügyfélszolgálati kiegészítés.** A bankok LLM-alapú asszisztenseket vezettek be az első vonalbeli ügyfélkérdésekhez, a szabályozott tanácsadás esetén emberi eszkalációval. Kulcsfontosságú megkötések: a modell nem adhat szabályozott tanácsot, nem hallucinálhat termékfeltételeket, és auditálhatónak kell lennie.

**KYC- és AML-szövegek generálása.** Az összetett tranzakciós minták és ügyfélprofilok összefoglalása elemzői felülvizsgálathoz, amely a korábban kézi jegyzetkészítést váltotta fel, hiteles felhasználási esetként jelent meg, alacsonyabb hallucinációs kockázattal, mert a modell a rendelkezésre bocsátott adatokat foglalja össze, nem pedig új állításokat generál.

## A kockázatok, amelyeket az éles üzem feltárt

A pénzügyi szolgáltatásokban a demótól az éles üzem felé való elmozdulás olyan kockázatok sorát tárta fel, amelyek architekturális válaszokat igényeltek:

**Hallucináció.** Az LLM-ek magabiztosan hangzó, hibás kimeneteket generálnak olyan arányban, amely a feladat típusától és a modelltől függően változik. Tényszerű felidézési feladatokon még a GPT-4 is olyan arányban hallucinál, amely elfogadhatatlan a megfelelőségi vélemények vagy a hitelezési tájékoztatások esetében. Az elsődleges enyhítés a visszakereséssel bővített generálás (RAG): a modell kimenetét visszakeresett, ellenőrizhető dokumentumokban kell megalapozni, ahelyett hogy kizárólag a parametrikus tudásra hagyatkoznánk.

**Prompt injekció.** A dokumentumokba vagy felhasználói üzenetekbe ágyazott ellenséges bemenetek átirányíthatják a modell viselkedését. A pénzügyi szolgáltatásokban, ahol az LLM-ek nem megbízható dokumentumokat (szerződéseket, e-maileket, ügyfélbeadványokat) dolgoznak fel, a prompt injekció éles üzemi biztonsági kockázat, nem elméleti.

**Adatszivárgás.** A bizalmas adatokon finomhangolt vagy azokkal promptolt modellek reprodukálhatják ezeket az adatokat a kimenetben: ez lényeges kockázat a személyes adatok (PII), a kereskedési pozíciók és az ügyféladatok szempontjából. Az architekturális kontrollok (privát telepítés, a kontextusban lévő adatok kezelése, kimenetszűrés) kötelezőek, nem opcionálisak.

**A modell eredete és auditálhatósága.** A szabályozók elvárják a pénzügyi intézményektől, hogy megmagyarázzák az automatizált döntéseket. Egy olyan LLM, amely auditálható érvelési nyomvonal nélkül állít elő hitelértékelést, nem felel meg a GDPR 22. cikkének megmagyarázhatósági követelményeinek, az EU AI Act magas kockázatú MI-re vonatkozó rendelkezéseinek, valamint a meglévő FCA modellkockázati útmutatásnak.

**Elavult tudás.** Az LLM-eknek van tanítási határidejük. Egy 2023 elejéig terjedő adatokon tanított modell nem tud az ezt követő szabályozási változásokról, kamatdöntésekről vagy piaci eseményekről: ez jelentős korlát a valós idejű megfelelőségi vagy piaci kommentár felhasználási esetekben RAG vagy valós idejű visszakeresés nélkül.

## Irányítási követelmények a bevezetés előtt

A 2023-ban működő pénzügyi szolgáltatási szakemberek nem várták meg a szabályozási bizonyosságot a bevezetés előtt, de a vezető intézmények az SR 11-7 és az SS3/18 útmutatásból adaptált modellkockázat-kezelési (MRM) keretrendszereket vezettek be:

**Modell-leltár és dokumentáció.** Az üzleti funkciókhoz telepített LLM-ekhez dokumentálni kell a tanítási adatok eredetét, a finomhangolás módszertanát, az ismert hibamódokat, valamint a területspecifikus validációs halmazokon nyújtott teljesítményt.

**Emberi ellenőrzési pontok (human-in-the-loop).** A szabályozott kimenetek (hitelezési döntések, megfelelőségi vélemények, ügyfél-tájékoztatások) esetében az emberi felülvizsgálat 2023-ban kötelező maradt. Az automatizálást a fogalmazásra és az összefoglalásra alkalmazták; a végső jóváhagyás emberi maradt.

**Beszállítói kockázat.** Egy harmadik féltől származó modell-API (OpenAI, Anthropic, Google) használata beszállítói koncentrációs kockázatot, adatlokalizációs kockázatot és modellváltozási kockázatot (a szolgáltatók csendben frissíthetik a modelleket) hoz magával. A vállalati megállapodások és a privát telepítések részben enyhítik ezeket.

**Szabályozói együttműködés.** Az FCA, a PRA, az ECB és a FINRA mind adtak ki dokumentumokat vagy tartottak beszédeket az MI-irányításról 2023-ban. A következetes üzenet: a meglévő modellkockázati keretrendszerek az MI-re is vonatkoznak, és a cégeknek proaktívan dokumentálniuk kell irányítási megközelítésüket a hivatalos útmutatás előtt.

## Gyakran ismételt kérdések

**Mi a különbség egy nagy nyelvi modell és egy alapmodell között?**

A nagy nyelvi modell (LLM) olyan modell, amelyet nagy mennyiségű szöveges adaton tanítottak a nyelv előrejelzésére és generálására. Az alapmodell tágabb fogalom minden olyan nagy, előtanított modellre, amely több utólagos feladatra adaptálható (finomhangolással vagy promptolással): ez magában foglalja az LLM-eket, de a képfeldolgozó modelleket, a kódmodelleket és a multimodális modelleket is. A GPT-4 egyszerre LLM és alapmodell. A DALL-E 3 alapmodell, de nem LLM. A gyakorlatban a fogalmakat gyakran felcserélhetően használják, amikor szöveggeneráló rendszerekre utalnak.

**Mi a visszakereséssel bővített generálás, és miért fontos a pénzügyi szolgáltatások számára?**

A RAG egy nyelvi modellt kombinál egy visszakereső rendszerrel: ahelyett, hogy kizárólag a modell parametrikus tudására (arra, amit a tanítás során tanult) hagyatkozna, a RAG a következtetés idején releváns dokumentumokat kér le, és azokat kontextusként adja át. Ez jelentősen csökkenti a hallucinációt a tényszerű feladatokon, mert a modell a rendelkezésre bocsátott szöveget szintetizálja, nem pedig a megtanult tényeket idézi fel. A pénzügyi szolgáltatások számára a RAG olyan felhasználási eseteket tesz lehetővé, mint a szabályozási változások figyelése (mindig az aktuális szabályokat kéri le) és a szerződések felülvizsgálata (a modellt a tényleges szerződési szövegben alapozza meg), amelyek egy tisztán generatív megközelítéssel túlságosan hallucinációra hajlamosak lennének.

**Hogyan kezeljék a pénzügyi intézmények az EU AI Actet a 2023-as generatív MI-bevezetésekkel kapcsolatban?**

Az EU AI Act 2023-ban még jogalkotási folyamatban volt (az Európai Parlament 2024 márciusában fogadta el, 2024 augusztusában lépett hatályba). Az EU-s működéssel vagy EU-s ügyfelekkel rendelkező intézmények azonban már értékelték a folyamataikat. A hitelpontozásban, a foglalkoztatási döntésekben és a kritikus infrastruktúrában alkalmazott magas kockázatú MI-rendszerek megfelelőségértékelést, emberi felügyeleti mechanizmusokat és auditnaplózást igényelnek. Az általános célú MI (GPAI) modellek, amelyek magukban foglalják az olyan alapmodelleket, mint a GPT-4, saját követelményszinttel rendelkeznek az átláthatóság és a rendszerszintű kockázat terén. Azok a cégek, amelyek 2023-ban megkezdték a dokumentációs és irányítási munkát, jobb helyzetben voltak a bevezetési határidőkre nézve.

**Mi a gyakorlati különbség a finomhangolás és a promptmérnökség között a vállalati LLM-bevezetéseknél?**

A finomhangolás módosítja a modell súlyait azzal, hogy területspecifikus adatokon folytatja a tanítást: új tudást és viselkedési mintákat tanít a modellnek. Címkézett tanítási adatokat, számítási keretet és folyamatos karbantartást igényel, ahogy az alapmodelleket frissítik. A promptmérnökség (beleértve a few-shot példákat és a rendszerpromptokat) a következtetés idején alakítja a viselkedést a súlyok megváltoztatása nélkül: gyorsabban megvalósítható és frissíthető, de korlátozza az, amit az alapmodell már tud. A legtöbb 2023-as pénzügyi szolgáltatási bevezetésnél a RAG és a promptmérnökség volt az előnyben részesített kiindulópont; a finomhangolást azokra az esetekre tartották fenn, amikor a modellnek meg kellett tanulnia egy védett terminológiát, vagy szigorú kimeneti formátumokat kellett átvennie.

## Hivatkozások

- Vaswani, A., et al., (2017). [Attention Is All You Need ⧉](https://arxiv.org/abs/1706.03762 "Attention Is All You Need").
- OpenAI, (2023). [GPT-4 Technical Report ⧉](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report").
- Touvron, H., et al., Meta AI, (2023). [Llama 2: Open Foundation and Fine-Tuned Chat Models ⧉](https://arxiv.org/abs/2307.09288 "Llama 2").
- Jiang, A., et al., Mistral AI, (2023). [Mistral 7B ⧉](https://arxiv.org/abs/2310.06825 "Mistral 7B").

