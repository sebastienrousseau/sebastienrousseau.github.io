---
title: "A kvantumkriptográfiai újraindítás 2026-ban: PQC-szabványok, QKD-tanúsítás és a migrációs munka, amelyet a bankok nem halogathatnak"
tags: "quantum cryptography, post-quantum cryptography, NIST, FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC, IETF, TLS, IPsec, QKD, ETSI, crypto-agility, HNDL, cybersecurity, ISO 20022, AI"
subtitle: "A kvantumkriptográfia a horizontfigyeléstől a megvalósítási fegyelemig jutott: a NIST PQC-szabványai készen állnak, az Egyesült Királyság NCSC útmutatása szűkítette az algoritmusválasztékot, az IETF protokollmunkája még érlelődik, a QKD-tanúsítás pedig a laboratóriumi bizonyosságtól a tanúsítási nyelvezet felé mozdul."
description: "A kvantumkriptográfia 2026-ban már nem arról szóló vita, hogy a kvantumszámítógépek küszöbön állnak-e. Ez egy migrációs program a posztkvantum-kriptográfián, a kriptográfiai agilitáson, a kvantumkulcs-elosztás tanúsításán, a protokollszabványokon, a beszállítói felkészültségen és a hosszú élettartamú pénzügyi adatokon átívelve, amelyek már ma ki vannak téve a most-begyűjt-később-visszafejt kockázatnak."
date: "May 18, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/alex-shuper-YYZnrK8NrSw-unsplash.webp"
banner_alt: "Kvantumbiztos kriptográfiai migrációs térkép 2026-ra, amely a NIST PQC-szabványokat, a hibrid protokollmunkát, a QKD-tanúsítást, a kriptográfiai agilitást és a banki adatkockázati szinteket mutatja"
keywords: "kvantumkriptográfia 2026, posztkvantum-kriptográfia, NIST FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC PQC, IETF TLS, IPsec, RFC 9794, hibrid kulcscsere, QKD, ETSI QKD, ISO IEC 23837, kriptográfiai agilitás, most begyűjt később visszafejt, HNDL, pénzügyi szolgáltatások kriptográfiája, banki biztonság"
---

## A kvantumkriptográfiai újraindítás 2026-ban: PQC-szabványok, QKD-tanúsítás és a migrációs munka, amelyet a bankok nem halogathatnak

A kvantumkriptográfia 2026-ban két gyakorlati sávra vált szét. A posztkvantum-kriptográfia mostanra megvalósítási program, mert a NIST szerint három posztkvantum-szabvány készen áll a használatra, és a szövetségi rendszereknek FIPS-szabványként kell kezelniük őket ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")); a [kvantumkulcs-elosztás](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) tanúsítási és minősítési kérdéssé válik, mert a [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) telepítéseknek értékelési nyelvezetre, védelmi profilokra és üzemeltetési szabványokra van szükségük, nem pusztán laboratóriumi bemutatókra ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI releases QKD Protection Profile")).

---

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - **A NIST a PQC-t a megvalósítás fázisába helyezte.** A jelenlegi szabványok a FIPS 203 az ML-KEM kulcslétesítéshez, a FIPS 204 az ML-DSA aláírásokhoz és a FIPS 205 az SLH-DSA aláírásokhoz, a NIST pedig sürgeti a szervezeteket, hogy azonosítsák a sérülékeny kriptográfiát és kezdjék meg a migrációt most ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")).
> - **Az Egyesült Királyság NCSC-je szűkítette a gyakorlati választékot.** A legtöbb felhasználási esetre az ML-KEM-768-at és az ML-DSA-65-öt ajánlja, ugyanakkor figyelmeztet, hogy a rendszereknek a végleges szabványok robusztus megvalósításaira kell támaszkodniuk, nem pedig tervezetkompatibilis kísérletekre ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")).
> - **A protokollkészültség egyenetlen.** Az IETF a TLS-t és az IPsec-et frissíti a PQC és a hibrid kulcscsere érdekében, de az NCSC óva int attól, hogy az üzemi rendszerek a változó Internet Drafteket részesítsék előnyben a közzétett RFC-kkel szemben ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")).
> - **A hibrid egy átmeneti mechanizmus, nem végállapot.** A hibrid nyilvános kulcsú plusz posztkvantum sémák segítik a migráció szakaszolását és fedezik a megvalósítási kockázatot, de bonyolultságot adnak hozzá, és később szükségessé tehetnek egy második migrációt a csak PQC-re ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")).
> - **A [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) nem a PQC helyettesítője.** A [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) speciális, magas biztonságú összeköttetéseket szolgálhat ki, de banki relevanciája a tanúsítástól, az interoperabilitástól, az üzemeltetési költségtől és a meglévő kulcskezelő rendszerekkel való integrációtól függ, nem pusztán a fizikától ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI releases QKD Protection Profile")).
> - **A bank szintjén a kérdés a leltár.** Az a pénzintézet, amely nem tudja megtalálni az RSA, ECDH, ECDSA, EdDSA, saját fejlesztésű VPN-kriptográfiát, HSM-sablonokat, tanúsítvány-élettartamokat és beszállító által kezelt kriptográfiát, nem tud migrálni, függetlenül attól, hogy mely szabványok állnak rendelkezésre.
> - **A kockázat már ma élő.** A most-begyűjt-később-visszafejt támadások a hosszú élettartamú pénzügyi adatokat már azelőtt sérülékennyé teszik, hogy kriptográfiailag releváns kvantumszámítógépek léteznének, mert az ellenfélnek csak ma kell begyűjtenie a titkosított szöveget.
> - **A kriptográfiai agilitás a tartós kontroll.** A győztes architektúra nem egyszeri csere RSA-ról ML-KEM-re; ez egy platformképesség az algoritmusok, paraméterek, könyvtárak, tanúsítványok, hardverpolitikák és protokollmódok rotálására a bank újjáépítése nélkül.
>
---

## Miért fontos ez a hét

A szabványokról szóló beszélgetés túljutott az absztrakció pontján. A NIST nyilvános útmutatása szerint a szervezeteknek most kell megkezdeniük az új szabványok alkalmazását, azonosítaniuk kell, hol használnak sérülékeny algoritmusokat, és meg kell tervezniük a termék-, szolgáltatás- és protokollfrissítéseket ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Ez a megfogalmazás azért fontos, mert a PQC-t kutatási témából technológiafrissítési függőséggé alakítja.

Az időzítés azért is számít, mert a pénzügyi adatoknak hosszú a bizalmassági felezési ideje. Az M&A anyagok, a treasury-mozgások, a szankciós vizsgálatok, az ügyfél-azonosító dokumentumok, a fizetési útvonalválasztási metaadatok és a nagybani elszámolási nyilvántartások évekig érzékenyek maradhatnak. A klasszikus nyilvános kulcsú kriptográfiát feltörő kvantumszámítógépnek nem kell ma léteznie ahhoz, hogy a kitettség ma is racionális legyen.

## A 2026-os kriptográfiai alapvonal: négy munkafolyam

### 1. A PQC-szabványok kellően készen állnak a tervezéshez

Az első alapvonal algoritmikus. A NIST PQC-programja mostanra megnevezett célokat ad a technológiai vezetőknek: ML-KEM a kulcslétesítéshez, ML-DSA az általános digitális aláírásokhoz és SLH-DSA a hash alapú aláírásokhoz ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")). A gyakorlati hatás az, hogy a beszerzési, architektúra- és beszállítókezelő csapatok abbahagyhatják annak firtatását, hogy léteznek-e majd PQC-szabványok, és elkezdhetik azt kérdezni, hogy az egyes rendszerek mikor fogják támogatni őket.

A nehezebb pont a kompatibilitás. Az NCSC figyelmeztet, hogy a tervezetszabványokon alapuló megvalósítások esetleg nem kompatibilisek a végleges szabványokkal, ami pontosan az a fajta részlet, amely tönkreteszi a nagybanki migrációkat, ha figyelmen kívül hagyják ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")). A bankoknak ezért el kell különíteniük a kísérleti pilotokat a produkciós migrációs útvonalaktól.

### 2. A protokollok a szűk keresztmetszet

Az algoritmusok önmagukban nem biztosítják a banki forgalmat. A TLS, az IPsec, az SSH, az S/MIME, a fizetési API-k, a HSM-integrációk és a tanúsítványkezelő rendszerek mind protokollszintű támogatást igényelnek. Az NCSC kijelenti, hogy az IETF a széles körben használt protokollokat, például a TLS-t és az IPsec-et frissíti, hogy a PQC-algoritmusok beépíthetők legyenek a kulcscsere- és aláírási mechanizmusokba ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")).

Ez szakaszolt megvalósítási problémát teremt. Egy bank azonnal leltározhatja a kriptográfiát, azonnal megkövetelheti a beszállítói ütemterveket, és azonnal megtervezheti a kriptográfiai agilitást, de mégis várnia kell a stabil protokollmegvalósításokra, mielőtt a magas kritikusságú produkciós csatornákat áthelyezné.

### 3. A QKD tanúsítási fegyelemmé válik

A [kvantumkulcs-elosztás](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) továbbra is releváns marad a rendkívül speciális összeköttetéseknél, különösen ahol az intézmény ellenőrzi a végpontokat és a hálózati útvonalakat. A fontos 2026-os fejlemény nem egyetlen új [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) doboz; hanem a tanúsítási nyelvezet megjelenése, ahol az ETSI GS [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) 016 a [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) termékértékelés védelmiprofil-mérföldköveként van leírva ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI releases QKD Protection Profile")).

A bankok számára ez áthelyezi a vásárlási beszélgetést. A helyes kérdés már nem az, hogy a [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) elviekben kvantumbiztos-e. A helyes kérdés az, hogy az eszköz, az integráció, a kulcskezelési folyamat, az üzemeltetési környezet és a tanúsítási bizonyíték megfelel-e a bank fenyegetésmodelljének.

### 4. A kriptográfiai agilitás az architektúra

A kriptográfiai agilitás az a képesség, hogy az algoritmusokat az egész rendszer megváltoztatása nélkül lehessen cserélni. Kiterjed a szoftverkönyvtárakra, a protokollegyeztetésre, a HSM-politikára, a tanúsítványprofilokra, a kulcs-élettartamokra, az aláírási szolgáltatásokra, az auditbizonyítékokra és a visszaállítási útvonalakra. Enélkül minden kriptográfiai migráció egyedi projektté válik.

Ez az alapvető architekturális tanulság. A posztkvantum-átállás nem lesz az utolsó kriptográfiai átállás, amellyel a pénzügyi rendszer szembesül. Azok a bankok, amelyek most építik ki a kriptográfiai agilitást, újrafelhasználható vezérlősíkot kapnak az algoritmusfrissítésekhez, a beszállítói kockázathoz, a sürgősségi visszavonáshoz és a szabályozói bizonyítékhoz.

## Mit tegyenek a bankok most

### Építsék fel a kriptográfiai eszközleltárt

Az első leszállítandó egy kriptográfiai anyagjegyzék. Tartalmaznia kell a nyilvános kulcsú algoritmusokat, a kulcshosszokat, a tanúsítványkiadókat, a HSM-sablonokat, a TLS-verziókat, a VPN-termékeket, a fizetési átjárókat, a harmadik féltől származó API-kat, a mobil SDK-kat, a nyugalmi adatok titkosítási burkolóit, az aláírókulcsokat, a firmware-aláírási folyamatokat és a beszállító által kezelt kriptográfiát.

A leltárnak meg kell különböztetnie a bizalmasságot és a hitelességet. A hosszú élettartamú titkosított adatok ki vannak téve a most-begyűjt-később-visszafejt kockázatnak, míg a hosszú élettartamú aláírókulcsok jövőbeli hamisítási kockázatot teremtenek, ha sérülékeny nyilvános kulcsú algoritmusokban maradnak gyökerezve.

### Szegmentáljanak az adatok felezési ideje szerint

Nem minden adat igényli ugyanazt a migrációs sorrendet. Egy valós idejű kártyaengedélyezési üzenetnek más lehet a bizalmassági felezési ideje, mint egy szankciós vizsgálatnak, egy vállalatfelvásárlási aktának, egy private banking azonosítócsomagnak vagy egy államadósság-kibocsátási dokumentumnak. Ezért tartozik a kvantummigráció az adatosztályozáshoz, nem pedig kizárólag a hálózati biztonsághoz.

A prioritásnak azoknak a rendszereknek kell lenniük, amelyek hosszú élettartamú adatokat védenek sérülékeny kulcslétesítéssel. Ezek azok a rendszerek, ahol a mai begyűjtés holnapi kitettséget teremt.

### Kényszerítsék a beszállítói ütemterveket a szerződésekbe

A NIST szerint a termékeknek, szolgáltatásoknak és protokolloknak frissítésre van szükségük az átálláshoz ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Ez azt jelenti, hogy a beszerzési nyelvezetnek meg kell változnia. A beszállítóknak közzé kell tenniük a PQC-támogatás ütemtervét, a végleges szabvánnyal való kompatibilitást, a hibrid mód viselkedését, a hardvermodul-korlátozásokat, a teljesítménybeli hatásokat, a tanúsítványprofil-támogatást és a tartalék kontrollokat.

Az a beszállító, amely csak annyit mond, hogy „kvantumbiztos ütemterv", nem válaszolta meg a kérdést. A banknak dátumokra, algoritmusokra, integrációs határokra és bizonyítékra van szüksége.

## PQC, QKD és hibrid: gyakorlati döntési táblázat

| Kontroll | Legjobb felhasználás | 2026-os státusz | Banki fenntartás |
|---|---|---|---|
| **ML-KEM / FIPS 203** | Kulcslétesítés a jövőálló bizalmasságért | Szabványosítva és készen a megvalósítás tervezésére ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")) | Protokoll- és könyvtártámogatásra van szükség a kritikus produkciós bevezetés előtt |
| **ML-DSA / FIPS 204** | Általános digitális aláírások | Az NCSC a legtöbb általános aláírási felhasználási esethez ajánlja ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")) | A tanúsítványláncok és a PKI-migráció üzemeltetésileg nehéz |
| **SLH-DSA / FIPS 205** | Hash alapú aláírások firmware- és szoftveraláíráshoz | Az NCSC által hivatkozott végleges NIST-szabvány ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")) | A nagyobb aláírások hatással lehetnek a korlátozott környezetekre |
| **Hibrid PQ/T sémák** | Átmeneti migráció és interoperabilitás | Hasznos átmeneti intézkedésként ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")) | Bonyolultságot ad hozzá és második migrációt igényelhet |
| **QKD** | Speciális, magas biztonságú összeköttetések | A tanúsítási munka érlelődik az ETSI védelmiprofil-tevékenységén keresztül ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI releases QKD Protection Profile")) | Nem oldja meg az általános internetméretű hitelesítést vagy a vállalati kriptográfiai leltárt |

## Mit jelent ez intézménytípusonként

### Első vonalbeli univerzális bankok

Az első vonalbeli bankoknak programirodára van szükségük, nem koncepcióbizonyításra. A célműködési modellnek egyesítenie kell a kriptográfiai leltárt, a beszállítói kikényszerítést, a HSM-ütemterv kezelését, a hibrid TLS/IPsec tesztkörnyezeteket és a szabályozásra kész bizonyítékot. A legnagyobb értékű korai munka nem minden titkosító azonnali cseréje; hanem annak a vezérlősíknak a felépítése, amely a változást biztonságossá teszi.

### Közép- és regionális bankok

A közép-kategóriájú bankoknak a PQC-t beszállítókezelési és platformszabványosítási feladatként kell kezelniük. Elkerülhetik a drága egyedi munkát azzal, hogy a rendszereket támogatott könyvtárak, szabványos TLS-készletek, felügyelt tanúsítványszolgáltatások és világos beszállítói határidők köré összpontosítják. A fő kockázat a berendezésekben, fizetési átjárókban és örökölt köztes szoftverekben rejlő rejtett kriptográfia.

### Fintechek, PSP-k és kriptográfiához közeli intézmények

A fintechek gyorsabban mozoghatnak, mert általában kevesebb örökölt bizalmi horgonyuk van. A kockázat az önelégültség a harmadik féltől származó API-kban, a felhő KMS alapértelmezéseiben, a tárcainfrastruktúrában és a letéti integrációkban. A kriptográfiához közeli cégeknek különösen óvatosaknak kell lenniük, hogy ne keverjék össze a blokkláncnatív biztonsági narratívákat a posztkvantum-felkészültséggel.

### Mérnökök és biztonsági architektek

A mérnöki fegyelem konkrét: adjanak algoritmus-metaadatokat a szolgáltatásleltárakhoz, naplózzák az egyeztetett protokollmódokat, hozzanak létre biztonságos feature flageket a hibrid tesztekhez, rövidítsék le a tanúsítvány-élettartamokat, ahol lehetséges, távolítsák el a merevkódolt algoritmus-feltételezéseket, és tegyék a kriptográfiai politikát konfiguráción keresztül telepíthetővé, ne kódágazások útján.

## Következtetés

A kvantumkriptográfiai újraindítás nem egyetlen technológiai vásárlás. Ez egy kriptográfiai működési modell. A NIST szabványalapvonalat adott az iparágnak, az NCSC szűkítette a gyakorlati útmutatást, a protokolltestületek még mozgásban vannak, a QKD-tanúsítás pedig egyre formálisabbá válik. Azok a banki intézmények, amelyek megnyerik ezt az átállást, nem azok lesznek, amelyek a legnagyobb pilotot bejelentik. Azok az intézmények lesznek, amelyek tudják, hol lakik a kriptográfiájuk, tudják, mely adatokat kell először védeni, és képesek a kriptográfiai primitíveket a bank újjáépítése nélkül cserélni.

## Gyakran ismételt kérdések

**Készen áll a posztkvantum-kriptográfia a bankok általi használatra?**

Tervezésre, beszállítói egyeztetésre, pilotokra és kiválasztott megvalósítási munkára készen áll. A NIST szerint három szabvány készen áll a megvalósításra, míg az NCSC figyelmeztet, hogy az üzemeltetési használatnak a végleges szabványok robusztus megvalósításaira és stabil protokollokra kell támaszkodnia ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography"), [NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC next steps in preparing for PQC")).

**Megszünteti-e a QKD a PQC iránti igényt?**

Nem. A QKD hasznos lehet speciális, ellenőrzött összeköttetésekhez, de a PQC a skálázható migrációs útvonal az általános szoftverek, internetprotokollok, API-k, tanúsítványok és vállalati rendszerek számára. A QKD ráadásul tanúsítási és minősítési keretrendszerektől függ, mielőtt bankminőségű infrastruktúraként kezelhető lenne ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI releases QKD Protection Profile")).

**Mit kell először migrálni?**

A hosszú élettartamú érzékeny adatokat védő rendszereket kell előtérbe helyezni. Ide tartozik az archívumtitkosítás, a fizetési vizsgálatok, a treasury- és tőkepiaci dokumentumok, a private banking azonosítónyilvántartások, a stratégiai ügyletaktak, a gyökértanúsítvány-kiadók, a firmware-aláírás és a bankközi csatornák.

**Mi a legnagyobb megvalósítási csapda?**

A legnagyobb csapda a PQC algoritmuscseréként való kezelése. A migráció érinti a protokollokat, a tanúsítványokat, a HSM-eket, a beszállítókat, a teljesítménytesztelést, az incidenskezelést, a monitorozást és az irányítást. Kriptográfiai agilitás nélkül az intézmény egyszerűen újrateremti ugyanazt a migrációs problémát a következő algoritmusváltáshoz.

## Hivatkozások

- NIST, (2025). [Post-quantum cryptography ⧉](https://www.nist.gov/pqc "Post-quantum cryptography").
- NCSC, (2024). [Next steps in preparing for post-quantum cryptography ⧉](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC PQC guidance").
- NIST CSRC, (2026). [The NIST Post-Quantum Cryptography Project ⧉](https://csrc.nist.gov/presentations/2026/mpts2026-3b1 "The NIST PQC Project").
- ID Quantique, (2024). [ETSI releases world's first Protection Profile for QKD ⧉](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD 016").
