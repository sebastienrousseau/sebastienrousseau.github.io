---
title: "ISO 20022 a migráció után: fizetési adatokból banki termékek 2026-ban"
tags: "ISO 20022, structured address, CBPR+, payment data, reconciliation, sanctions screening, fraud detection, post-quantum cryptography, AI, tokenised deposits, cross-border payments"
subtitle: "Az ISO 20022 valódi nyereménye nem az üzenetmegfelelés. Hanem az, hogy a strukturált fizetési adatokat olyan banki termékké alakítjuk, amelyért az ügyfelek fizetnek, és amelyet az üzemeltetési csapatok automatizálni tudnak."
description: "Az ISO 20022 a migráció után adattermék-lehetőség. A strukturált címek, a jogcímkódok, a számlaadatok, a vizsgálati üzenetek és a gazdagabb fizetési státuszesemények egyeztetési, csalásfelderítési, likviditási, megfelelőségi és analitikai termékekké válhatnak."
date: "May 29, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/humphrey-muleba-1660004-1200.webp"
banner_alt: "ISO 20022 fizetésiadat-termék diagram, amely strukturált címeket, jogcímkódokat, egyeztetést, csalásfelderítést, likviditás-előrejelzést, szankciószűrést és analitikai termékeket ábrázol"
keywords: "ISO 20022 2026, strukturált cím, CBPR+, fizetésiadat-termékek, fizetési jogcímkódok, vállalati treasury, egyeztetés, szankciószűrés, csalásfelderítés"
---

## ISO 20022 a migráció után: fizetési adatokból banki termékek 2026-ban

Az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) a migráció után mérnöki munka, nem stratégia. A SWIFT MT / MX együttélése a határon átnyúló fizetéseknél 2025. november 22-én véget ért; az MT 103, az MT 202 és az MT 202COV határon átnyúló értékre már nem dolgozódik fel. A CHAPS 2023 júniusában fejezte be a migrációját; a T2 és a T2S 2023 márciusában migrált; a Fedwire Funds Service 2025 márciusában migrált; a CHIPS és a SIC igazodott. A 2026. novemberi pacs.008 strukturáltcím-előírás öt hónapra van, és a szabad formátumú `<AdrLine>` tartalom hosszú farka számos korridoron fennmarad. A 2026-os intézményi kérdés nem az, hogy elfogadják-e az ISO 20022-t (ez megtörtént), hanem az, hogy a bank back office-a natív MX-e, vagy egy fordítási réteg csendben lecsupaszítja-e a strukturált hasznos terhet, mielőtt az adat egyáltalán elérne egy termékcsapatot. ([SWIFT](https://www.swift.com/news-events/news/2025-iso-20022-progress "SWIFT 2025 ISO 20022 progress")).

---

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - **Az MT / MX együttélése lezárult.** A végső átállás 2025. november 22. A SWIFT FINplus ettől a naptól az egyetlen hálózati formátum a határon átnyúló készpénzforgalomra a hálózaton.
> - **Öt hónap a következő határidőig.** A CBPR+ 2. fázisa 2026 novemberétől strukturált `<PstlAdr>` komponenseket ír elő: `<StrtNm>`, `<TwnNm>`, `<Ctry>`, miközben az `<AdrLine>` új üzenetek esetén elavulttá válik.
> - **Natív MX, vagy nem migrált.** Az a bank, amely MX-ből belső kanonikus formátumba fordító réteget üzemeltet, amely elveszíti a `<RmtInf><Strd>`, `<Purp>`, `<UltmtDbtr>`, `<UltmtCdtr>`, `<LEI>` elemeket, megfelelő üzeneteket bocsát ki, de az értékből semmit sem fog meg. A munka a back office szintjén natív, nem az interfész szintjén.
> - **Az első adattermék a kevesebb vizsgálat.** A camt.027 / .028 / .029 / .087 üzenetek egy ügykezelő platformba kötve a teljesen MX-alapú korridorokon körülbelül 60%-kal csökkentették a határon átnyúló vizsgálatok átfutási idejét. A mérőszám az FTE-naponként lezárt vizsgálatok száma, nem valamiféle „elfogadási" mutató.
> - **A második a szankciós téves találatok csökkentése.** A strukturált `<Nm>`, `<PstlAdr>`, BIC, LEI, `<Othr>` a régi üzenetek minőségétől függően 15–40%-kal csökkenti az OFAC / OFSI / EU konszolidált listás téves találatokat az MT 103 szabad formátumú mezőihez képest.
> - **A harmadik a vállalati treasury-adat.** A pacs.008 `<RmtInf><Strd><RfrdDocAmt>`, `<CdtrRefInf>`, `<AddtlRmtInf>` elemei a pain.001 `<RmtId>` elemével együtt számlaszintű egyeztetést tesznek lehetővé. A vállalatok fizetnek ezért; a legtöbb bank ezt még nem csomagolta termékké.
> - **A SWIFT gpi immár ISO-natív.** Az UETR fennmarad; a tracker közvetlenül olvassa a pacs.002 / .004 / .028 üzeneteket. A treasury-ügyfélélmény attól függ, hogy az MX-natív feldolgozási lánc strukturált státuszeseményeket vagy általános visszaigazolásokat állít elő.
>
---

## Mi zárult le 2025 novemberében, és mi nem

A 2025. november 22-i határon átnyúló SWIFT-átállás nyugdíjazta az MT 103, MT 202, MT 202COV, MT 205 és MT 205COV üzeneteket az értékhordozó, határon átnyúló használatra. A SWIFT FINplus, az ISO 20022 MX-et hordozó, InterAct-alapú szolgáltatás lett az egyetlen útvonal ezekhez a folyamatokhoz. A CBPR+ 1. fázisa ugyanebben az időablakban vált kötelezővé. Az EKB-nál működő ESMIG-üzemeltető megerősítette a T2 és a T2S megfelelő migrációját; a [Bank of England CHAPS szolgáltatása ⧉](https://www.bankofengland.co.uk/payment-and-settlement/chaps "CHAPS, Bank of England") 2023 júniusában állt át a teljes MX-re; a Federal Reserve 2025 márciusában fejezte be a Fedwire Funds Service migrációját.

Ami nem zárult le:

- **A belföldi MT a nem határon átnyúló folyamatokhoz.** A nem SWIFT belföldi sémákhoz belső, MT-alakú üzeneteket futtató bankok tovább működnek. Az átállás egy SWIFT FIN határon átnyúló esemény, nem az MT globális nyugdíjazása.
- **Az MT üzenetküldés a kereskedelemfinanszírozásban.** Az MT 7XX (okmányos meghitelezések), az MT 4XX (beszedések), az MT 5XX (értékpapír-kereskedelem) egyelőre a FIN-en maradnak. Az ISO 20022 megfelelői (semt.*, tsmt.*) léteznek, de még nem tartoznak határon átnyúló előírás alá.
- **Az MT 9XX nostro-kivonatok a régi back office-okban.** Az MT 940 / 942 / 950 kivonatok számos levelezőtől tovább érkeznek; a camt.052 / camt.053 / camt.054 megfelelői elérhetők, de a régi nostro-egyeztetési folyamatok nem mind migráltak.
- **Az `<AdrLine>` tartalmú MX hosszú farka.** Az 1. fázis előírása elfogadta a hibrid, strukturált és nem strukturált címeket. A 2026. novemberi 2. fázis előírása nem.

A hálózati formátum megváltozása nem egyenlő az adatarchitektúra megváltozásával. Az a bank, amely a beérkező MX-et MT-alakú belső kanonikus formátumba fordítja, lecsupaszítja a `<RmtInf><Strd>`, `<Purp>`, `<UltmtDbtr>`, `<UltmtCdtr>`, `<LEI>`, `<UETR>` elemeket, mielőtt az adattárháza, a szankciómotorja, a csalásmotorja, az AML-motorja és az egyeztetési feldolgozási lánca látná az üzenetet. A hálózati formátum MX; az intézmény belsőleg elszegényített, MT-alakú adaton dolgozik. Szabályozói és kereskedelmi szempontból a migráció befejezetlen.

## A 2026. novemberi strukturáltcím-előírás

A CBPR+ 2. fázisa 2026 novemberétől előírja a `<PstlAdr>` strukturált formáját. A strukturált forma a következőket igényli:

```xml
<PstlAdr>
  <StrtNm>200 Aldersgate Street</StrtNm>
  <TwnNm>London</TwnNm>
  <PstCd>EC1A 4HD</PstCd>
  <Ctry>GB</Ctry>
</PstlAdr>
```

Az elavult, szabad formátumú alternatíva, a `<AdrLine>200 Aldersgate Street, London, EC1A 4HD</AdrLine>`, ma az 1. fázis alatt megengedett, de a 2. fázis átállásától új üzenetek esetén már nem elfogadható. A kötelező minimális tartalom a `<TwnNm>` és a `<Ctry>`; a `<StrtNm>` és a `<PstCd>` erősen ajánlott.

A bevezetés valósága a legtöbb első vonalbeli banknál 2026 közepén:

- **Kezdeményező oldal (adós adatai).** Az ügyfélnek szánt onboarding évek óta rögzíti a strukturált címmezőket. A bank ügyfél-törzsadata általában rendelkezik velük. A gond a leképezés az ügyfél-törzsadatról a `<DbtrAcct><Acct>` / `<Dbtr><PstlAdr>` mezőkre a HVPS+ vagy a CBPR+ használati útmutatói szerint.
- **Beérkező oldal (a kedvezményezett adatai a partnerüzeneteken).** Itt van a hosszú farok. A kedvezményezett adatait a kezdeményező bank állítja össze az ügyfele megbízásából. Azoknak a bankoknak, amelyek nagy volument kezelnek olyan korridorokból, ahol a kezdeményező bank még mindig `<AdrLine>` tartalmat bocsát ki, olyan gazdagító feldolgozási láncra van szükségük, amely a szabad formátumot strukturálttá alakítja a downstream felhasználáshoz, majd egy stratégiára, hogy mit tegyenek azokkal az üzenetekkel, amelyek nem felelnek meg a 2026. novemberi határidőnek.
- **A CBPR+ piaci gyakorlati útmutató.** A [SWIFT CBPR+ használati útmutatói ⧉](https://www2.swift.com/mystandards/CBPR+/ "SWIFT MyStandards CBPR+") a mérvadó forrás. A HVPS+ útmutató (a központi bankok által használt, nagy értékű fizetési rendszerek) ugyanazt a strukturáltcím-mintát követi, kissé eltérő kötelező mezőkkel.

A következő öt hónap mérnöki teljesítménye: strukturáltcím-gazdagító feldolgozási lánc a beérkező MX-interfészen, kemény hibás validáció a kimenő interfészen minden olyan cím esetén, amely nem éri el a 2. fázis kötelező minimumát, és kivételkezelő sor azoknak a korridoroknak, amelyek a határidő után is nem megfelelő üzeneteket bocsátanak ki.

## Az adattermékek, amelyeket a bankok ténylegesen felépíthetnek

A pacs.008 boríték sokkal több strukturált adatot hordoz, mint az MT 103. A termék-lehetőség három konkrét mezőn nyugszik.

### Strukturált közlemény: `<RmtInf><Strd>`

A szabad formátumú közlemény, a `<RmtInf><Ustrd>`, olyan összevont szöveg, amely a vállalati oldalon végül OCR-jellegű elemzést igényel. A strukturált közlemény, a `<RmtInf><Strd>`, a következőket hordozza: `<RfrdDocInf>` (számlahivatkozások típussal, számmal, kiállítási dátummal, összeggel), `<CdtrRefInf>` (egyetlen jogosulti hivatkozás típussal), `<RfrdDocAmt>` (a dokumentumösszegek felbontása), `<AddtlRmtInf>` (további szabad szöveg, legfeljebb négy előfordulásban). A vállalati treasury-egyeztetés szempontjából ez az a mező, amely bevételt termel.

A termék: számlaszintű automatizált egyeztetés treasury-szolgáltatásként. A vállalat követeléskezelő (AR) rendszere a beérkező fizetéseket konkrét számlákhoz egyezteti kézi párosítás nélkül. Azok a bankok, amelyek ezt hozzáadott értékű szolgáltatásként árazzák a nagy számlavolumenű vállalatoknak, a volumen szintjétől függően a fizetési érték 0,5 és 3 bázispontja között tudtak díjat felszámítani.

### Jogcímkódok: `<Purp>`

A `<Purp><Cd>` mező az ISO 20022 ExternalPurpose1Code kódot hordozza: SALA (fizetés), DIVI (osztalék), GOVT (kormányzati kifizetés), INTC (vállalaton belüli), CASH (készpénzgazdálkodás), GDDS (áruvásárlás), SCVE (szolgáltatásvásárlás), TRAD (kereskedelmi kiegyenlítés) és további körülbelül 280 kód, amelyeket az ISO tart karban. A szabad szöveges alternatívák a `<Purp><Prtry>` elemben találhatók.

A termékfelület szélesebb, mint az egyeztetés:

- **Szankciós és AML kockázatpontozás.** A jogcímkódok strukturált szándékadattal táplálják a tranzakciófigyelő modelleket, amit az MT 103 szabad formátuma nélkülözött. Egy `<Purp><Cd>TRAD</Purp>` tartalmú pacs.008 egy olyan korridoron és partnernél, ahol a bank kockázati modellje csak `<Purp><Cd>SALA</Purp>` értéket vár, magasabb szintű felülvizsgálatot vált ki.
- **Likviditás-előrejelzés.** A treasury-menedzsment napon belüli részletességgel tudja előrevetíteni a likviditást, ha a fizetéseket jogcímkód szerint, nem pusztán partner szerint aggregálja. A SALA és a DIVI folyamatok időzítési kiszámíthatósága eltér a TRAD vagy a CASH folyamatokétól.
- **Adózási és jelentési kategorizálás.** A jogcímkódok számos adóügyi jelentési kategóriára képezhetők le, külön gazdagítási lépés nélkül.

### Félazonosítók: `<UltmtDbtr>`, `<UltmtCdtr>`, `<LEI>`, `<BIC>`

A pacs.008 a közvetlen adóstól / jogosulttól elkülönítve hordozza a végső adóst és jogosultat, ami akkor számít, amikor a fizetések közvetítettek. A `<FinInstnId>` alatti `<LEI>` elem a Legal Entity Identifier azonosítót hordozza, ha jelen van.

A termék: fejlett szankciószűrés strukturált féladatokkal. Az OFAC, az OFSI és az EU konszolidált listás szűrés téves találatai érdemben csökkennek, ha a szűrőmotor strukturált `<Nm>`, `<PstlAdr>` (strukturált), `<Id><OrgId><LEI>`, `<Id><OrgId><Othr>` elemeket lát a szabad szöveges mezők helyett. A G-SIB szankciószűrő csapatok 2025-ös bevezetési adatai, amelyeket a SIBOS-on és különböző kockázattechnológiai konferenciákon tettek közzé, 15–40%-os téves találat csökkenést mutatnak a forrás MT 103 régi minőségétől függően.

### Vizsgálati üzenetek

A camt.027 (nem érkezett meg reklamáció), a camt.028 (kiegészítő információ), a camt.029 (vizsgálat lezárása), a camt.087 (módosítási kérelem) leváltja az MT 192 / 195 / 196 / 199 párbeszédet. A strukturált szemantika, azaz lekérdezés, válasz, lezárás, a vizsgálati sort hosszú szöveges osztályozási folyamatból munkafolyamattá alakítja.

A termék működési, nem kereskedelmi: a régi MT-korridorokon 5–7 napban mért határon átnyúló vizsgálati átfutási idő 48 óra alá csökken a teljesen MX-alapú korridorokon, ha a camt.* üzeneteket egy ügykezelő platformba kötik. A megtérülés az az üzemeltetési FTE, amelyet a banknak nem kell felvennie, ahogy a volumenek nőnek.

## Mérnöki minta: natív MX kontra fordítási réteg

A legtöbb első vonalbeli bank a három migrációs minta egyikét választotta. A migráció utáni adattermék-képességük közvetlenül ebből a választásból következik.

### A minta: fordítás a vezetéken, régi kanonikus formátum belül

MX befelé, a gateway-en MT-alakú kanonikus formátumba fordítva, meglévő rendszerek dolgozzák fel, majd kifelé vissza MX-be fordítva. A legegyszerűbb, a legkisebb fennakadással. **Kompromisszum:** a back office adattárháza, az AML-motor, a csalásmotor, a szankciómotor és az egyeztetési feldolgozási lánc mind MT-alakú adatot lát. A bank megfelelő MX-et bocsát ki, de a strukturált adat értékéből semmit sem fog meg. A vizsgálati sorok, a szankciós téves találatok és az egyeztetési ráfordítás mind az MT-korszak szintjén marad. A legtöbb megfigyelő arra számít, hogy az A minta szerinti bankok 2026 és 2028 között a back office munkájának második hullámába kezdenek, hogy hozzáférjenek a strukturált hasznos teherhez.

### B minta: MX-re tervezett belső kanonikus formátum

MX befelé, egy belső kanonikus formátumba fordítva, amely megőrzi a strukturált közleményt, a jogcímkódokat, a végső fél adatait, a strukturált címeket és a vizsgálati üzeneteket. A szankciómotor, az AML-motor és az egyeztetési feldolgozási lánc felújítva a strukturált adat feldolgozására. **Kompromisszum:** magasabb megvalósítási költség, hosszabb program. **Előny:** a fent leírt adattermékek elérhetők a back office munkájának második hulláma nélkül.

### C minta: végponttól végpontig natív MX

A hálózati formátumú MX változatlanul áramlik a back office-ba és az adattárházba. A bank belső adatmodellje közvetlenül leképeződik az ISO 20022 elemekre. **Kompromisszum:** a legnagyobb fennakadás a régi rendszereknél; néhány alapbanki platform ezt csak a következő nagyobb kiadásáig tudja elfogadni. **Előny:** a legkisebb súrlódású út az adattermékek bevételtermeléséhez, és a legtisztább pozíció a 2026. novemberi strukturáltcím-előíráshoz, a jövőbeli CBPR+ fázisokhoz és a még MT-n lévő belföldi sémák idővel bekövetkező migrációjához.

A helyes minta a bank alapplatformjától, program-étvágyától és a strukturált adat termékeivel szembeni kitettségétől függ. A rossz kimenet az, ha alapértelmezésként az A mintát választják, majd 2026 második felében rájönnek, hogy a strukturáltcím-előírás, a gpi-tracker integráció és a vállalati treasury termék-ütemterv mindegyike olyan back office változást igényel, amely nem szerepelt az eredeti program hatókörében.

## Mit jelent ez banktípusonként

### Globálisan rendszerszinten jelentős bankok

A CBPR+ 1. fázis átállása mögöttük van. A 2026. novemberi strukturáltcím-átállás az azonnali prioritás, a strukturált hasznos terhet bevétellé alakító adattermék-program pedig a középtávú prioritás. Előbb építsék meg a strukturáltcím-gazdagító feldolgozási láncot: a határidő kemény. Ezután ütemezzék a szankciós téves találatok csökkentését és a vállalati treasury egyeztetési termékeket az üzemeltetési irányítópulton már meglévő MT-korszakbeli alapértékekhez képest.

### Tranzakciós és levelező bankok

A versenynyomás éles. A 2026-ban levelező partnereket értékelő vállalatok és válaszadó bankok szolgáltatásjellemzőkként kérdeznek a gpi tracker strukturált státuszeseményeiről, a vizsgálati átfutási időkről és a számlaszintű egyeztetésről. Az A mintát futtató bankok (fordítás a vezetéken, régi kanonikus formátum belül) kevésbé versenyképesen válaszolnak ezekre a kérdésekre, mint a B vagy C minta szerinti bankok. A 2026 második felére szóló termék-ütemterv kérdése az, hogy elkötelezik-e magukat a B minta szerinti back office fejlesztés mellett, vagy elfogadják a lemorzsolódást a felső szegmensben.

### Regionális és középszintű bankok

A helyes stratégia az MX gazdagságának fogyasztása, nem pedig natív előállítása. Válasszanak olyan fizetésiüzenet-platform szállítót, amelynek belső kanonikus formátuma megőrzi a strukturált hasznos terhet, ellenőrizzék a szállító CBPR+ 2. fázisra való felkészültségét, és az adattermékeket szállító által üzemeltetett szolgáltatásként integrálják ahelyett, hogy házon belül építenék meg őket. Kifejezetten a vállalati treasury egyeztetési termék alkalmas white-label platformbeszerzésre.

### Vállalati treasurerek és PSP-k

A banknak felteendő kérdés egyértelmű: „Képes-e a platformjuk strukturált közlemény szerinti egyeztetést nyújtani számlaszintű adatok alapján, és mit nyújt a gpi tracker a számlánkra beérkező fizetéseknél?" Az a bank, amely strukturált adat termékjellemzőkkel válaszol, a B vagy a C mintán van; az a bank, amely azt válaszolja, hogy „CBPR+ megfelelők vagyunk", valószínűleg nincs.

## Következtetés

Az ISO 20022 a migráció után nem lezárási téma. A hálózati formátum változása 2025 novemberében lezárult; az adatarchitektúra változása többnyire még előttünk áll. A 2026. novemberi strukturáltcím-előírás olyan back office képességet kényszerít ki, amelyet sok A minta szerinti bank elhalasztott. Az adattermék-lehetőségek, azaz a vizsgálati átfutási idő csökkentése, a szankciós téves találatok csökkentése, a vállalati számlaszintű egyeztetés és a gpi tracker strukturált státusza, csak akkor teljesülnek, ha a strukturált hasznos teher végponttól végpontig fennmarad.

Azok az intézmények, amelyek 2027-ben hitelesnek tűnnek a vállalati ügyfelek szemében, azok, amelyek 2026 során leváltak az A mintáról, befejezték a 2. fázis strukturáltcím-mérnökségét, és a strukturált közlemény termékét egy megfogalmazott ügyfélelőnyhöz kötve csomagolták. Azok az intézmények, amelyek nem, továbbra is levelező-banki korszakbeli díjakat számítanak fel egy MT-korszakbeli szolgáltatásért egy MX-vezetéken.

Mérjék a migrációt úgy, ahogy bármely működési programot mérnek: FTE-naponként lezárt vizsgálatok, szankciós téves találatok aránya, strukturáltcím-lefedettség a kimenetnél, strukturált közlemény kitöltöttsége a bemenetnél, gpi tracker strukturáltesemény-teljesítési aránya. A megfelelőségi mérőszámok nem a migráció; a működési mérőszámok azok.

## Gyakran ismételt kérdések

**Mi ért véget 2025. november 22-én?**

Az MT 103, az MT 202, az MT 202COV, az MT 205 és az MT 205COV a határon átnyúló értékfolyamatokra a SWIFT FIN szolgáltatásban. Ettől a naptól a SWIFT-en minden határon átnyúló készpénzüzenet a FINplus-on fut, amely az ISO 20022 MX-et hordozza a CBPR+ 1. fázis használati útmutatója szerint. A belföldi MT-használat, az MT 7XX kereskedelemfinanszírozási üzenetküldés és az MT 9XX nostro-kivonatok kívül estek ennek az átállásnak a hatókörén.

**Mi a 2026. novemberi határidő?**

A CBPR+ 2. fázisa előírja a `<PstlAdr>` strukturált formáját, azaz a `<StrtNm>`, `<TwnNm>`, `<Ctry>` elemeket, miközben az `<AdrLine>` új üzenetek esetén elavulttá válik. A kötelező minimális tartalom a `<TwnNm>` és a `<Ctry>`. A határidő a SWIFT-hálózaton keresztül határon átnyúló értékre küldött üzenetekre vonatkozik.

**„Migrált-e" egy bank, ha a back office-a MT-alakú belső kanonikus formátumon fut?**

A hálózati formátum migrált; az adatarchitektúra nem. A bank megfelelő MX-et küld és megfelelő MX-et fogad, de a strukturált hasznos teher lecsupaszításra kerül, mielőtt az adattárház, az AML-motor, a csalásmotor, a szankciómotor és az egyeztetési feldolgozási lánc látná. Szabályozói szempontból a migráció befejezett; kereskedelmi szempontból nem.

**Mi a legnagyobb adattermék-lehetőség?**

A vállalatoknak: számlaszintű egyeztetés strukturált közlemény alapján. Magának a banknak: szankciós téves találatok csökkentése (15–40% a régi minőségtől függően) és a vizsgálati átfutási idő csökkentése (5–7 napról 48 óra alá a teljesen MX-alapú korridorokon). A vizsgálati csökkentés működési megtérülés a meglévő volumenen; a szankciós csökkentés működési megtérülés plusz szabályozói pozicionálás; a vállalati egyeztetési termék új díjbevétel.

**Alkalmazandó-e még a SWIFT gpi?**

Igen. Az UETR fennmarad; a gpi tracker közvetlenül olvassa a pacs.002, pacs.004 és pacs.028 üzeneteket. A gpi treasury-ügyfélélménye, azaz a végponttól végpontig terjedő láthatóság strukturált státuszeseményekkel, attól függ, hogy a bank MX-natív feldolgozási lánca strukturált státuszeseményeket állít-e elő általános visszaigazolások helyett.

## Hivatkozások

- SWIFT, (2025). [2025 ISO 20022 előrehaladás ⧉](https://www.swift.com/news-events/news/2025-iso-20022-progress "SWIFT 2025 előrehaladás").
- SWIFT, (2025). [CBPR+ használati útmutatók a MyStandards oldalon ⧉](https://www2.swift.com/mystandards/CBPR+/ "MyStandards CBPR+").
- Bank of England, (2023). [CHAPS, Bank of England ⧉](https://www.bankofengland.co.uk/payment-and-settlement/chaps "CHAPS").
- European Central Bank, (2023). [TARGET Services konszolidáció ⧉](https://www.ecb.europa.eu/paym/target/consolidation/html/index.en.html "T2 / T2S konszolidáció").
- Federal Reserve, (2025). [Fedwire Funds Service ISO 20022 bevezetés ⧉](https://www.frbservices.org/resources/financial-services/wires/iso-20022-implementation-center "Fedwire ISO 20022").
- ISO, (2024). [ISO 20022 üzenetkatalógus ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 üzenetdefiníciók").
