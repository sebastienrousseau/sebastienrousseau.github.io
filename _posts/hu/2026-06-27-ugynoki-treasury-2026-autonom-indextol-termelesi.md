---
title: "Ügynöki treasury 2026: az autonóm treasury indextől a termelési szintű társpilótákig"
tags: "agentic AI, treasury co-pilots, autonomous treasury, cash forecasting, liquidity, agentic banking, governance, SR 11-7, DORA, EU AI Act, CIB, ISO 20022, MCP"
subtitle: "Az autonóm treasury indextől a termelési szintű társpilótákig: hogyan operacionalizálják a CIB treasuryk az ügynöki MI-t az ISO 20022 adatokra, MCP eszközhívásokra és SR 11-7 által formált irányításra építve 2026-ban."
description: "Az ügynöki treasury társpilóták 2026-ban a pilotoktól a termelésig jutnak: ISO 20022 adatok és eszközhívások, körülöttük SR 11-7, DORA és EU AI Act kontrollokkal."
date: "June 27, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/sebastien-rousseau-20260617-ai-7.webp"
banner_alt: "Kereskedőtermi fény egy modern bankcsarnok felett, amely az ügynöki treasury társpilótákat jelképezi, ahogy a napközbeni likviditást a szabályzati sávokon belül egyensúlyozzák, SR 11-7 és EU AI Act kontrollok mellett"
keywords: "ügynöki MI, treasury társpilóták, autonóm treasury, készpénz-előrejelzés, likviditáskezelés, ügynöki banki működés, irányítás, SR 11-7, DORA, EU AI Act, CIB, ISO 20022, pacs.008, RTGS, SWIFT, MCP, modellkockázat-kezelés, MRM"
---

## Ügynöki treasury 2026: az autonóm treasury indextől a termelési szintű társpilótákig

Egy treasury társpilóta 2026-ban nem egy készpénzpozíció-képernyőre ráaggatott chatbot. Olyan körülhatárolt ügynök, amely [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) kivonatokat olvas, napközbeni likviditást vetít előre, és javaslatot tesz, vagy szoros szabályzati kereten belül végre is hajt sweepeket, FX-fedezeteket és napközbeni repóügyleteket. A minta minden Corporate and Investment Banking (CIB) treasuryben ugyanaz: az ügynökök folyamatosan egyensúlyozzák a likviditást a szabályzati sávokon belül, és csak akkor eszkalálnak emberhez, ha egy sáv áttörése fenyeget vagy egy partnerlimit közel van. Szakértői tanulmányok szerint a kézi munkateher csökkenése [30-50% a készpénzpozicionálás, az előrejelzés és a kivételkezelés terén](https://assistents.ai/blogs/ai-agent-use-cases-in-banking-2026 "MI-ügynökök felhasználási esetei a bankszektorban: 2026-os értékelés"), és a [Capgemini 2026-os banki kitekintése](https://www.capgemini.com/insights/research-library/banking-top-trends-2026/ "Capgemini: a bankszektor fő trendjei 2026") a treasury ügynöki MI-t azon kevés felhasználási eset egyikeként nevezi meg, ahol a 2026-os ráfordítás mérhető kiszolgálásiköltség-csökkenést eredményez.

Ez a cikk az [autonóm treasury index](https://sebastienrousseau.com/2026-06-07-autonomous-treasury-index-programmable-liquidity-tokenised-deposits-2026/) természetes második része. Az index a célt határozza meg: programozható likviditás, tokenizált betétek, gépileg olvasható szabályzat. A társpilóták azok a termelési egységek, amelyek egy CIB treasuryt eljuttatnak oda anélkül, hogy megsértenék az SR 11-7-et, a DORA-t vagy az EU AI Act-et.

## 01. A kísérlettől a termelésig

A 2024–2025-ös évek a treasury pilotokról szóltak. A 2026-os év a treasury termelésről szól.

A [Forrester Predictions 2026: Banking and Investing](https://www.forrester.com/report/predictions-2026-banking-and-investing/RES185001 "Forrester: Predictions 2026: Banking and Investing") egyértelműen fogalmaz: 2026-ban a Tier-1 bankok többsége legalább egy ügynöki felhasználási esetet a homokozóból élő, mért termelési környezetbe visz át, és a treasury az első három közé tartozik, amely átlépi ezt a küszöböt. A [Capgemini 2026-os banki fő trendekről szóló jelentése](https://www.capgemini.com/insights/research-library/banking-top-trends-2026/ "Capgemini: a bankszektor fő trendjei 2026") ugyanezt más nézőpontból erősíti meg: az ügynöki MI-be irányuló beruházás a horizontális termelékenységi kísérletektől a vertikális, funkcióspecifikus bevezetések felé mozdul el, ahol a vállalati treasury, a fizetési műveletek és a KYC-korrekció viszi el az új 2026-os költségvetés nagy részét.

Mi változott? Három dolog.

Először, az adatréteg. Az ISO 20022 migráció a legtöbb fő deviza esetében 2025 novemberében befejeződött, így a készpénz- és fizetési adatok olyan strukturált formában érkeznek, amelyet egy ügynök törékeny képernyőleolvasó réteg nélkül is fel tud dolgozni.

Másodszor, a vezérlősík. Az MCP szabványosította, hogyan hívnak eszközöket az ügynökök, és a bankoknak most már megvédhető válaszuk van a CRO kérdésére: "mit is tud valójában ez az ügynök?" A válasz azon MCP eszközök jegyzéke, amelyekhez kötve van, semmi több.

Harmadszor, a szabályozók megszűntek hipotetikusak lenni. Az SR 11-7 felügyeleti iránymutatást kiterjesztették a nem determinisztikus modellekre is; a DORA 2025 januárjában lépett életbe; az EU AI Act magas kockázatú besorolási rendszere 2026 augusztusában kezdte éreztetni a hatását.

## 02. Az architektúra: adatok + ISO + eszközhívások

Egy termelési treasury társpilótának 2026-ban három rétege van, ebben a sorrendben.

**Adatok.** Az ügynök ISO 20022 üzeneteket olvas: `camt.052` (napközbeni kivonat), `camt.053` (napzárás), `camt.054` (terhelési/jóváírási értesítés), valamint pacs.008 ügyfél-átutalásokat, ahogy azok áthaladnak a bank fizetési sínjein. Az ügynök beolvassa a strukturált üzenetet, és egyezteti a főkönyvvel. Az [Elire 2026-os treasury MI-forgatókönyve](https://web.archive.org/web/20260124183820/https://elire.com/treasurys-ai-playbook-ete-2025/ "Elire: Treasury's AI playbook 2025-2026") ezt előfeltételként fogalmazza meg: ha az ügynök nem képes strukturált ISO 20022 adatokat olvasni, akkor az előrejelzés pontosságáról szóló minden későbbi állítás csupán marketing.

**Következtetés.** Egy korlátozott alapmodell, jellemzően egy belső élvonalbeli modell finomhangolt treasury szabályzati adapterrel, az ISO 20022 valóságot javasolt műveletté alakítja. A következtetési lépés soha nem érint fizetési sínt. Strukturált eszközhívási kérést állít elő: "vezess át 180 millió GBP-t az EUR nostróból az X BoE-szintű partnernél az Y GBP RTGS-számlára 14:30-kor, hogy a GBP napközbeni puffer a szabályzati alsó határ felett maradjon."

**Eszközhívások.** Az ügynök MCP-ben regisztrált eszközöket hív. Minden eszköz egy típusos, auditált függvény: `propose_sweep`, `simulate_fx_hedge`, `query_limit`, `submit_pacs008_for_human_approval`. Az MCP eszköz az egyetlen út a valós hatás felé. A konfigurált küszöb feletti SWIFT-benyújtás emberi treasurerhez kerül jóváhagyásra; a küszöb alatt az ügynök egy napközbeni szabályzati sávon belül nyújthat be, és a művelet ugyanazon a másodpercen belül egy WORM auditnaplóba kerül.

A fegyelem abban áll, hogy a modellnek soha nincs adatbázis-írási jogosultsága, soha nincsenek közvetlen SWIFT-hitelesítő adatai, és soha nem olvas strukturálatlan képernyőket. Az MCP jegyzék a biztonsági határ, és az OPA szabályzatok kényszerítik ki, hogy melyik ügynökidentitás mit hívhat.

## 03. Felhasználási esetek és metrikák

Három treasury társpilóta felhasználási eset van termelésben CIB léptékben 2026-ban.

**Készpénzpozicionálás.** Az ügynök élő napközbeni készpénzpozíciót tart fenn a nostro számlák között, előre jelzi a folyamatban lévő pacs.008 üzeneteket, és sweepeket javasol, hogy a pufferek a szabályzati sávokon belül maradjanak. Jelentett hatás: 35-45%-os csökkenés a kézi egyeztetési időben, mérhető visszaesés a napzárási puffer túlfinanszírozásában (ami javítja a tétlen készpénz nettó kamatmarzsát), és a napközbeni RTGS folyószámlahitel-események nullához közelítenek azokban a pilotokban, amelyek egy teljes negyedévet lezártak.

**Készpénz-előrejelzés.** Az ügynök beolvassa a történeti ISO 20022 áramlásokat, az ügyfél-viselkedési jelzéseket és az ismert naptári eseményeket (adóhatáridők, osztalékfizetési időpontok, kötvénykuponok), és 1 napos, 5 napos és 30 napos készpénz-előrejelzést állít elő konfidenciaintervallummal. Az 5 napos előrejelzések átlagos abszolút százalékos hibája a jobban műszerezett CIB treasuryknél a ~7-9%-os regressziós alapszintről ~3-4%-ra csökkent, ami érdemben javítja a CFO finanszírozási tervét.

**Kivételkezelés.** Az ügynök osztályozza a fizetési kivételeket: sikertelen pacs.008 üzenetek, szankcionált partnerre eső találatok, nem egyező átutalási adatok, és javaslatot tesz a rendezésre (javítás, visszaküldés, eszkaláció). Az osztályozási idő ~7 percről (csak ember) ~90 másodpercre (ember a hurokban) csökkent, és az ember szerepe az adatgyűjtésről a döntéshozatalra tolódik.

A becsületes metrika nem az "automatizált feladatok" száma, hanem az, hogy "a treasurer figyelmét az adatösszeállításról a mérlegelésre irányítottuk át". Ez az a szám, amelyet egy CFO megvédhet az igazgatóság előtt, egy CRO pedig a szabályozó előtt.

## 04. Irányítás, audit és SR 11-7 illeszkedés

Az ügynöki treasury előbb modellkockázati probléma, mintsem termelékenységi történet.

**SR 11-7 és MRM.** A Federal Reserve [SR 11-7 modellkockázat-kezelési iránymutatása](https://web.archive.org/web/20260414150921/https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm "Federal Reserve: SR 11-7 modellkockázat-kezelés") szerint minden olyan modell, amely érdemben befolyásol pénzügyi döntéseket, dokumentált fejlesztést, független validálást és folyamatos teljesítménymonitorozást igényel. Egy treasury társpilóta az SR 11-7 szerinti modell. Az MRM felelős a leltárba vételért, a validáció a challenger-tesztelésért (az ügynök előrejelzése felülmúlja-e a regressziós alapszintet egy elkülönített időablakon?), a termelés pedig a driftmonitorozásért. Azok a bankok, amelyek a társpilótát "csupán eszközként" kezelik, tévesen sorolják be a kockázatot.

**DORA.** Az [(EU) 2022/2554 rendelet (DORA)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R2554 "DORA: Digital Operational Resilience Act") 5. cikke az igazgatóságot teszi végső soron felelőssé az IKT-kockázatért. A treasury társpilóták kritikus funkciót támogató IKT-rendszerek: az igazgatóságnak jóvá kell hagynia a kockázati keretrendszert, a harmadik feles szolgáltatói koncentrációt és a kilépési tervet. A vészleállító kapcsoló (az MCP eszközhozzáférés visszavonása és percek alatt visszaállás a kizárólag emberi működésre) egy DORA-kontroll, nem pedig kellemes ráadás.

**EU AI Act.** Egy treasury társpilóta, amely érdemi pénzügyi döntéseket befolyásol, a magas kockázatú besorolás alá esik, ami kötelezi a bankot arra, hogy kockázatkezelési rendszert tartson fenn, minden műveletet OTLP-kompatibilis telemetriába naplózzon, emberi felügyeletet működtessen, és kérésre megfelelőségi dokumentációt állítson elő. A reális megvalósítás teljes OTLP-nyomkövetés minden ügynöki következtetési lépésre, valamint WORM-ban tárolt eszközhívási auditnaplók, és egy emberi ellenőr minden olyan műveletre, amely átlép egy szabályzati sávot.

**Felügyeleti párbeszéd.** A Bank of England (BoE) és a Financial Conduct Authority (FCA) 2025-2026 folyamán egyértelművé tette, hogy látni akarja a leltárt, a validálási bizonyítékokat és a vészleállító kapcsolót, ebben a sorrendben. A beszélgetés akkor megy jól, ha a CRO mindhármat egyetlen teremben be tudja mutatni.

A vezérlősík a védőárok. Az a bank, amely meg tudja mutatni a felügyeletének az MCP jegyzéket, az OPA szabályzatfájlt, a WORM auditnaplót, az OTLP-nyomkövetési adatfolyamot és az SR 11-7 validálási csomagot, egyetlen ülés alatt, készen áll arra, hogy treasury társpilótákat futtasson termelésben. Az a bank, amely erre nem képes, engedély nélküli pilotot üzemeltet.

## Következtetés

Az autonóm treasury index a célt határozta meg: programozható likviditás, tokenizált betétek, gépileg olvasható szabályzat. Ez az írás a második rész: az a termelési egység, amely egy CIB treasuryt eljuttat oda. A minta stabil: ISO 20022 adatok, MCP-vel körülhatárolt eszközhívások, SR 11-7 irányítás, DORA-elszámoltathatóság, EU AI Act audit. Azok a 2026-os treasury társpilóták, amelyek túlélik az első felügyeleti felülvizsgálatukat, ugyanolyan alakúak; amelyek nem, azokból ugyanaz a három dolog hiányzik: az MRM validálási csomag, a vészleállító kapcsoló és a WORM auditnapló.

A 2026-os érdekes munka nem a modell. Hanem a modellt körülvevő vezérlősík, és az a CFO-beszélgetés, amely a 30-50%-os kézimunkateher-csökkenést megvédhető kiszolgálásiköltség-számmá alakítja.

A felmenő kontextushoz lásd az [autonóm treasury indexet](https://sebastienrousseau.com/2026-06-07-autonomous-treasury-index-programmable-liquidity-tokenised-deposits-2026/ "Az autonóm treasury index 2026"), az irányítási kerethez pedig a [bankok ügynöki MI-indexét](https://sebastienrousseau.com/2026-06-03-agentic-ai-index-banks-autonomy-governance-auditability-2026/ "A bankok ügynöki MI-indexe 2026").
