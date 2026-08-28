---
title: "A 2026. novemberi pacs.008 strukturáltcím-határidő: hathónapos áttekintés"
tags: "ISO 20022, pacs.008, CBPR+, structured address, SWIFT, cross-border payments, sanctions screening, FI-to-FI credit transfer, payments, DORA, post-quantum cryptography, AI, tokenised deposits, open source, quantum computing"
subtitle: "2026. november közepétől a SWIFT CBPR+ elutasítja a strukturálatlan postai címeket a pacs.008 és a kapcsolódó, határokon átnyúló fizetési üzenetekben. Mivel az üzenetek megközelítőleg 65%-a továbbra sem megfelelő, a hibajavítási ablak gyorsan bezárul."
description: "2026 novemberétől a SWIFT CBPR+ strukturált postai címeket követel meg a határokon átnyúló fizetési üzenetekben. A strukturálatlan címsorok (önmagában az AdrLine) többé nem lesznek elfogadva a pacs.008 kulcsfontosságú félmezőiben. Legalább a TwnNm és a Ctry kötelező, a StrtNm, valamint a BldgNb vagy a PstBx pedig ajánlott. Hat hónappal a határidő előtt a fizetési üzenetek 65%-a még mindig strukturálatlan címeket tartalmaz, a bankok 44%-a pedig le van maradva az ütemtervhez képest."
date: "May 12, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "ISO 20022 pacs.008 strukturált cím diagram: határokon átnyúló fizetési üzenet mezői kiemelt TwnNm és Ctry elemekkel"
keywords: "ISO 20022, pacs.008, SWIFT CBPR+, strukturált cím, 2026 november, postai cím, TwnNm, Ctry, StrtNm, BldgNb"
---

## A 2026. novemberi pacs.008 strukturáltcím-határidő: hathónapos áttekintés

2026. november közepétől a SWIFT CBPR+ elutasítja a strukturálatlan postai címeket a pacs.008 és a kapcsolódó, határokon átnyúló fizetési üzenetekben. Mivel az üzenetek megközelítőleg 65%-a továbbra sem megfelelő, és a bankok 44%-a le van maradva az ütemtervhez képest, a hibajavítási ablak gyorsabban zárul be, mint amire a legtöbb felkészülési program tervezve van.

---

> **Legfontosabb tanulságok**
>
> - **2026 novemberétől** a SWIFT CBPR+ többé nem fogadja el a strukturálatlan postai címeket a határokon átnyúló fizetési üzenetekben. A változás a **pacs.008** (ügyfél-átutalás), a **pacs.009** (pénzügyi intézmények közötti átutalás), a **pacs.004** (visszautalások) és a **pacs.003** (beszedések) üzenetekre, valamint az ezeket tápláló, feljebb elhelyezkedő **pain.001** folyamatokra vonatkozik.
> - Legalább a **Town Name (TwnNm)** és a **Country (Ctry)** elemnek szerepelnie kell erre kijelölt strukturált mezőkben. A **Street Name (StrtNm)**, valamint a **Building Number (BldgNb)** vagy a **PO Box (PstBx)** használata erősen ajánlott. A szabad szöveges címsorok (AdrLine) önmagukban többé nem elégítik ki a kulcsfontosságú félmezőkre vonatkozó követelményt.
> - A változás javítja a szankciószűrés pontosságát, csökkenti a kézi javítások arányát, és védi a közvetlen feldolgozást (straight-through processing), de csak azoknál az intézményeknél, amelyek a feljebb elhelyezkedő ügyféladataikat is rendbe tették, nem csupán az üzenetmotorjaikat.
> - Az iparági felkészültség egyenetlen. 2026 márciusában a **CBPR+ üzenetek mintegy 65%-a még mindig strukturálatlan címeket hordoz**, a **bankok 44%-a** nincs jó úton a határidő teljesítéséhez, és **az ügyfélcím-nyilvántartások 32%-a** átlagosan strukturálatlan marad.
> - A nyílt forráskódú eszközök, köztük a **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, amely egy Python-könyvtár és FastAPI-szolgáltatás a pacs.008 üzenetfolyamok generálásához, validálásához és vezényléséhez, lerövidíthetik a hibajavítási határidőket azáltal, hogy automatizálják a sémavalidálást, a címminőségi ellenőrzéseket és a CI-szintű kikényszerítést, mielőtt az üzenetek elérnék a SWIFT-hálózatot.

---

## Egy határidő, amely mindig is közeledett

A 2026. novemberi strukturált címre vonatkozó követelmény nem hirtelen szabályozói lépés. Az eredeti [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) migráció bejelentése óta szerepel a SWIFT CBPR+ ütemtervén, és az MT/MX együttélés 2025. novemberi végét követi. Ami 2026-ban megváltozott, az a közelség. A hozzávetőleg hat hónap hátralévő idővel az iparág most abban az ablakban működik, ahol a megoldatlan adatminőségi problémák működési kockázattá válnak.

A számok egyértelműen elmondják a történetet. A SWIFT saját, 2026. márciusi közösségi frissítése megjegyzi, hogy [a fizetési üzenetek megközelítőleg 65%-a még mindig strukturálatlan címeket tartalmaz ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), és hogy a bevezetés egyenetlen marad a földrajzi régiók és intézménytípusok között. A RedCompass Labs 2026. márciusi, [308 vezető fizetési szakemberrel készített felmérése ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") megállapította, hogy a bankok 44%-a jelenleg nincs jó úton a strukturált címre vonatkozó határidő teljesítéséhez, annak ellenére, hogy átlagosan 20 millió dollárt, a legnagyobb intézményeknél pedig több mint 30 millió dollárt költenek a 2026-os felkészülésre, átlagosan 13 további munkatársat rendelve az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) programokhoz. Ugyanez a felmérés megállapította, hogy az ügyfélcím-nyilvántartások 32%-a átlagosan strukturálatlan marad, és hogy a bankok 60%-a hiányosságokról számol be az alaprendszereikben (core banking) a strukturált címmezők támogatásakor.

Ez tehát, más szóval, nem olyan probléma, amelyet az üzenetmotoron végzett újabb egy hónapnyi munkával meg lehet oldani. Ez adatminőségi probléma, amely az üzenetrétegtől felfelé húzódik az ügyfélbefogadó rendszerekbe, a KYC-folyamatokba, a vállalati csatornákba és a felhalmozódott, évtizedes szabad szöveges ügyfél-törzsadatokba.

## Mit követel meg valójában a szabály

A SWIFT CBPR+ Standards Release 2026 (SR2026) keretében a fő követelmény elviekben egyszerű, a részletekben viszont könyörtelen. 2026. november közepétől a CBPR+ fizetési üzenetek valamennyi ügynöke és fele esetében [a Town Name és a Country elemet a számukra kijelölt strukturált mezőkben kell megadni ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), nagyon korlátozott kivételekkel (a camt.052, camt.053 és camt.054 kivonatai és értesítései, valamint néhány adminisztratív üzenet a szigorú követelményen kívül marad). Az ügynökök esetében a BIC önmagában való további használata érvényes alternatíva marad a névvel és címmel szemben.

Az átállás után két címformátum megengedett:

- **Teljesen strukturált**: a postai cím minden összetevője a saját, kijelölt [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) elemére van leképezve: StrtNm (Street Name), BldgNb (Building Number) vagy BldgNm (Building Name), PstCd (Post Code), TwnNm (Town Name), CtrySubDvsn (Country Subdivision), Ctry (Country, ISO 3166-1 alpha-2 kódként). Ezt a formátumot a SWIFT kifejezetten a kívánatosabb lehetőségként jelöli meg, ahol csak lehetséges.
- **Hibrid**: a Town Name és a Country a strukturált mezőikbe kerül, míg a cím fennmaradó része legfeljebb két strukturálatlan AdrLine elemet használhat. Fontos, hogy [a strukturált elemeket nem szabad megismételni a strukturálatlan sorokban ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"); bármely adott összetevő esetében a cím vagy az egyik, vagy a másik.

A teljesen strukturálatlan címeket, ahol a teljes cím TwnNm vagy Ctry nélkül, AdrLine elemekben helyezkedik el, egyetlen érintett félmezőben sem fogadják el. Az European Payments Council összehangolta a SEPA szabálykönyvét ugyanezzel az átállással, így [2026. november 15-étől a strukturálatlan formátum az SCT, az SDD és az SCT Inst esetében is tiltott ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). Az összehangolás szándékos: a SWIFT és az EPC egyetlen iparági átállási hétvégét terveztek meg.

A félreértések elkerülése végett a [pacs008 dokumentációja közvetlenül felsorolja az érintett üzeneteket ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"): pacs.008 (adós és kedvezményezett az ügyfél-átutalásokban), pacs.009 (intézményi címek a pénzügyi intézmények közötti átutalásokban és fedezeti fizetésekben), pacs.004 (a felek címei a visszautalásokban) és pacs.003 (beszedések). A követelmény felfelé is továbbterjed: a strukturálatlan címeket hordozó vállalati pain.001 fájlok blokkolják a megfelelő pacs.008 generálását a fogadó banknál.

## Miért tette az iparág ezt prioritássá

A strukturált címek melletti érv nem esztétikai. Működési jellegű, és három helyen mutatkozik meg.

**Szankciószűrés.** Az egyetlen legnagyobb gyakorlati előny az, hogy a strukturált címek lehetővé teszik a szűrőrendszerek számára a fél nevének elkülönítését a helyadatoktól. A szabad szöveges címblokkok rendszeresen okoznak téves találatokat, amikor egy településnév véletlenül átfed egy szankcionált személy nevének egy tokenjével, vagy amikor egy szabad szövegbe ágyazott ország teljesen elkerüli a figyelmet. A strukturált mezők lehetővé teszik a szűrőmotorok számára az országspecifikus kockázati szabályok determinisztikus alkalmazását, és lehetővé teszik a szankciós listával való egyeztetés kikényszerítését az országkód alapján, ahelyett, hogy egy elemzett karakterláncot kellene kitalálni. A CGI UK 2026 márciusában közzétett elemzése kifejezetten hangsúlyozza ezt a pontot: [a strukturált címadatok a működési ellenállóképesség központi elemévé válnak, nem pusztán megfelelési kötelezettséggé ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Kézi javítási arányok.** A határokon átnyúló fizetések ma jelentős működési költséget hordoznak kézi vizsgálatok, kivételkezelés és javítási sorok formájában, amelyek nagy részét olyan címek okozzák, amelyeket a szűrő- vagy útvonalválasztó rendszerek nem tudnak megbízhatóan értelmezni. Azok a bankok, amelyek már áttértek a strukturált címekre, érdemi csökkenésről számolnak be a közvetlen feldolgozás kivételeiben, különösen a korridorközi folyamatokban, ahol a közvetítő ügynököknek korábban olyan szabad szöveges adatokat kellett értelmezniük, amelyek nem tőlük származtak.

**Hálózati szintű kikényszerítés.** Az SR2026 megerősíti a validálást a SWIFT-hálózat rétegében. Néhány új ellenőrzés kezdetben nem blokkoló módban működik, jelezve az adatminőségi problémákat a fizetések leállítása nélkül, de a pálya egyértelmű, és az átállást követően [a nem megfelelő üzeneteket egyenesen elutasítják ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Több egyesült államokbeli fizetési rendszer (Fedwire, CHIPS) és a SWIFT CBPR+ lényegében ugyanarra az ütemtervre konvergál, ami megszünteti az egyes intézmények korábbi terveiben feltételezett szakaszos átállás lehetőségét.

## Mezőszintű nézet: mi változik az üzenetben

A pacs.008 üzenet a korai CBPR+ használati útmutatók 2023. márciusi élesítése óta támogatja a strukturált címeket. Ami 2026 novemberében megváltozik, az nem a séma, hanem a validálás. Eddig a bankok az AdrLine elemeket szabad szöveggel tölthették ki, és azt átküldhették a hálózaton. A határidőtől a félblokkok tartalmának minimális strukturáltmező-követelményeknek kell megfelelnie.

### Kötelező, ajánlott és kivezetett

| Elem | XPath (a `PstlAdr` alatt) | Állapot 2026 novembere után | Megjegyzések |
|---|---|---|---|
| Town Name | `<TwnNm>` | **Kötelező** | Legalább egy strukturált Town Name érintett felenként |
| Country | `<Ctry>` | **Kötelező** | ISO 3166-1 alpha-2 kód |
| Street Name | `<StrtNm>` | Erősen ajánlott | A teljesen strukturált formátumhoz szükséges |
| Building Number | `<BldgNb>` | Ajánlott | Vagy BldgNb, vagy PstBx, de nem mindkettő |
| PO Box | `<PstBx>` | Ajánlott | A BldgNb alternatívája |
| Post Code | `<PstCd>` | Ajánlott | Egyes helyi rendszerek megkövetelik |
| Country Subdivision | `<CtrySubDvsn>` | Opcionális | Állam, régió, tartomány |
| Address Line (szabad szöveg) | `<AdrLine>` | **Korlátozott** | Hibrid esetén legfeljebb 2 sor; soha nem ugyanazon összetevő mellett a strukturált mezőkben |
| Address Type | `<AdrTp>` | Opcionális | Postai címekhez az `ADDR` használata ajánlott |

*Forrás: a SWIFT CBPR+ SR2026 használati útmutatóinak, valamint a [pacs008.com strukturált címre vonatkozó dokumentációjának ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008") szintézise.*

A gyakorlati következmény az, hogy minden olyan intézménynek, amely még mindig kizárólag az AdrLine elemre támaszkodik, akár saját üzenetgenerálásában, akár a vállalati ügyfelektől kapott pain.001 fájlokban, akár a fizetések menet közbeni gazdagítására használt törzsadat-nyilvántartásokban, az átállás előtt strukturált mezőkbe kell migrálnia ezeket az adatokat. A SWIFT menet közbeni fordítási szolgáltatása segíthet az átvitel során, de [2026 januárjától felárat von maga után ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB"), és nem tud megbízhatóan feldolgozni minden címformátumot. A SWIFT kiadott [egy nyílt forráskódú, mesterséges intelligenciára épülő címstrukturáló modellt is ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"), amelyet több mint 200 ország adatain tanítottak be, hogy megbízhatósági pontszámokkal következtessen a Town és a Country elemre a strukturálatlan örökölt adatokból, de ez kifejezetten hibajavítási segédeszköz, nem pedig a tiszta forrásadatok hosszú távú helyettesítője.

## Hogyan segít a pacs008.com lerövidíteni a határidőt

Azon intézmények számára, amelyeknek gyorsan iparosítaniuk kell a címminőségi és üzenetvalidálási folyamataikat, a [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") MIT-licenccel rendelkező nyílt forráskódú eszközkészletet és FastAPI-szolgáltatást kínál, amelyet kifejezetten a pénzügyi intézmények közötti (FI-to-FI) ügyfél-átutalási munkafolyamathoz terveztek. Ez a három olyan réteget kezeli, ahol a hibajavítási programok a leggyakrabban elakadnak: adatvalidálás, XML-generálás és folyamat-kikényszerítés.

Az eszközkészlet strukturált címekre vonatkozó képességei az SR2026 követelményeihez igazodnak:

- **Generálás előtti validálás** a strukturált és hibrid postai címmezőkre, hogy a nem megfelelő adatok még bármely XML előállítása vagy elküldése előtt kiszűrődjenek.
- **A strukturálatlan címadatok megjelölése**, amelyek a 2026. novemberi határidő után elbuknának, egyértelmű megkülönböztetéssel a hibridként elfogadható és a teljesen strukturálatlan esetek között.
- **Kettős formátumtámogatás** mind a határidő előtti hibrid formátumokhoz, mind a határidő utáni teljesen strukturált elrendezésekhez, lehetővé téve az intézmények számára a fokozatos migrációt anélkül, hogy megtörnék az együttműködési képességet azokkal a partnerekkel, amelyek még nem fejezték be saját átállásukat.
- **CI-folyamatba integrálás**, hogy a címminőségi ellenőrzések a build folyamat részévé váljanak, ne pedig a folyamat végi utólagos megfontolássá, ami gyakorlati válasz a [CGI azon megfigyelésére, hogy az adatirányításnak alapvető tervezési elvnek kell lennie ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"), nem pedig megfelelési ráépülésnek.

A címeken túl az eszközkészlet lefedi azt a szélesebb validálási felületet, amelyet az SR2026 kiadás szigorít: JSON Schema validálás 20 üzenetspecifikus séma ellenében, IBAN-formátum és ellenőrzőösszeg-ellenőrzés 75 országban, a generált XML XSD-validálása a hivatalos [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) sémák ellenében, valamint verziótudatos generálás mind a 13 támogatott pacs.008 revízión (a pacs.008.001.01-től a pacs.008.001.13-ig). A működési és megfelelési csapatok számára tartalmaz továbbá XXE-megelőzést a defusedxml segítségével, szigorú útvonalbejárás elleni védelmet, valamint PII-maszkolást a strukturált JSON-naplókban a GDPR- és PCI DSS-követelmények támogatására, olyan kontrollokat, amelyek a produkciós fizetési folyamatokban nem képezik alku tárgyát, a szállítóvezérelt migrációkban azonban gyakran csak későn kerülnek utólag beépítésre.

A könyvtár elérhető [a PyPI-n ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") `pip install pacs008` csomagként, valamint a [GitHubon ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") teljes forráskódi átláthatósággal. Az intézmények számára, amelyek a lehetőségeiket mérlegelik, ez számít: a nyílt forráskódú eszközök lehetővé teszik a belső csapatok számára a validálási logika auditálását, annak integrálását a meglévő Python- vagy FastAPI-környezetekbe licencről szóló tárgyalások nélkül, valamint a javítások visszaküldését, ahogy saját peremeseteik felbukkannak.

Érdemes pontosnak lenni a hatókört illetően. A pacs008 üzenetréteg-eszközkészlet; nem helyettesíti a fizetési motort, a szűrőrendszert vagy azt az ügyfél-törzsadatok javítását, amelyet egy intézménynek továbbra is a forrásnál kell elvégeznie. Amit tesz, az az, hogy ezt a javítási munkát kikényszeríthetővé teszi, a strukturált címre vonatkozó megfelelést egy hosszú folyamat végén elvégzett kézi felülvizsgálatból a generálás pontján lévő automatizált kapuvá alakítva. Az idővel szűkösen álló programok számára ez a kapu a különbség a tiszta átállás és az átállás utáni elutasításhullám között.

## Az eszközök tájképe

A pacs008 az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) üzeneteszközök tágabb ökoszisztémáján belül helyezkedik el, és a megközelítés megválasztása az intézmény technológiai készletétől, méretétől és migrációs filozófiájától függ. A nyílt forráskódú és kereskedelmi tájkép magában foglalja a [pyiso20022-t ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (széles, több kategóriát átfogó Python-könyvtár béta validálással), a kapcsolódó [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") könyvtárat a feljebb elhelyezkedő fizetéskezdeményezéshez, a [Prowide ISO 20022-t ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (átfogó, Apache 2.0 licencű Java-könyvtár kereskedelmi réteggel a CBPR+ validáláshoz és fordításokhoz), valamint számos kereskedelmi platformot, köztük a Mambut, a Kyribát, a PaymentComponentst és másokat, amelyek az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) képességet szélesebb treasury- vagy fizetésiplatform-kínálatokba csomagolják.

A kompromisszum ismerős. A kereskedelmi platformok csökkentik a házon belüli mérnöki terhet, de az intézményt egy olyan szállítói ütemtervhez kötik, amely nem feltétlenül egyezik a sajátjával. Az átfogó, több kategóriát átfogó könyvtárak szélesebb felületet fednek le, de bármely egyetlen üzenettípushoz több integrációs munkát igényelnek. A fókuszált nyílt forráskódú könyvtárak, a pacs008 a pénzügyi intézmények közötti ügyfél-átutaláshoz, a [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) a fizetéskezdeményezéshez, minimálisra csökkentik az integrációs időt azon intézmények számára, amelyeknek gyorsan kell kezelniük konkrét szűk keresztmetszeteket, és az intézmény kezében hagyják a saját validálási szabályai feletti irányítást. Kifejezetten a strukturált cím problémája esetében a fókuszált megközelítés előnye, hogy a kikényszerített szabályok szűkek, jól meghatározottak, és valószínűtlen, hogy az átállás előtt megváltoznak.

## Mit jelent ez ágazatonként

A 2026. novemberi határidő nem érint minden intézményt egyformán. A helyes válasz a határokon átnyúló forgalom volumenétől, a meglévő adatvagyon érettségétől és attól függ, hogy az intézmény milyen szerepet tölt be a fizetési láncban.

### Nagy levelező- és határokon átnyúló bankok

A jelentős CBPR+ forgalmat bonyolító első vonalbeli bankok számára a strukturált címre vonatkozó követelmény csupán egy munkafolyamat egy sokkal nagyobb SR2026 felkészülési programon belül, amely kiterjed a kivételekre és vizsgálatokra, a BAH megerősítésére, valamint (az Egyesült Államokban) a Fedwire és a CHIPS egyidejű migrációjára is. A RedCompass Labs adatai arra utalnak, hogy ezen intézmények többsége 20-30 millió dollárt költ a 2026-os felkészülésre, 10-20 szakemberből álló megvalósítási csapatokkal. E csoport számára a kockázat nem a technikai képességben, hanem a megvalósítási kapacitásban rejlik. Mivel több párhuzamos munkafolyamat verseng ugyanazokért a kiadási ablakokért, a címminőség javítása csendben lemaradhat a láthatóbb munkafolyamatok mögött, amíg átállási heti problémává nem válik. A gyakorlati enyhítés a címvalidálás előrehozása a folyamatban, hogy a hibák hónapokkal azelőtt felszínre kerüljenek a fejlesztési és tesztkörnyezetekben, mielőtt elérnék a produkciót.

### Középszintű bankok és fizetési intézmények

A középszintű bankok és az EMI/PI intézmények számára a strukturált címre vonatkozó követelmény gyakran a legjelentősebb 2026-os kötelezettség, amellyel szembesülnek, mert nem viselik ugyanazt a kísérő munkafolyamat-terhet, mint az első vonalbeli intézmények. A kihívás itt általában a forrásoldali adatminőség. Azok az ügyfélbefogadó folyamatok, amelyek évtizedeken át szabad szövegként rögzítették a címeket, olyan törzsadat-vagyont eredményeznek, amely nem egyszerűen elemezhető. Az automatizált hibajavítás, a SWIFT nyílt forráskódú címstrukturáló modelljét, kereskedelmi címtisztító szolgáltatásokat vagy ezek kombinációját használva, a rekordok jelentős részét kezelheti, de a komplex nemzetközi címek maradék hosszú farka kézi felülvizsgálatot igényel. Minél korábban kezdődik ez a munka, annál kisebbé válik ez a farok.

### Vállalatok és fizetési szolgáltatók

A fizetéseket pain.001 útján kezdeményező vállalatok a bank pacs.008 generálásától feljebb helyezkednek el, de nem mentesülnek a strukturált címre vonatkozó követelmény alól. A bankok nem töltik ki visszamenőleg a kedvezményezett címeit a vállalati ügyfelek nevében; a strukturált adatoknak a vállalat saját rendszereiből kell származniuk. A vállalati treasury-vezetők számára ez azt jelenti, hogy biztosítaniuk kell, hogy az ERP- és treasury-rendszerek strukturált formában rögzítsék a kedvezményezett címeit, hogy az aláíróra és a végső adósra vonatkozó információ hasonlóképpen strukturált legyen, és hogy a fizetéskezdeményezési sablonok ne dobjanak el csendben mezőket a fájlgenerálás során. A pain.001 fájlok előzetes validálása, akár a vállalat saját eszközeit, akár a bank által kínált szolgáltatásokat használva, a gyakorlati ellenőrzési ponttá válik.

### Szállítók, fintechek és rendszerintegrátorok

A fizetési rendszerekre építő szállítók számára a határidő olyan kényszerítő tényező az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) képesség tekintetében, amelyet esetleg későbbi fázisokra halasztottak. Azoknak a fintecheknek, amelyek banki partnereken keresztül irányítanak vagy indítanak határokon átnyúló fizetéseket, meg kell jeleníteniük a strukturált cím rögzítését a saját felhasználói felületeiken és API-jaikban, vagy el kell fogadniuk, hogy az adataikból nem állítható elő megfelelő pain.001 fájl. A lehetőség a gyorsan mozogni képes szállítók számára az, hogy a javítási terhet a vállalati ügyfelek nevében vállalják magukra, egy megfelelési problémát szolgáltatássá alakítva.

## Következtetés

A 2026. novemberi strukturált címre vonatkozó határidő egyfelől szűk körű változás: két kötelező mező, néhány ajánlott mező, valamint egy olyan szabad szöveges lehetőség kivezetése, amelyet szankciórelevanciájú adatokhoz eleve soha nem lett volna szabad használni. Másfelől ez az eredeti CBPR+ migráció óta a működési szempontból legjelentősebb [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) mérföldkő, mert a strukturált adatokat nem csupán az üzenetrétegbe, hanem az azt tápláló, feljebb elhelyezkedő rendszerekbe is kényszeríti.

Az iparági szintű felkészültségi kép hat hónappal a határidő előtt nem biztató. A CBPR+ üzenetek kétharmada még mindig strukturálatlan címeket hordoz. A bankok közel fele nincs jó úton. Az ügyfélcím-nyilvántartások csaknem egyharmada elemezhetetlen marad. A finanszírozás rendelkezésre áll, a felmérések következetesen nyolc- és kilencjegyű befektetéseket mutatnak, de a munka nem, és a probléma adatminőségi dimenzióját önmagában a költekezéssel nem lehet megoldani az utolsó hónapokban.

Ami most segít, az a validálás pontján történő automatizálás: a szabályok betolása olyan folyamatokba, amelyek még azelőtt elkapják a problémákat, hogy azok elérnék a hálózatot, nem pedig utána. A Python- vagy FastAPI-környezeteket üzemeltető intézmények számára az olyan nyílt forráskódú eszközök, mint a [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"), gyakorlati módot kínálnak erre a váltásra egy szállítóválasztási ciklus nélkül. Mindenki számára, a technológiai készlettől függetlenül, a stratégiai lényeg ugyanaz: azok az intézmények, amelyek most iparosítják a változást, sokkal erősebb helyzetben lesznek, mint azok, amelyek az utolsó pillanatban történő megfelelésre támaszkodnak, hogy a 2026-os beszélgetés nagy részét keretbe foglaló RedCompass Labs kutatás megfogalmazását kölcsönözzem.

A novemberi átállási hétvége lezár egy fejezetet. Azok az intézmények, amelyek tiszta adatokkal, automatizált validálással és annak működő megértésével érkeznek meg, hogy a strukturált címek valójában mit tesznek a szankciószűrésért, azt a hétvégét a forgalom figyelésével töltik. Azok, amelyek ezek nélkül érkeznek meg, a telefonoknál töltik majd.

## Gyakran ismételt kérdések

**Pontosan mi változik a 2026. novemberi határidőkor?**

2026. november közepétől a SWIFT CBPR+ elutasítja azokat a pacs.008, pacs.009, pacs.004 és pacs.003 üzeneteket, amelyek félmezői kizárólag strukturálatlan postai címeket tartalmaznak. A minimális strukturált követelmény a Town Name a TwnNm elemben és a Country a Ctry elemben (az ISO 3166-1 alpha-2 kód használatával). A hibrid címek továbbra is megengedettek, a Town és a Country strukturált mezőkben, plusz legfeljebb két szabad szöveges AdrLine elem a fennmaradó összetevőkhöz, de ugyanaz az összetevő nem jelenhet meg egyszerre a strukturált és a strukturálatlan mezőkben. A teljesen strukturált címek a preferált formátum. Az European Payments Council a SEPA rendszereket (SCT, SDD, SCT Inst) ugyanahhoz az átállási dátumhoz igazította.

**Mely üzeneteket és mely félmezőket érinti?**

A pacs.008 esetében a követelmény az adós és a kedvezményezett postai címeire vonatkozik. A pacs.009 esetében az intézményi címekre vonatkozik a pénzügyi intézmények közötti átutalásokban és fedezeti fizetésekben. A pacs.004 esetében a felek címeire vonatkozik a fizetési visszautalásokban. A pacs.003 esetében a kedvezményezett és az adós címeire vonatkozik az ügyfélbeszedésekben. A kivonat- és értesítési üzenetek (camt.052, camt.053, camt.054), valamint bizonyos adminisztratív üzenetek a szigorú követelményen kívül maradnak. A vállalati ügyfelektől érkező, feljebb elhelyezkedő pain.001 üzeneteket nem közvetlenül a CBPR+ szabályozza, de a pain.001 fájlokban lévő strukturálatlan címek blokkolják a megfelelő pacs.008 generálását a folyamat lejjebbi részén, így gyakorlatilag a hatókörbe tartoznak.

**Mi a különbség a strukturált, a hibrid és a strukturálatlan címek között?**

A teljesen strukturált cím minden összetevőt a saját, kijelölt [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) elemére képez le: StrtNm, BldgNb vagy PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. A hibrid cím esetében a Town Name és a Country strukturált mezőkben van, a cím többi része pedig legfeljebb két szabad szöveges AdrLine elemben; ugyanaz az összetevő nem jelenhet meg mindkettőben. A strukturálatlan cím esetében a teljes postai cím AdrLine elemekben van, strukturált TwnNm vagy Ctry nélkül; ez az a formátum, amelyet 2026 novemberében kivezetnek az érintett félmezők esetében.

**Hogyan segít a pacs008.com ebben az átállásban?**

A [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") könyvtár az XML-generálás előtt validálja a strukturált és hibrid postai címmezőket, megjelöli a határidő után elbukó strukturálatlan adatokat, támogatja mind a határidő előtti hibrid, mind a határidő utáni teljesen strukturált formátumokat, és integrálódik a CI-folyamatokba és a kötegelt validálási munkafolyamatokba. XML-t generál mind a 13 támogatott pacs.008 verzióhoz, a hivatalos [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) XSD-sémák ellenében validál, és FastAPI-szolgáltatást kínál az automatizált vezényléshez. Nyílt forráskódú, MIT-jellegű licenc alatt, elérhető a PyPI-n, és kifejezetten a pénzügyi intézmények közötti ügyfél-átutalási munkafolyamatokhoz tervezték, így a validálási szabályok az SR2026 CBPR+ használati útmutatóihoz vannak kalibrálva, nem pedig sok üzenettípus között elvonatkoztatva.

**Mi történik, ha az intézményem nem áll készen 2026 novemberére?**

Az érintett félmezőkben strukturálatlan címeket tartalmazó üzeneteket az átállás után hálózati szinten elutasítják. Ez a gyakorlatban fizetési hibákat, megnövekedett kivételvolument, kézi javítási hullámokat és valószínű ügyfélhatást jelent. A SWIFT menet közbeni fordítási szolgáltatása néhány átmeneti esetben elérhető, de 2026 januárjától felárat von maga után, és nem tud megbízhatóan feldolgozni minden címformátumot. A SWIFT kiadott egy nyílt forráskódú, mesterséges intelligenciára épülő címstrukturáló modellt is, amely az örökölt strukturálatlan adatokból következtet a Town és a Country elemre, de ezt hibajavításra és előfeldolgozásra tervezték, nem pedig a tiszta forrásadatok tartós helyettesítésére. Azoknak az intézményeknek, amelyek javított ügyfél-törzsadatvagyon és automatizált validálási folyamat nélkül érkeznek meg a határidőhöz, nehéz átállási hétre és az azt követő hónapokban érdemi működési többletterhelésre kell számítaniuk.

## Hivatkozások

- Sebastien Rousseau, (2023). [Automating ISO 20022-Compliant Payment File Creation with Pain001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html "Automating ISO 20022-Compliant Payment File Creation with Pain001").
- pacs008, (2026). [November 2026 structured-address deadline ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"). pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 Toolkit and API ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"). pacs008.com.
- SWIFT, (2026). [ISO 20022 milestone for November 2026: Unstructured addresses to be removed ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"). SWIFT.
- SWIFT, (2026). [ISO 20022 for Financial Institutions ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions "ISO 20022 for Financial Institutions"). SWIFT.
- SWIFT, (2026). [The Swift AI address structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"). SWIFT.
- RedCompass Labs, (2026). [Nearly Half of Banks Are Behind on ISO 20022 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022"). Financial IT.
- RedCompass Labs, (2026). [ISO 20022 is arriving all at once for US banks ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). RedCompass Labs.
- ClearingPost, (2026). [The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline"). ClearingPost.
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 Migration: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 Migration: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale Banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- Standard Chartered, (2025). [ISO 20022 – Standard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "Standard Chartered ISO 20022 Address Guidelines"). Standard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.
