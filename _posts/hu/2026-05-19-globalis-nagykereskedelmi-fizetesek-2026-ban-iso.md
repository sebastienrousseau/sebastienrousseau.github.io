---
title: "Globális nagykereskedelmi fizetések 2026-ban: ISO 20022, RTGS-megújítás és az interoperabilitás gazdaságtana"
tags: "wholesale payments, ISO 20022, RTGS, cross-border payments, BIS, CPMI, FSB, SWIFT, CBPR+, G20 roadmap, payment interoperability, correspondent banking, wholesale CBDC, DLT settlement, DORA, post-quantum cryptography, AI, stablecoins, tokenised deposits, cloud native banking"
subtitle: "A nagykereskedelmi fizetések gazdaságpolitikai eszközzé váltak: az ISO 20022, az RTGS üzemidő, a nem banki hozzáférés, az összekapcsolás, a DLT-elszámolási kísérletek és a G20 ütemterv a globális likviditásmozgás költsége köré rendeződnek."
description: "A globális nagykereskedelmi fizetéseket 2026-ban az ISO 20022 harmonizációja, az RTGS-megújítás, a kiterjesztett elszámolási ablakok, a nem banki hozzáférés, az API-irányítás, a DLT-kísérletek és a határon átnyúló fizetések fragmentációja alakítja át. A gazdasági kérdés az interoperabilitás, nem pusztán az üzenetküldés."
date: "May 19, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/miguel-sousa-ejIF-pJhYkM.webp"
banner_alt: "A globális nagykereskedelmi fizetések 2026-os architektúratérképe, amely bemutatja az ISO 20022-t, az RTGS-megújítást, a határon átnyúló folyosókat, a likviditási ablakokat és a DLT-elszámolási kísérleteket"
keywords: "nagykereskedelmi fizetések 2026, globális fizetési gazdaságtan, ISO 20022, RTGS, határon átnyúló fizetések, BIS CPMI, FSB, Swift CBPR+, G20 ütemterv, valós idejű bruttó elszámolás, Project Agora, Project Mandala, Project Nexus, fizetési interoperabilitás, levelező banki tevékenység, fizetési fragmentáció, nagykereskedelmi CBDC"
---

## Globális nagykereskedelmi fizetések 2026-ban: ISO 20022, RTGS-megújítás és az interoperabilitás gazdaságtana

A nagykereskedelmi fizetések 2026-ban már nem pusztán banki alapinfrastruktúrát jelentenek. Részei a makrogazdasági ellenállóképességnek, a kereskedelmi versenyképességnek, a likviditási hatékonyságnak, a szankciós megfelelésnek és a fizetési rendszerek fragmentációjáért folytatott stratégiai versengésnek. A BIS CPMI amellett érvel, hogy a harmonizált [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) bevezetés csökkentheti a régóta fennálló, határon átnyúló fizetési súrlódásokat a strukturált adatok, a jobb straight-through feldolgozás és az erősebb megfelelési szűrés révén ([BIS CPMI](https://www.bis.org/cpmi/publ/brief11.htm "The future of financial messaging: navigating the ISO 20022 migration journey")).

---

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - **Az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) mostanra a nagykereskedelmi fizetési modernizáció közös nyelvévé vált.** A BIS CPMI szerint a szabvány kezeli a fragmentált üzenetküldést, az adatcsonkolást, a gyenge straight-through feldolgozást és a megfelelési súrlódást ([BIS CPMI](https://www.bis.org/cpmi/publ/brief11.htm "The future of financial messaging: navigating the ISO 20022 migration journey")).
> - **A G20 ütemterv továbbra is elmarad a céloktól.** Az FSB 2026 márciusi frissítése szerint a haladás valós, de a 2027-es célok még nincsenek jó úton ([FSB](https://www.fsb.org/2026/03/reforming-cross-border-payments-keynote-speech-at-the-fsb-payments-summit/ "Reforming cross-border payments")).
> - **Az RTGS üzemideje és hozzáférése gazdasági eszközök.** Az FSB megjegyzi, hogy a joghatóságok több mint fele kiterjesztette az RTGS üzemidejét vagy tervezi a kiterjesztést, miközben a nem banki szolgáltatók közvetlen hozzáférése növekszik a fizetési rendszerekben ([FSB](https://www.fsb.org/2026/03/reforming-cross-border-payments-keynote-speech-at-the-fsb-payments-summit/ "Reforming cross-border payments")).
> - **A Bank of England megújított RTGS-szolgáltatása kifejezetten középpontba állítja az ellenállóképességet és az interoperabilitást.** A megújított szolgáltatást úgy tervezték, hogy az ellenállóképesség, a hozzáférés, az interoperabilitás és a funkcionalitás révén támogassa a monetáris és pénzügyi stabilitást ([Bank of England](https://www.bankofengland.co.uk/payment-and-settlement/rtgs-renewal-programme/the-renewed-rtgs-service-key-benefits "The renewed RTGS service — key benefits")).
> - **A fragmentáció a makrokockázat.** Az Atlantic Council figyelmeztet, hogy a fizetési rendszerek fragmentációja növelheti a költségeket, lassíthatja az elszámolást, csökkentheti az átláthatóságot és gyengítheti a globális pénzügyi integrációt ([Atlantic Council](https://www.atlanticcouncil.org/in-depth-research-reports/issue-brief/global-payment-systems-are-fragmenting-heres-what-the-g20-can-do/ "Global payment systems are fragmenting")).
> - **A DLT-kísérletek mostanra infrastruktúra-kísérletek, nem kriptoszínház.** A BIS-hez köthető munka, például a Project Agorá és az európai nagykereskedelmi elszámolási kísérletek azt vizsgálják, hogy a tokenizált kereskedelmi banki pénz és a jegybankpénz javíthatja-e a nagy értékű, határon átnyúló elszámolást ([Atlantic Council](https://www.atlanticcouncil.org/in-depth-research-reports/issue-brief/global-payment-systems-are-fragmenting-heres-what-the-g20-can-do/ "Global payment systems are fragmenting")).
> - **A gazdaságtan operatív.** Egy határon átnyúló fizetés gazdaságilag akkor bukik el, ha a gazdag adatok elvesznek, a megfelelési ellenőrzések manuálissá válnak, a likviditást az időzónák csapdába ejtik, és a vizsgálatok emberi javítást igényelnek.
>
---

## Miért gazdasági történet a nagykereskedelmi fizetés

A határon átnyúló nagykereskedelmi fizetések a kereskedelemfinanszírozás, a levelező banki tevékenység, az értékpapír-elszámolás, a vállalati treasury és a jegybanki műveletek alatt húzódnak meg. Amikor lassúak vagy átláthatatlanok, a forgótőke csapdába esik. Amikor fragmentáltak, a likviditási pufferek nőnek. Amikor a megfelelési adatok gyengék, a szankciós és pénzmosás elleni ellenőrzések drága manuális munkává válnak.

A BIS CPMI 2026 áprilisi tájékoztatója az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) szabványt úgy írja le, mint az adatobjektumok, szabályok és folyamatok szabványosításának módját a fizetések, az értékpapírok és a treasury területén, ami lehetővé teszi az interoperabilitást a pénzügyi intézmények, a piaci infrastruktúrák és a végfelhasználók között ([BIS CPMI](https://www.bis.org/cpmi/publ/brief11.htm "The future of financial messaging: navigating the ISO 20022 migration journey")). Ezért gazdaságilag lényeges a migráció, nem pusztán technikai jellegű.

## A 2026-os nagykereskedelmi fizetési kiindulópont

### 1. Az ISO 20022 a migrációtól a harmonizáció felé mozdul

Az első fázis az volt, hogy a fizetési rendszereket az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) szabványra állítsák. A második fázis az, hogy a bevezetés elég következetes legyen ahhoz, hogy az előnyök határokon átívelve is fennmaradjanak. A BIS CPMI a strukturált adatokat, a csökkentett csonkolást, a jobb szűrést és a javított egyeztetést azonosítja a harmonizált bevezetés alapvető előnyeiként ([BIS CPMI](https://www.bis.org/cpmi/publ/brief11.htm "The future of financial messaging: navigating the ISO 20022 migration journey")).

A nehézség abban rejlik, hogy az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) továbbra is fragmentálódhat, ha a joghatóságok eltérő mezőhasználati gyakorlatot, validációs szabályokat és opcionális adatkonvenciókat vezetnek be. A bankok stratégiai feladata ezért nem pusztán a formátumátalakítás, hanem a szemantikai összehangolás.

### 2. Az RTGS-megújítás kiterjeszti az elszámolási ablakot

Az elszámolási ablak azért számít, mert a globális nagykereskedelmi fizetések átlépik az időzónákat. Fabio Panetta 2026 májusi BIS-beszéde a nemzeti fizetési infrastruktúrát a reform egyik koordinátájaként keretezi, ideértve a szélesebb elszámolási ablakokat és a teljes [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) bevezetést ([BIS](https://www.bis.org/cpmi/speeches/sp260505.pdf "Interconnect to stabilize: cross-border payments in a fragmenting world")).

A Bank of England megújított RTGS-szolgáltatása ugyanebbe az irányba mutat. Hangsúlyozza az ellenállóképességet, a szélesebb hozzáférést, az interoperabilitást és egy szinkronizált elszámolási felületet, amely más főkönyvekkel is együttműködhet, és csökkentheti az elszámolási kockázatot és a likviditási költségeket ([Bank of England](https://www.bankofengland.co.uk/payment-and-settlement/rtgs-renewal-programme/the-renewed-rtgs-service-key-benefits "The renewed RTGS service — key benefits")).

### 3. A nem banki hozzáférés megváltoztatja a versenystruktúrát

A fizetési rendszerek szélesítik a közvetlen hozzáférést a nem banki fizetési szolgáltatók számára. A BIS 2026 májusi beszéde szerint a nem banki fizetési szolgáltatók közvetlen hozzáférése a 2025-ös adatok alapján a gyorsfizetési rendszerekben elérte a 45%-ot, az RTGS-rendszerekben pedig a 39%-ot ([BIS](https://www.bis.org/cpmi/speeches/sp260505.pdf "Interconnect to stabilize: cross-border payments in a fragmenting world")).

Ez azért fontos, mert a nem banki hozzáférés megváltoztatja a levelező banki tevékenység gazdaságtanát. Csökkentheti a hosszú levelező láncoktól való függőséget, de következetes szabályozást, likviditási kontrollt, elszámolási kockázati irányítást és működési ellenállóképességi normákat is igényel.

### 4. Az összekapcsolás lesz a párhuzamos rendszerek alternatívája

Az FSB megjegyzi, hogy az ázsiai-csendes-óceáni kezdeményezések felgyorsították a gyorsfizetési összekapcsolást, és hogy az összekapcsolási megállapodások mintegy 17 kétoldalú folyosót fednek le, továbbiakat tervezve ([FSB](https://www.fsb.org/2026/03/reforming-cross-border-payments-keynote-speech-at-the-fsb-payments-summit/ "Reforming cross-border payments")). A nagykereskedelmi fizetések esetében az ezzel egyenértékű kérdés az, hogy az RTGS-rendszerek, a jegybankpénz, a tokenizált főkönyvek és a levelező banki rendszerek hogyan működnek együtt anélkül, hogy új silókat hoznának létre.

Az összekapcsolás azért vonzó, mert megőrzi a hazai fizetési rendszer szuverenitását, miközben lehetővé teszi a határon átnyúló elérést. A kockázat az, hogy minden folyosó egyedi mérnöki és jogi projektté válik.

## A megszüntetendő gazdasági súrlódások

### Adatjavítás

A rosszul strukturált adatok fizetési vizsgálatokat, hamis szankciós találatokat, egyeztetési késéseket és manuális megkereséseket okoznak. Panetta 2026 májusi beszéde szerint a fizetések 1-3%-a generál megkereséseket, és a harmonizált ISO 20022 akár 80%-kal csökkentheti a megkeresések megoldási idejét ([BIS](https://www.bis.org/cpmi/speeches/sp260505.pdf "Interconnect to stabilize: cross-border payments in a fragmenting world")).

Ez nem háttérirodai optimalizálás. Ez likviditási és ügyfélélmény-javulás rendszerszintű léptékben.

### Likviditási fragmentáció

A határon átnyúló fizetések akkor fragmentálják a likviditást, amikor az elszámolási ablakok nem fedik egymást, amikor a rendszerek több joghatóságban is előfinanszírozást igényelnek, vagy amikor az elszámolási eszközök eltérnek. Az RTGS üzemidő kiterjesztése csökkenti ezt a problémát azáltal, hogy növeli azt az átfedést, amelyben a jegybankpénz elszámolhatja a tranzakciókat.

A stratégiai végpont nem a mindenhol, holnaptól folyamatosan működő RTGS. A reális végpont a kritikus ablakok célzott kiterjesztése, a jobb likviditási elemzés és az elszámolási szinkronizáció ott, ahol a gazdasági haszon a legnagyobb.

### Szabályozási átfedés

A határon átnyúló fizetések különböző pénzmosás elleni, szankciós, adatvédelmi és adatmegosztási rendszereken haladnak át. Az FSB kiemeli az adatkeretrendszerekkel, a banki és nem banki szabályozással, a FATF-szabványokkal és a határon átnyúló fizetési csalásokkal kapcsolatos munkát a reformmenetrend részeként ([FSB](https://www.fsb.org/2026/03/reforming-cross-border-payments-keynote-speech-at-the-fsb-payments-summit/ "Reforming cross-border payments")).

A technológia nem tudja megszüntetni ezeket a kötelezettségeket. Csak korábbivá, gazdagabbá és kevésbé manuálissá teheti a megfelelési ellenőrzéseket.

## Architektúratáblázat: a nagykereskedelmi fizetések modernizációja

| Réteg | 2026-os irány | Gazdasági hatás | Kockázat rossz megvalósítás esetén |
|---|---|---|---|
| **Üzenetküldés** | ISO 20022 harmonizáció | Jobb STP, szűrés, egyeztetés | Fragmentált mezőhasználat és adatcsonkolás |
| **Elszámolás** | Megújított RTGS és szélesebb üzemidő | Alacsonyabb likviditási pufferek és gyorsabb véglegesség | Működési terhelés és egyenetlen időzónai lefedettség |
| **Hozzáférés** | Több nem banki fizetési szolgáltatói hozzáférés | Verseny és rövidebb fizetési láncok | Egyenetlen felügyelet és elszámolási kockázat kiszivárgása |
| **Összekapcsolás** | Két- és többoldalú kapcsolatok | Elérés a hazai rendszerek újjáépítése nélkül | Folyosóspecifikus fragmentáció |
| **DLT / tokenizáció** | Nagykereskedelmi elszámolási kísérletek | Programozhatóság és atomi elszámolás | Jogi véglegesség és interoperabilitási hiányosságok |
| **Irányítás** | FSB, CPMI, FATF koordináció | Következetes globális működési modell | Megfelelési átfedés és geopolitikai eltérés |

## Mit jelent ez intézménytípusonként

### Globális tranzakciós bankok

A prioritás az, hogy az ISO 20022 adatokat termékképességgé tegyék, ne pedig megfelelési átalakítássá. A legerősebb tranzakciós bankok a strukturált adatokat az egyeztetés, a készpénz-előrejelzés, a szankciós előzetes validáció, a vizsgálatok és az ügyfél-treasury irányítópultok javítására fogják használni.

### Jegybankok és piaci infrastruktúrák

A prioritás az, hogy kiterjesszék az üzemidőt ott, ahol a likviditási haszon egyértelmű, biztonságosan szélesítsék a hozzáférést, és igazodjanak a globális adatkövetelményekhez. Az RTGS-megújítás mostanra stratégiai nemzeti infrastruktúra-program, nem háttérirodai csere.

### Vállalatok és treasury csapatok

A prioritás az átláthatóság. A treasury szakembereknek strukturált fizetési állapotjelentést, jobb elutasítási elemzést, gazdagabb átutalási adatokat és olyan API-kat kell kérniük a bankoktól, amelyek az ISO 20022-t forgótőke-intelligenciává alakítják.

### Fintechek és fizetési szolgáltatók

A prioritás a hozzáférés és a megfelelési mélység együtt. Az elszámolási rendszerekhez való közvetlen vagy közvetett hozzáférés csak akkor értékes, ha a fizetési szolgáltató képes teljesíteni a bankszintű ellenállóképességi, pénzmosás elleni, szankciós, likviditási és incidensjelentési elvárásokat.

## Következtetés

A globális nagykereskedelmi fizetések története 2026-ban az interoperabilitás története. Az ISO 20022 biztosítja a nyelvet, az RTGS-megújítás biztosítja az elszámolási alapot, az összekapcsolás biztosítja az elérést, a DLT-kísérletek pedig azt tesztelik, hogy a programozható elszámolás javíthatja-e a modellt. A gazdasági nyeremény: kevesebb csapdába esett likviditás, kevesebb manuális javítás, gyorsabb elszámolás, jobb megfelelés és ellenállóbb globális kereskedelem.

A kockázat az, hogy minden joghatóság önmagában modernizál. Ha ez történik, a világ újabb fizetési rendszereket kap, amelyek fragmentáltak maradnak. Ha a harmonizáció kitart, a nagykereskedelmi fizetések a globális gazdasági hatékonyság valódi motorjává válnak.

## Gyakran ismételt kérdések

**Miért fontos az ISO 20022 a nagykereskedelmi fizetések számára?**

Azért fontos, mert a strukturált adatok javítják a straight-through feldolgozást, a megfelelési szűrést, az egyeztetést és az interoperabilitást a fizetési rendszerek és a piaci infrastruktúrák között ([BIS CPMI](https://www.bis.org/cpmi/publ/brief11.htm "The future of financial messaging: navigating the ISO 20022 migration journey")).

**Jó úton halad a G20 határon átnyúló fizetési ütemterve?**

Az FSB szerint történt előrehaladás, de a 2027-es célok még nincsenek jó úton, és további köz- és magánszektori intézkedéseket igényelnek ([FSB](https://www.fsb.org/2026/03/reforming-cross-border-payments-keynote-speech-at-the-fsb-payments-summit/ "Reforming cross-border payments")).

**Mi az RTGS-megújítás szerepe?**

Az RTGS-megújítás javítja az ellenállóképességet, a hozzáférést, az interoperabilitást és az elszámolási funkcionalitást. A Bank of England kiemeli továbbá a szinkronizált elszámolási felületeket és az ISO 20022-t mint az elszámolási kockázat és a likviditási költségek csökkentésének mechanizmusait ([Bank of England](https://www.bankofengland.co.uk/payment-and-settlement/rtgs-renewal-programme/the-renewed-rtgs-service-key-benefits "The renewed RTGS service — key benefits")).

**A stablecoinok felváltják a nagykereskedelmi fizetéseket?**

Nem. A stablecoinok befolyásolhatják a határon átnyúló fizetések kialakítását, de a nagykereskedelmi fizetések elszámolási véglegességet, jegybankpénz-horgonyokat, prudenciális kontrollokat és jogi bizonyosságot igényelnek. A hitelesebb intézményi irány a kereskedelmi banki pénz, a jegybankpénz és a tokenizált elszámolási rendszerek közötti interoperabilitás.

## Hivatkozások

- BIS CPMI, (2026). [The future of financial messaging: navigating the ISO 20022 migration journey ⧉](https://www.bis.org/cpmi/publ/brief11.htm "BIS CPMI Brief No 11").
- FSB, (2026). [Reforming Cross-border payments ⧉](https://www.fsb.org/2026/03/reforming-cross-border-payments-keynote-speech-at-the-fsb-payments-summit/ "FSB Payments Summit keynote").
- BIS, (2026). [Interconnect to stabilize: cross-border payments in a fragmenting world ⧉](https://www.bis.org/cpmi/speeches/sp260505.pdf "Fabio Panetta speech").
- Bank of England, (2026). [The renewed RTGS service — key benefits ⧉](https://www.bankofengland.co.uk/payment-and-settlement/rtgs-renewal-programme/the-renewed-rtgs-service-key-benefits "Renewed RTGS service").
- Atlantic Council, (2026). [Global payment systems are fragmenting ⧉](https://www.atlanticcouncil.org/in-depth-research-reports/issue-brief/global-payment-systems-are-fragmenting-heres-what-the-g20-can-do/ "Payment-system fragmentation").
