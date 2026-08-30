---
title: "A pain.001-től a programozható likviditásig: az ISO 20022 mint a treasury autonóm idegrendszere 2026-ban"
tags: "ISO 20022, pain.001, pacs.008, MX, SWIFT, CBPR+, programmable liquidity, autonomous treasury, BIS, structured addresses, DORA, agentic AI, cross-border payments, CIB"
subtitle: "Az ISO 20022 2026-ban már nem migrációs projekt. Ez az az adatréteg, amely a programozható likviditás, az ügynöki treasury és a 2026. novemberi SWIFT MT/MX átállás alatt húzódik, amelynek teljesítésétől a világ bankjainak közel fele még mindig le van maradva."
description: "ISO 20022 pain.001 és pacs.008 2026-ban: hogyan építik újra az MX-natív treasury API-k, a strukturált címek és a programozható likviditás a CIB-treasury autonóm idegrendszerét."
date: "June 23, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/markus-spiske-FXFz-sW0uwo.webp"
banner_alt: "Egy modern klíringközpont acélartériái hajnalban, amelyek az ISO 20022 pain.001 és pacs.008 üzeneteket jelképezik: a programozható likviditást a globális treasury, a SWIFT MX és a CBPR+ hálózatokon átvivő autonóm idegrendszer"
keywords: "ISO 20022, pain.001, pacs.008, MX, SWIFT, CBPR+, programozható likviditás, autonóm treasury, BIS CPMI, strukturált címek, DORA, ügynöki MI, határokon átnyúló fizetések, CIB, MT103, MT202, RTGS, Basel III, SR 11-7, treasury API-k"
---

## A pain.001-től a programozható likviditásig: az ISO 20022 mint a treasury autonóm idegrendszere 2026-ban

### Az ISO 20022 2026-ban már nem migrációs projekt. Ez az az adatréteg, amely a programozható likviditás, az ügynöki treasury és a 2026. novemberi SWIFT MT/MX átállás alatt húzódik, amelynek teljesítésétől a világ bankjainak közel fele még mindig le van maradva.

> **Vezetői összefoglaló.** Öt hónappal a 2026. november 22-i SWIFT MT/MX átállás előtt az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) megszűnt migrációs projekt lenni, és a vállalati és befektetési banki treasury adatrétegévé vált. Az a 44% bank, amelyet a RedCompass Labs felkészültségi felmérése lemaradóként jelentett, nem egy vezetékformátum-cserével van elmaradva; egy testületi felelősséggel járó kötelezettséggel vannak elmaradva, hogy strukturált célkódokat, strukturált `<PstlAdr>` címeket és CBPR+-kompatibilis fizetési adatokat juttassanak el minden általuk kezdeményezett vagy fogadott, határokon átnyúló fizetésbe. Ez a cikk a pain.001-et a programozható likviditási verem szívverésének mutatja be: hogyan néz ki éles üzemben egy ISO-first kanonikus séma, egy elemzés közbeni validációt végző bemenet, és egy olyan vezérlősík, amely közvetlenül a pacs.008-at fogyasztja; és milyen szabályozói büntetés vár azokra a bankokra, amelyek november 22-én még mindig fordítási problémaként kezelik.

2026 júniusában az ISO 20022 megszűnt migrációs történet lenni. Ez az alapréteg. Minden komoly vállalati és befektetési bank ma már a `pain.001`, `pacs.008` és `camt.053` üzeneteket tekinti a treasury elsődleges adatmodelljének, nem pedig a hálózat szélén lefordítandó vezetékformátumnak. És mégis, öt hónappal a [2026. november 22-i SWIFT MT/MX átállás](https://www.redcompasslabs.com/insights/what-now-iso-20022-deadlines-in-2026-onwards/ "RedCompass Labs: ISO 20022 határidők 2026-tól") előtt [a világ bankjainak közel fele még mindig le van maradva](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Financial IT: a bankok közel fele le van maradva az ISO 20022-vel") a strukturáltadat-, strukturáltcím- és CBPR+-kötelezettségek teljesítésétől, amelyeket a hálózat megkövetel.

Ez a szám, a legfrissebb iparági felmérés szerint 44%, a határokon átnyúló fizetések területén az idei év legfontosabb ténye. Ez nem technológiai történet. Ez testületi felelősségi történet. Azok a bankok, amelyek november 22-én még mindig strukturálatlan címtömbökkel ellátott MT103 vagy pain.001 üzeneteket bocsátanak ki, elzáródnak az MX-only levelező bankoktól, a többiek felárat számolnak fel nekik, és képtelenek lesznek táplálni bármely ügynöki treasury motort, amely gépileg olvasható cél-, fizetési és szabályozói adatoktól függ.

Az ezen az oldalon található 2023-as cikk, az [ISO 20022-kompatibilis fizetési fájlok létrehozásának automatizálása a pain.001 segítségével](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001), a pain.001-et generálási problémaként keretezte. 2026-ban a keret más. A pain.001 ma már a programozható likviditási verem szívverése: az, amit az [Autonomous Treasury Index 2026](https://sebastienrousseau.com/2026-06-07-autonomous-treasury-index-programmable-liquidity-tokenised-deposits-2026) a CIB-treasury autonóm idegrendszerének nevez. Az üzenetek a jel. A séma a huzalozás.

## 01. Az együttélés vége

A SWIFT MT/MX együttélési időszaka 2026. november 22-én ér véget. Ezt a dátumot követően a FIN MT határokon átnyúló kategóriák, az MT103, MT202, MT202COV és a kapcsolódó MT9xx jelentési üzenetek kivonulnak a határokon átnyúló használatból. A [Banking Vision "utolsó fejezet" tájékoztatója](https://banking.vision/en/iso-20022-the-final-chapter-begins/ "Banking Vision: ISO 20022, kezdődik az utolsó fejezet") helyesen írja le: ez nem egy újabb hosszabbítás. A hálózat fordítási átjárója továbbra is működni fog, de minden bank, amely lefordított üzenetet küld vagy fogad, kétszer fizet a kiváltságért: egyszer díjakban, egyszer az elveszett adathűségben.

A strukturális probléma az adat. Az MT103 35 karakternyi strukturálatlan fizetési adatot hordoz a 70-es mezőben, és egy szabad szöveges címet az 50K mezőben. A pacs.008 hordozza az `<RmtInf>`-et strukturált hitelezői hivatkozással, a `<PstlAdr>`-t utcával, irányítószámmal, várossal és országkóddal különálló elemekként, valamint az `<RgltryRptg>`-t a joghatóság-specifikus kötelezettségekhez. A 2024-es CBPR+ frissítés a valaha "lehet" mezőket "kell" mezőkké alakította. Azok a bankok, amelyek lefordítanak MT103-ra, elveszítik azokat az adatokat, amelyekre szükségük van a megbízóra és a kedvezményezettre vonatkozó információkról szóló [FATF 16. ajánlás](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html "FATF-ajánlások") teljesítéséhez.

Az együttélés udvariasság volt. Vége van.

## 02. Az ISO mint adatréteg az ügynökök számára

Az érdekes munka a 2026-os treasuryben a séma felett zajlik. A programozható likviditási motorok, a napközbeni hiteloptimalizálók és az ügynöki treasury munkafolyamatok mind gépileg olvasható, sémavalidált fizetési adatoktól függenek. Gyakorlati értelemben egy ügynöki treasury automatikusan optimalizálja a napközbeni likviditási pozícionálást azáltal, hogy a strukturált `<Purp>` kódokat és a fizetési adatokat összeveti a valós idejű finanszírozási igényekkel: pénzt mozgat, hitelkereteket vesz igénybe, vagy visszatartja a végrehajtást emberi beavatkozás nélkül. Az MT103 nem tudja ezt szolgáltatni. A pacs.008 igen.

A [BIS CPMI jelentés az ISO 20022 harmonizációjáról a határokon átnyúló fizetésekhez](https://www.bis.org/cpmi/publ/d230.pdf "BIS CPMI: harmonizált ISO 20022 adatkövetelmények") 2023-ban tette közzé a kanonikus üzenet- és adatkövetelmény-készletet. A 2026-os kiegészítés élesebb foggal fogalmazza meg ugyanezt: a harmonizáció már nem ajánlás, hanem előfeltétele a [G20 határokon átnyúló fizetési ütemtervének](https://www.bis.org/cpmi/publ/d193.htm "BIS CPMI: G20 határokon átnyúló fizetési ütemterv") a költségre, sebességre, átláthatóságra és hozzáférésre vonatkozó céljainak. Strukturált `<Purp>` kódok, strukturált címek és strukturált fizetési adatok nélkül egy ügynöknek nincs miről gondolkodnia. Prózája van.

Ez az a pont, ahol az [Autonomous Treasury Index 2026](https://sebastienrousseau.com/2026-06-07-autonomous-treasury-index-programmable-liquidity-tokenised-deposits-2026) tézise leér. A programozható likviditás nem varázslat. Ez annak fegyelme, hogy az ügynököket kanonikus, sémavalidált ISO 20022 üzenetekkel tápláljuk, és hagyjuk, hogy a policy-as-code szabályozza, mit és kinek mozgathatnak az ügynökök. Az MX üzenet az idegimpulzus. A treasury vezérlősík a gerincvelő. Az SR 11-7 modellkockázat-kormányzás és a DORA 5. cikkely szerinti testületi felelősség a tetején ül központi idegrendszerként.

Vedd el az MX-et, és az ügynökök megvakulnak.

## 03. Natív MX vagy másodrendű állampolgár

Két operatív valóság alakítja át a gazdaságosságot ebben a negyedévben. Először, a nagy levelező bankok közzétették a 2026 negyedik negyedévétől érvényes felárrendszereiket az MT-only partnerek számára: jellemzően egy üzenetenkénti felárat a lefordított forgalomra, plusz elutasítási díjakat azokra az üzenetekre, amelyek nem mennek át a CBPR+ strukturáltcím-validáláson. Másodszor, a SWIFT FINplus csatorna azonnal elutasítja a hibás pacs.008-at, MT-tartalék nélkül az új, határokon átnyúló forgalomra.

Ez a lemaradó viselkedés költségét projektterhelésből ismétlődő margóapasztássá változtatja. Egy középső kategóriás tranzakciós bank, amely havonta kétmillió határokon átnyúló fizetést dolgoz fel akár néhány centes üzenetenkénti felárral, hétjegyű éves többletköltséggel néz szembe, még a meghiúsult fizetések ügyfélélmény-költsége és a fordítási adót fizetőnek lenni hírnévköltsége előtt.

Maguk a CBPR+ validációs szabályok nem alku tárgyai. Strukturált `<PstlAdr>` `<Ctry>`-vel és a `<StrtNm>`/`<TwnNm>`/`<PstCd>` közül legalább eggyel kitöltve. LEI az `<OrgId>/<LEI>`-ben, ahol a megbízó vagy a végső hitelező jogi személy. ISO 4217 devizakódok. ISO 8601 dátumok időzónával. Bármi más elbukik a hálózati átjárónál, nem a célbanknál, ami azt jelenti, hogy a küldő bank fizeti az elutasítás költségét, és az ügyfél látja először a meghiúsult fizetést.

Nincs puha landolás.

## 04. ISO-first treasury API-k tervezése

A 2026-os helyes mérnöki minta az ISO-first. A belső séma, az API-szerződés és a vezetéken lévő üzenet mind ugyanazt a kanonikus modellt osztja: `pain.001` az ügyfél-bank kezdeményezéshez, `pacs.008` a bankközi elszámoláshoz, `camt.054` a jóváírási értesítéshez, `camt.053` a napvégi jelentéshez. A JSON-borítékok rendben vannak a fejlesztői élményrétegben, de a mezőnevek, a strukturált cím, a célkód és a szabályozói jelentési blokk kanonikus marad végponttól végpontig.

Egy minimális pain.001.001.09 részlet, amely a strukturáltcím-kötelezettséget mutatja:

```xml
<CdtTrfTxInf>
  <PmtId>
    <EndToEndId>E2E-2026-06-23-0001</EndToEndId>
  </PmtId>
  <Amt>
    <InstdAmt Ccy="EUR">125000.00</InstdAmt>
  </Amt>
  <Cdtr>
    <Nm>Acme Manufacturing SA</Nm>
    <PstlAdr>
      <StrtNm>Rue de la Loi</StrtNm>
      <BldgNb>200</BldgNb>
      <PstCd>1049</PstCd>
      <TwnNm>Brussels</TwnNm>
      <Ctry>BE</Ctry>
    </PstlAdr>
    <Id>
      <OrgId>
        <LEI>529900T8BM49AURSDO55</LEI>
      </OrgId>
    </Id>
  </Cdtr>
  <CdtrAcct>
    <Id><IBAN>BE71096123456769</IBAN></Id>
  </CdtrAcct>
  <Purp>
    <Cd>GDDS</Cd>
  </Purp>
  <RmtInf>
    <Strd>
      <CdtrRefInf>
        <Tp><CdOrPrtry><Cd>SCOR</Cd></CdOrPrtry></Tp>
        <Ref>RF18539007547034</Ref>
      </CdtrRefInf>
    </Strd>
  </RmtInf>
</CdtTrfTxInf>
```

Ebből két elv következik. Először, a `<PstlAdr>` blokk nem opcionális a CBPR+ 3. fázisától kezdve. Bármely belső API, amely egyetlen szabad szöveges címsort fogad el, jövőbeli elutasítás. Másodszor, a `<Purp>` kód és a `<RmtInf><Strd>` blokk az, ami az üzenetet gépileg olvashatóvá teszi egy treasury ügynök számára. Egy `GDDS` célkód plusz egy strukturált `SCOR` hitelezői hivatkozás emberi beavatkozás nélkül egyeztethető. Egy 35 karakteres, szabad szöveges megjegyzés nem.

Egy pragmatikus API-felület egy 2026-os vállalati banki platformhoz egy vékony REST-réteg a kanonikus séma felett. A `POST /v1/payments/credit-transfer` egy JSON-törzset fogad el, amely egy az egyben leképeződik a pain.001 elemekre. A szerver a bemeneten validál a CBPR+ XSD ellen, megőrzi a kanonikus XML-t, aláírja azt a letagadhatatlanság érdekében, és WORM auditeseményt bocsát ki. Ugyanaz a végpont `camt.054` és `camt.053` visszahívásokat bocsát ki a kanonikus modellen. Nincs fordítás. Nincs elcsúszás.

Ez az ISO-first éles üzemben.

## GYIK

**Mi változik 2026. november 22-én, ami 2025 novemberében nem változott?**
2025 novembere a FIN MT/MX együttélés leépítésének kezdete volt a határokon átnyúló kategóriákra. 2026 novembere a vég. Ezt a dátumot követően a FIN MT103, MT202, MT202COV és az MT9xx jelentési sorozat kivonul a határokon átnyúló használatból. A hálózat fordítási átjárója továbbra is működni fog, de minden lefordított üzenet díjakban és elveszett adathűségben fizet. A CBPR+ strukturáltcím- és strukturáltfizetési mezők megszűnnek opcionálisak lenni.

**Ugyanaz-e a pain.001, mint a pacs.008?**
Nem. A pain.001 az ügyfél-átutalás kezdeményezési üzenet: vállalati ERP-től bankig. A pacs.008 a bankközi átutalás: banktól bankig, SWIFT-en vagy azzal egyenértékű hálózaton. A kettő osztja az ISO 20022 nyelvtant és a strukturális elemek nagy részét (`<PstlAdr>`, `<RmtInf>`, `<Purp>`, `<Dbtr>` / `<Cdtr>` / `<DbtrAgt>` / `<CdtrAgt>`), de eltérő üzenetek eltérő szakaszokon. Egy 2026-os treasury platform a bemeneten validálja a vállalati pain.001-et, és a bankközi ugráson kibocsátja a pacs.008-at újbóli leképezés nélkül.

**Miért olyan nagy dolog a strukturált `<PstlAdr>` blokk?**
Mert a FATF 16. ajánlás és a CBPR+ 3. fázis egyaránt strukturált címadatokat követel a határokon átnyúló megbízói és kedvezményezetti mezőkön. Egy szabad szöveges címsor nem validálható, szűrhető vagy egyeztethető nagy léptékben. A strukturált `StrtNm` / `PstCd` / `TwnNm` / `Ctry` elemek igen. 2026 novemberétől azok a bankok, amelyek strukturálatlan címeket bocsátanak ki, elemzéskor elutasításra kerülnek az MX-only levelező bankok által, és felárat kapnak a fordítástűrők által.

**Mit jelent az "ISO-first" egy belső API számára?**
Azt jelenti, hogy a kanonikus modell a bank oldalán az API-nak az ISO 20022 elemfa, nem egy lapított, bank-proprietáris JSON. A `POST /v1/payments/credit-transfer` egy olyan kéréstörzset fogad el, amely egy az egyben leképeződik a pain.001-re. A szerver a bemeneten validál a CBPR+ XSD ellen, megőrzi a kanonikus XML-t, és pacs.008-at bocsát ki a hálózatra. Nincs szélen történő fordítás, nincs szemantikai elcsúszás a vállalat kérése és aközött, ami a levelező bankhoz érkezik.

**Hol hagyja ez azt a bankot, amely még el sem kezdte?**
Öt hónap elég idő ahhoz, hogy leszállítsunk egy a CBPR+-nál szigorúbb üzenetprofilt és egy elemzéskori elutasítást végző bemenetet, egy párhuzamosan futó CBPR+ validációt élő levelezőbanki forgalom ellen, és egy pacs.008-natív elszámolási szakaszt a top 20 folyosóra. Ez nem elég idő egy mag újraplatformozásához. Az ilyen helyzetben lévő bankoknak sorrendbe kell állítaniuk: elemzés közbeni validáció először (megállítja a vérzést a kimenő forgalomban), strukturáltcím-javítás másodszor (bezárja a szabályozói rést), teljes pacs.008-natív elszámolás harmadszor (megragadja a programozható likviditási előnyt a határidő után).

## Következtetés

A 2026. novemberi határidő a könnyű rész. A nehéz rész az, amit a határidő kikényszerít. Azok a bankok, amelyek időben érkeznek, de még mindig fordítási problémaként kezelik a pain.001-et, a következő évtizedet a treasury adatmodelljük vezetéktől befelé történő újjáépítésével fogják tölteni. Azok a bankok, amelyek ISO-first kanonikus sémával, alapértelmezés szerint strukturált címekkel, és egy olyan programozható likviditási vezérlősíkkal érkeznek, amely közvetlenül a pacs.008-at fogyasztja, ügynöki treasuryt fognak működtetni a DORA 5. cikkely szerinti testületi felelősség, a [Basel III](https://www.bis.org/bcbs/publ/d424.htm "Basel III: a válság utáni reformok véglegesítése") operatívkockázat-fegyelme és az [SR 11-7](https://web.archive.org/web/20260414150921/https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm "SR 11-7 útmutató a modellkockázat kezeléséhez") modellkormányzás alatt.

Az autonóm idegrendszer keretezés nem díszítés. A treasury nem tud olyan likviditásról gondolkodni, amelyet nem lát. Az ügynökök nem tudnak olyan adatra cselekedni, amelyet nem tudnak elemezni. Az ISO 20022 a CIB-treasury huzalozása 2026-ban: a strukturált üzenet az akciós potenciál, a séma az az auditnapló, amelyet a szabályozó a következő incidens másnapján követelni fog.

Öt hónap. Építsd a sémát, ne a kerülő megoldást.

## Hivatkozások

Bank for International Settlements, Committee on Payments and Market Infrastructures (2023). *Harmonised ISO 20022 data requirements for enhancing cross-border payments* (CPMI Papers No. 230). Elérhető: [https://www.bis.org/cpmi/publ/d230.htm](https://www.bis.org/cpmi/publ/d230.htm "BIS CPMI 230: Harmonizált ISO 20022 adatkövetelmények")

Basel Committee on Banking Supervision (2017). *Basel III: Finalising post-crisis reforms*. Bank for International Settlements. Elérhető: [https://www.bis.org/bcbs/publ/d424.htm](https://www.bis.org/bcbs/publ/d424.htm "Basel III: Finalising post-crisis reforms")

European Parliament and Council (2022). *Regulation (EU) 2022/2554 on digital operational resilience for the financial sector (DORA)*. Elérhető: [https://eur-lex.europa.eu/eli/reg/2022/2554/oj](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "Regulation (EU) 2022/2554 — DORA")

Financial Action Task Force (2023). *International standards on combating money laundering and the financing of terrorism — Recommendation 16 on wire transfers*. Elérhető: [https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html "FATF-ajánlások")

Federal Reserve (2011). *SR 11-7 Guidance on Model Risk Management*. Elérhető: [https://web.archive.org/web/20260414150921/https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm](https://web.archive.org/web/20260414150921/https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm "SR 11-7 Guidance on Model Risk Management")

International Organization for Standardization (2022). *ISO 20022 Financial services — Universal financial industry message scheme*. Elérhető: [https://www.iso20022.org](https://www.iso20022.org "ISO 20022 — Universal financial industry message scheme")

RedCompass Labs (2025). *What now? ISO 20022 deadlines in 2026 onwards*. Elérhető: [https://www.redcompasslabs.com/insights/what-now-iso-20022-deadlines-in-2026-onwards/](https://www.redcompasslabs.com/insights/what-now-iso-20022-deadlines-in-2026-onwards/ "RedCompass Labs — ISO 20022 deadlines in 2026 onwards")

SWIFT (2024). *Cross-Border Payments and Reporting Plus (CBPR+) usage guidelines*. Elérhető: [https://www.swift.com/standards/iso-20022/iso-20022-programme](https://www.swift.com/standards/iso-20022/iso-20022-programme "SWIFT CBPR+ usage guidelines")
