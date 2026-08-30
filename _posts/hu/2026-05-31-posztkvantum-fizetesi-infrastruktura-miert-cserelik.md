---
title: "Posztkvantum fizetési infrastruktúra: miért cserélik le a bankok a régi rendszereket ahelyett, hogy utólag módosítanák őket"
tags: "post-quantum cryptography, crypto-agility, HNDL, ML-KEM, ML-DSA, NIST, payment infrastructure, ISO 20022, SWIFT, HSM, PKI, operational resilience, DORA, quantum computing, AI"
subtitle: "Az ML-KEM és az ML-DSA nem illeszkedik tisztán a SWIFT MT és az ISO 20022 üzeneteket szállító rendszerekbe. Az őszinte mérnöki válasz az, hogy az utólagos módosítás rövid szavatosságú, szabályozott migrációs terv, a csere pedig az egyetlen stabil végállapot."
description: "A posztkvantum kriptográfia bináris döntés elé állítja a fizetési rendszereket: utólag módosítani az RSA/ECC megoldást a SWIFT MT és ISO 20022 borítékokon belül, amelyeket sosem méreteztek az ML-KEM és ML-DSA algoritmusokhoz, vagy lecserélni kriptoagilis infrastruktúrára. Az építészeknek dönteniük kell, mielőtt a HNDL működési veszteséggé válik."
date: "May 31, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/lan-pham-4qG2qqXi3tY.webp"
banner_alt: "Kriptográfiai kulcsanyag sodródik a mélykék vízbe, jelképezve a fizetési üzenetek harvest-now-decrypt-later elfogását, amelyek RSA- és ECC-borítékai nem élik túl egy kriptoanalitikailag releváns kvantumszámítógép megjelenését"
keywords: "posztkvantum kriptográfia, PQC fizetések, kriptoagilitás, Harvest Now Decrypt Later, HNDL, NIST posztkvantum szabványok, ML-KEM, ML-DSA, FIPS 203, FIPS 204, fizetési rendszer migráció, ISO 20022 PQC, SWIFT MT csere, HSM, PKI-összeomlás, működési ellenállóképesség, Quantum Computing Cybersecurity Preparedness Act"
---

## Posztkvantum fizetési infrastruktúra: miért cserélik le a bankok a régi rendszereket ahelyett, hogy utólag módosítanák őket

A kriptográfiai primitívek, amelyek ma minden éles nagykereskedelmi fizetést hitelesítenek, az RSA, az ECDSA és az ECDH, lejárati dátummal rendelkeznek. Az USA [Quantum Computing Cybersecurity Preparedness Act ⧉](https://www.congress.gov/bill/117th-congress/house-bill/7535/text "H.R. 7535") ezt a lejárati dátumot 2022 végén beírta a szövetségi közbeszerzési jogba. A [BIS Working Paper No. 1208 ⧉](https://www.bis.org/publ/work1208.htm "Project Leap: Quantum-proofing the financial system") ugyanezt a lejáratot a jegybankok felügyeleti keretébe emelte. A [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "Module-Lattice-Based Key-Encapsulation Mechanism Standard") és a [FIPS 204 ⧉](https://csrc.nist.gov/pubs/fips/204/final "Module-Lattice-Based Digital Signature Standard") 2024 augusztusában publikálta a helyettesítőket.

A fizetési infrastruktúra még nem dolgozta fel, mit jelent mindez.

Ez a cikk a mérnöki érvelés a csere mellett az utólagos módosítással szemben. Olyan építészeknek szól, akik már értik az algoritmusokat, és el kell dönteniük, mit tegyenek a SWIFT MT-vel, az [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) pacs- és pain-üzenetekkel, az RTGS-interfészekkel, a HSM-állományokkal és a mindezek alatt húzódó tanúsítványhierarchiákkal.

---

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - **A harvest-now-decrypt-later (HNDL) a működési fenyegetés.** A támadók 2026-ban rögzítik a titkosított fizetési forgalmat, hogy dekódolják, amint létezik egy kriptoanalitikailag releváns kvantumszámítógép (CRQC). Az elfogott forgalom kiegyenlítési utasításokat, kedvezményezetti adatokat és hosszú élettartamú érzékenységű hitelesítési anyagokat tartalmaz.
> - **A NIST szabványosította a helyettesítőket.** Az ML-KEM (FIPS 203) a kulcskapszulázáshoz és az ML-DSA (FIPS 204) a digitális aláírásokhoz az alapértelmezettek. Az SLH-DSA (FIPS 205) fedi az állapotmentes, hash-alapú tartalékmegoldást.
> - **A méretkülönbség szétzúzza a régi feltételezéseket.** A nyilvános kulcsok és aláírások 5-20-szor nagyobbak az RSA-2048 megfelelőknél. Ez ütközik a fizetési hálózatok MTU-értékével, az MT-üzenetkezelők rögzített pufferre vonatkozó feltételezéseivel és a telepített HSM-flották kriptográfiai átbocsátóképességével.
> - **A hibrid (klasszikus + PQC) a migráció eszköze, nem a végállapota.** A hibrid TLS és a hibrid X.509 két-három év interoperabilitást vásárol, amíg az éles rendszereket lecserélik. Nem oldják meg a mögöttes kapacitásproblémát.
> - **A PKI a teherhordó fal.** Az a tanúsítványkibocsátó, amelynek aláírási algoritmusa hamisíthatóvá válik, érvényteleníti alatta minden tanúsítványt. A bank intézményi kitettsége a lánc, nem pedig egyetlen végpont.
> - **A kriptoagilitás az a mérnöki architekturális tulajdonság, amelyre tervezni kell.** Az algoritmusazonosítóknak, a kulcsformátumoknak, az aláírási borítékoknak és a HSM-partícióknak mind paraméterezhetőnek kell lenniük. Bármi, ami fordítási időben RSA-hoz van rögzítve, technikai adósság, amely egyszerre válik esedékessé.
>
---

## Harvest Now, Decrypt Later: a fenyegetési modell, amely megszünteti a várakozás lehetőségét

A HNDL megfordítja a szokásos kriptográfiai idővonalat. A hagyományos kockázatértékelés azt kérdezi, mikor válik valóra a fenyegetés. A HNDL azt kérdezi, mikor válik a ma elfogott adat hasznossá egy támadó számára. A fizetési üzenetek esetében, kedvezményezetti azonosságok, számlaszámok, strukturált átutalási adatok, szankciószűrési tartalmak, bankközi kiegyenlítési utasítások, az érzékenységi ablak évektől évtizedekig terjed. E forgalom nagy része jelenleg is rögzítve van valahol.

Az [NSA CNSA 2.0 idővonala ⧉](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF "Commercial National Security Algorithm Suite 2.0") 2035-ig ad időt a nemzetbiztonsági rendszereknek az átállás befejezésére. A pénzügyi felügyeletek gyorsabb ütemtervvel haladnak: a [PRA működési ellenállóképességre vonatkozó elvárásai ⧉](https://www.bankofengland.co.uk/prudential-regulation/publication/2021/march/operational-resilience-impact-tolerances-for-important-business-services-ss "PRA SS1/21") a kriptográfiai agilitást harmadik feles koncentrációs kockázatként kezelik. A 2026-os elvárás az, hogy a jelentős fizetési rendszerek közzétegyék PQC-migrációs tervüket ellenállóképességi önértékelésükben.

A HNDL-támadónak nincs szüksége CRQC-re ma. A támadónak a következőkre van szüksége:

1. **Hálózati pozíció.** A tengeralatti kábelek lehallgatása, az ISP-szintű elfogás és a kompromittált középdobozok mind hatókörben vannak. A nagykereskedelmi fizetési forgalom kevés hálózati útvonalon koncentrálódik.
2. **Tárhely.** Egy petabájtnyi strukturált fizetési adat 2026-ban kezelhető archívum.
3. **Türelem.** Az elfogás elfogott üzenetenként semmibe sem kerül. A hozam később érkezik.

A migrációs érv tehát nem az, hogy „a kvantumszámítógépek 2035-ben megérkezhetnek”. Hanem az, hogy „bármely TLS-munkamenet, amely ma éjjel RSA-2048 kulcscserével fejeződik be, addig kitett, ameddig a benne lévő adat érzékeny marad”.

## A méretprobléma a mérnöki probléma

A PQC-migrációról szóló nyilvános vita hajlamos az algoritmusválasztásra összpontosítani. A nehezebb probléma dimenzionális.

| Primitív | Nyilvános kulcs | Aláírás / rejtjelezett szöveg |
|---|---|---|
| RSA-2048 | 256 bájt | 256 bájt (aláírás) |
| ECDSA P-256 | 64 bájt | 64 bájt (aláírás) |
| ML-KEM-768 | **1 184 bájt** | **1 088 bájt (rejtjelezett szöveg)** |
| ML-DSA-65 | **1 952 bájt** | **3 309 bájt (aláírás)** |
| SLH-DSA-128f | 32 bájt | **17 088 bájt (aláírás)** |

Ezek a számok közvetlenül olyan hibamódokra vetülnek, amelyekre a régi fizetési infrastruktúrát sosem tervezték:

- **Csomagtöredezettség az útvonalon.** Egy hibrid ML-KEM-768 plusz klasszikus X25519 megoldást hordozó ClientHello meghaladja a tipikus 1 500 bájtos Ethernet MTU-t. A két fizetési végpont közötti középdobozok töredezik, eldobják vagy átírják a kézfogást. A hiba időszakos TLS-hibaként jelentkezik, amely átmeneti hálózati zajnak tűnik.
- **Pufferfeltételezések az MT-kezelőkben.** Sok SWIFT MT-integráció ECDSA-hoz méretezett aláírt borítékokat hordoz. Helyezz egy ML-DSA-aláírást ugyanabba a borítékba, és az elemző vagy csonkol, vagy elutasít.
- **HSM-átbocsátóképesség.** Az ML-DSA-aláírás egy telepített HSM-flottán műveletenként 3-10-szer lassabb, mint az ECDSA, olyan hardveren, amelynek másodpercenkénti kulcskeretét már a napvégi kötegelt ablakok is erősen terhelik.
- **Tanúsítványlánc súlya.** Egy négyszintű CA-hierarchia, amelyet ML-DSA-aláírásokkal újra kibocsátanak, nagyjából 6 KB-ról nagyjából 60 KB-ra nő. Minden TLS-kézfogás a rendszer felé ezt megfizeti.

Az utólagos módosítás útja az, hogy ezeket a korlátokat egyenként osztályozzuk: nagyobb pufferek itt, gyorsabb HSM-ek ott, töredezettségtűrés a középdobozokban. Ez egy védhető hat hónapos áthidalás. Nem architektúra.

## Utólagos módosítás kontra csere: a döntés, amely meghatározza a programot

Az őszinte megfogalmazás az, hogy az utólagos módosítás rövid szavatosságú, szabályozott migrációs terv, a csere pedig az egyetlen stabil végállapot. A döntés az, hogy melyiket finanszírozza először a bank, és meddig marad nyitva az utólagos módosítás ablaka, mielőtt tartós toldozás-foltozássá válik.

Az utólagos módosítás a következőket jelenti:

- Hibrid TLS (ML-KEM + X25519), amelyet a meglévő rendszerhatáron zárnak le.
- Kettős aláírású tanúsítványok (RSA elsődleges, ML-DSA másodlagos), amelyeket egy PQC-képes alárendelt CA bocsát ki.
- Nagyobb MT-pufferek és szigorúbb MTU-szabályzat a fizetési VPN-eken.
- HSM-firmware-frissítések ott, ahol a gyártók támogatják a PQC-primitíveket; teljes HSM-csere ott, ahol nem.

Ez a munka elvégezhető. Nem oldja meg a mögöttes problémát, ami az, hogy a SWIFT MT és sok ISO 20022 implementáció a kriptográfiai borítékot olyan üzenetformátumon belül kódolja, amely rögzíti az algoritmust. A következő algoritmusátállás, és lesz ilyen, amikor az ML-KEM végül gyengeséget mutat vagy egy új szabvány felváltja, ugyanazt a migrációt futtatja le újra ugyanazokon a rendszereken.

A csere azt jelenti, hogy elfogadjuk: a kriptográfiai réteg nem az üzenetformátum tulajdonsága. Egy elkülöníthető borítékszolgáltatás tulajdonsága, amelyet az üzenetformátum hív meg. Konkrétan:

- A szállításbiztonsági határ egy service meshbe vagy sidecarba kerül, amely lezárja a hibrid TLS-t, és a tiszta szöveges üzenetet stabil interfészen keresztül adja át a rendszernek.
- Az üzenetszintű aláírásokat egy dedikált aláíró szolgáltatás állítja elő, amelynek algoritmusválasztása konfigurációs paraméter, nem pedig szigorúan kódolt feltételezés.
- A tanúsítványokat olyan CA bocsátja ki, amelynek aláírási algoritmusa maga is forgatható.
- A HSM-partíciókat rendeltetés szerint (szállítás, aláírás, kulcskapszulázás) címezik, nem üzenetformátum szerint.

A csere tervezése túléli a következő algoritmusváltást anélkül, hogy újra hozzá kellene nyúlni a rendszerhez.

## A kriptoagilis architektúra rétegről rétegre

A PQC-migráció szempontjából fontos infrastruktúrarétegek nem az „adat, kontroll, gazdaság” üzleti rétegei, amelyek egy általános banki narratívához illenek. A fontos rétegek kriptográfiaiak.

| Réteg | Mit tesz | A PQC-kérdés | Építészeti irányelv |
|---|---|---|---|
| **HSM / kulcskezelés** | Kulcsanyagot generál, tárol és operál rajta hardveres elszigetelés alatt | Támogatja-e a telepített HSM-firmware az ML-KEM-et, az ML-DSA-t és egy hibrid kulcskapszulázási API-t? Mekkora az aláírási átbocsátóképesség eltérése az ECDSA-hoz képest ugyanazon a hardveren? | Vedd leltárba minden HSM-partíciót algoritmustámogatás és másodpercenkénti kapacitás szerint. Vonj ki minden olyat, ami firmware-út nélkül RSA-hoz van rögzítve. Állíts fel dedikált PQC-partíciókat az éles átállás előtt. |
| **PKI / tanúsítványkibocsátó** | X.509-tanúsítványokon keresztül bizalmat bocsát ki, von vissza és láncol | Tud-e a CA ma ML-DSA-val aláírni? Van-e tesztelt folyamat a gyökér forgatására és a lánc újbóli kibocsátására? A CRL- és OCSP-válaszadók az ML-DSA-aláírás súlyához vannak-e méretezve? | Kezeld a CA-készletet teherhordó falként. Hozz létre most egy PQC-képes alárendeltet. Időzítsd a gyökérforgatást a leghosszabb élettartamú tanúsítványfüggőséghez, ne a kényelemhez. |
| **Szállítás / hálózat** | Lezárja a TLS-t, IPsec-et és MACsec-et a fizetési végpontok között | Tolerálja-e a terheléselosztó, a WAF és a középdoboz-útvonal a régi MTU-t meghaladó hibrid kézfogásokat? A munkamenet-folytatási jegyek PQC-kulcsokhoz vannak-e méretezve? | Helyezd a TLS-lezárást kriptoagilis határra (sidecar vagy mesh). Emeld az MTU-szabályzatot a fizetési VPN-eken. Teszteld a teljes útvonalat szándékosan előidézett töredezettséggel. |
| **Alkalmazás / üzenettartalom** | SWIFT MT, ISO 20022 pacs / pain / camt üzeneteket és azok kriptográfiai borítékait hordozza | Tolerálja-e a rendszer üzenetkezelője az ML-DSA-méretű aláírt borítékokat? Az köztes elemzők algoritmustudatosak, vagy hosszra csonkolnak? | Válaszd szét a borítékot a tartalomtól. Írj alá szolgáltatáshatáron, ne az üzenetformátum-kezelőn belül. Kezeld az algoritmusazonosítókat adatként, ne sémaként. |
| **Audit / bizonyíték** | Előállítja a kriptográfiai őrzési láncot, amelyre a felügyeletek és az ügyfelek támaszkodnak | Ellenőrizhetők-e még a történelmi aláírt rekordok, amint az aláírási algoritmust elavulttá nyilvánítják? Van-e hosszú távú archiválási aláírási terv? | Ellenjegyezd az archívumokat hash-alapú primitívvel (SLH-DSA) olyan biztosítékért, amely túléli bármely egyetlen algoritmus feltörését. Kezeld az auditláncot szabályozott műtermékként, ne pedig build-melléktermékként. |

A fegyelem az, hogy minden algoritmusválasztást konfigurációs értékké tegyünk minden rétegben. Az az intézmény, amely e rétegek bármelyikén RSA-2048-at kódol keményen, egy összehangolt életciklus-végi eseményt örököl, amikor az az algoritmus elbukik.

## Mit jelent ez banktípusonként

A kitettségi profil intézményenként eltér. Az irányelvek ennek megfelelően különböznek.

### Globális bankok

A globális bankok üzemeltetik a legnagyobb telepített HSM-flottákat, a leghosszabb tanúsítványláncokat és a legösszetettebb hálózati útvonalakat a partnerek között. A domináns kockázat nem az algoritmusválasztás, hanem az algoritmusok egyidejű megváltoztatásának koordinációs költsége több száz belső szolgáltatáson és több tucat külső partneren keresztül.

Az irányelv az, hogy a PQC-képes CA-t, a kriptoagilis szállítási határt és az algoritmusparaméterezett aláíró szolgáltatást 2026-os munkaként finanszírozzák, mielőtt bármely egyes rendszert utólag módosítanak. Az utólagos módosítás ekkor rutinszerű éles változtatássá válik egy ismert kereten belül. A keret nélkül minden rendszer utólagos módosítása újratárgyalja ugyanazokat az építészeti döntéseket.

### Regionális bankok

A regionális bankoknak kisebb az algoritmikus felületük, de arányosan kevesebb szakemberük. A domináns kockázat a HSM-gyártói bezártság olyan algoritmusokhoz, amelyek támogatását a gyártó nem vállalta.

Az irányelv az, hogy a PQC-támogatást, konkrétan az ML-KEM-et és az ML-DSA-t, tesztelt firmware-frissítési úttal, minden HSM-szerződés megújításába beleírják 2026-tól kezdve. Az ilyen záradék nélküli bankok kényszerű hardvercserét örökölnek a gyártó ütemterve szerint, nem a sajátjuk szerint.

### Fintechek és PSP-k

A fizetési szolgáltatók és a fintechek jellemzően egy bankpartner és egy kereskedő vagy végfelhasználói rendszer között helyezkednek el. Kriptográfiai kitettségük a mindkét oldali API-határ.

Az irányelv az, hogy közzétegyenek egy hibrid TLS-interfészt, klasszikus plusz ML-KEM, a bank felőli oldalon, mint alapelvárást a 2026-os kereskedelmi tárgyalásokon. Az a fintech, amely már bemutatott PQC-interoperabilitással érkezik, elnyeri az integrációs ciklusokat azzal a fintechhel szemben, amely még el sem kezdte.

### Vállalati kincstárnokok

A kincstárnokok nem üzemeltetnek közvetlenül kriptográfiai infrastruktúrát. Fogyasztják azonban: minden bank-API, minden biztonságos fájlátvitel, minden aláírt visszaigazolás a bank PKI-jától függ.

Az irányelv az, hogy minden banki ajánlatkéréshez három kérdést adjanak hozzá 2026-ban: mely PQC-algoritmusokat használja a bank ma az ügyféloldali TLS-ben, mi a bank terve az ML-DSA-aláírású fizetési visszaigazolásokra, és hogyan szándékozik a bank megőrizni a történelmi aláírt rekordok ellenőrizhetőségét, amint az RSA elavulttá válik. Azok a bankok, amelyek nem tudják megválaszolni ezeket a kérdéseket, jeleznek valamit a mögöttes mérnöki felkészültségükről.

## Mi történik ezután

A PQC-telepítés első hulláma a fizetésekben láthatatlan lesz a végfelhasználók számára. A hibrid TLS megjelenik a kézfogásban, a tanúsítványláncok nőnek, a HSM-aláírás késleltetése néhány ezredmásodperccel kúszik feljebb, és a rendszerek tovább működnek. Ez a siker útja.

A látható hibák utólagos módosítás vezéreltek lesznek: egy rendszer, amely csonkolás nélkül nem tud elfogadni egy ML-DSA-aláírású borítékot, egy CA, amelynek CRL-elosztási pontja megakad az új aláírási súlyon, egy középdoboz, amely a hibrid kézfogásokat átrendezett ClientHellókra töredezi. Ezek a hibák 2027-ig érkeznek éles környezetbe.

A 2026-os építészeti döntés az, hogy a cserét biztosító infrastruktúrát finanszírozzák-e, amely az utólagos módosítást irrelevánssá teszi, vagy egy sor rendszerspecifikus javítást, amelyek egyenként olcsóbbnak tűnnek, és egy hosszabb, drágább migrációvá összegződnek. Az a bank, amely az első utat választja, csendesebb működéssel futja végig az átmenetet. Az a bank, amely a másodikat választja, az évtized hátralévő részét azzal tölti, hogy incidensfelülvizsgálatokat magyaráz a felügyeleteknek.

A PQC nem infrastruktúra-problémának álcázott kriptográfiai probléma. Infrastruktúra-probléma, amelyet a kriptográfia történetesen elindított.

## Gyakran ismételt kérdések

**Van olyan határidő, amely kikényszeríti ezt a munkát?**

A kemény szabályozási határidők joghatóságfüggők. Az USA [Quantum Computing Cybersecurity Preparedness Act ⧉](https://www.congress.gov/bill/117th-congress/house-bill/7535/text "H.R. 7535") a szövetségi rendszereket köti. Az [NSA CNSA 2.0 idővonala ⧉](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF "CNSA 2.0") 2035-öt céloz a nemzetbiztonsági rendszerek esetében. A [BIS Project Leap ⧉](https://www.bis.org/publ/work1208.htm "BIS Working Paper 1208") publikáció és az FSB munkaprogramja előrébb húzza ezt a horizontot a rendszerszintű fizetési infrastruktúra számára. A HNDL azt jelenti, hogy a működési óra jóval e névleges dátumok bármelyike előtt elindult.

**Miért az ML-KEM az ajánlott kulcskapszulázás valami gyorsabb helyett?**

Az ML-KEM (a [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) szabványosított változata) rendelkezett a kis rejtjelezett szöveg és kulcsméretek legerősebb kombinációjával a rácsjelöltek között, érett implementációkkal és oldalcsatorna-védelemmel. A NIST [FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203") néven publikálta. Léteznek gyorsabb jelöltek, de nagyobb mérettel vagy a biztonsági paraméterekre vonatkozó gyengébb konfidenciaintervallumokkal járnak.

**Miért ne használjunk mindenütt SLH-DSA-t az ML-DSA helyett?**

Az SLH-DSA (a SPHINCS+ szabványosított változata) hash-alapú, ezért kizárólag a hash-függvények biztonságára támaszkodik, ami a rendelkezésre álló legkonzervatívabb feltételezés. Aláírásai 5-20-szor nagyobbak az ML-DSA-énál. Ez elfogadható archív ellenjegyzéshez, de kivitelezhetetlen tranzakciós aláíráshoz, ahol a méret üzenetenként számít. A szokásos minta az ML-DSA az éles aláíráshoz és az SLH-DSA az archív biztosítékhoz.

**Várhat-e egy bank egyszerűen addig, amíg a rendszerek közzéteszik a PQC-profilokat?**

Az a bank, amely vár, azt a migrációs ablakot örökli, amelyet a rendszer közzétesz, ami rövidebb, mint a bank saját belső változtatási ciklusa. Mire a SWIFT, a helyi RTGS-üzemeltető és az érintett CCP-k mindegyike közzéteszi PQC-profilját, a migrációs ablak tizenkét-huszonnégy hónap lesz. Azok a bankok, amelyek nem építették elő CA-, szállítási és HSM-képességüket, működési rövidre zárások nélkül nem fogják teljesíteni.

**Mi az egyetlen legnagyobb hatású dolog, amit először finanszírozni kell?**

Egy PQC-képes alárendelt tanúsítványkibocsátó, amely a meglévő PKI-ba integrálva kettős algoritmusú tanúsítványokat (RSA plusz ML-DSA) tud kibocsátani anélkül, hogy megzavarná az éles bizalmat. Ez létrehozza a forgatási primitívet. Minden más, a szállítási frissítések, a HSM-partíció tervezése, az üzenetboríték-változtatások, köré ütemezhető.

## Hivatkozások

- Congress.gov, (2022). [H.R. 7535 - Quantum Computing Cybersecurity Preparedness Act ⧉](https://www.congress.gov/bill/117th-congress/house-bill/7535/text "Quantum Computing Cybersecurity Preparedness Act").
- NIST, (2024). [FIPS 203 - Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203").
- NIST, (2024). [FIPS 204 - Module-Lattice-Based Digital Signature Standard ⧉](https://csrc.nist.gov/pubs/fips/204/final "FIPS 204").
- NIST, (2024). [FIPS 205 - Stateless Hash-Based Digital Signature Standard ⧉](https://csrc.nist.gov/pubs/fips/205/final "FIPS 205").
- NSA, (2022). [Commercial National Security Algorithm Suite 2.0 ⧉](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF "CNSA 2.0").
- BIS, (2024). [Working Paper No. 1208 - Project Leap: Quantum-proofing the financial system ⧉](https://www.bis.org/publ/work1208.htm "BIS Working Paper 1208").
- Bank of England (PRA), (2024). [SS1/21 - Operational resilience: Impact tolerances for important business services ⧉](https://www.bankofengland.co.uk/prudential-regulation/publication/2021/march/operational-resilience-impact-tolerances-for-important-business-services-ss "PRA SS1/21").
