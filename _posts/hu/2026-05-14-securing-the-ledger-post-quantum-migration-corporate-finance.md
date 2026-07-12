---
title: "A főkönyv védelme: igazgatósági szintű útmutató a posztkvantum migrációhoz a vállalati pénzügyekben"
tags: "post-quantum cryptography, corporate banking, G7 CEG, BIS Project Leap, ML-KEM, ML-DSA, NCSC, ASD, CNSA 2.0, harvest now decrypt later, Mosca equation, crypto-agility, hybrid cryptography, ISO 20022, DORA, quantum computing, AI, Rust, open source, cross-border payments"
subtitle: "A kvantumkockázat kutatási érdekességből aktív szabályozói előírássá vált. A G7 2026 januárjában közzétett ütemtervével és a BIS Project Leap élő fizetési rendszerekben bizonyított megvalósíthatóságával az igazgatósági szintű kérdés már nem az, hogy migráljanak-e: hanem az, hogy befejezhető-e a migráció, mielőtt a mai adatok eltarthatósága lejár."
description: "A kvantumkockázat kutatási érdekességből aktív szabályozói előírássá vált. A G7 2026 januárjában közzétett ütemtervével, az EU, az Egyesült Királyság és az ASD tisztázott határidőivel, valamint a BIS Project Leap központi banki szinten bizonyított megvalósíthatóságával az igazgatóságok számára a kérdés már nem az, hogy migráljanak-e: hanem az, hogy befejezhető-e a migráció, mielőtt a mai adatok kriptográfiai eltarthatósága lejár."
date: "May 14, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Posztkvantum kriptográfiai migrációs ütemtervet ábrázoló diagram: vállalati banki infrastruktúra átállása RSA-ról ML-KEM-re és ML-DSA-ra"
keywords: "posztkvantum kriptográfia, PQC migráció, vállalati bankolás, pénzügyi szolgáltatások, G7 CEG ütemterv, BIS Project Leap, ML-KEM, ML-DSA, FIPS 203, FIPS 204"
---

## A főkönyv védelme: igazgatósági szintű útmutató a posztkvantum migrációhoz a vállalati pénzügyekben

A kvantumkockázat kutatási érdekességből aktív szabályozói előírássá vált. A G7 2026 januárjában közzétett ütemtervével, az EU, az Egyesült Királyság és Ausztrália tisztázott határidőivel, valamint a BIS Project Leap élő fizetési rendszerekben bizonyított megvalósíthatóságával az igazgatóságok számára a kérdés már nem az, hogy migráljanak-e: hanem az, hogy befejezhető-e a migráció, mielőtt a mai adatok kriptográfiai eltarthatósága lejár.

---

> **Legfontosabb tanulságok**
>
> - **2026 az az év, amikor a szabályozói álláspont megkeményedett.** A G7 Cyber Expert Group januári ütemterve, az EU NIS Cooperation Group összehangolt idővonala és az Egyesült Királyság NCSC háromfázisú terve a beszélgetést a tudatosságtól a végrehajtás felé mozdította. Az Australian Signals Directorate még tovább ment, kemény 2030-as véghatáridőt szabva a klasszikus aszimmetrikus kriptográfiának.
> - **A kitettség aszimmetrikus.** Az RSA, az ECC és a Diffie-Hellman a közvetlen probléma: az aszimmetrikus algoritmusok, amelyek a SWIFT kézfogások, a TLS, a PKI, a kódaláírás és a klíringhálózati hitelesítés alapját képezik. A szimmetrikus titkosítás (AES-256) stabil marad, ha a kulcshosszakat fenntartják. Az igazgatósági szintű figyelmet az aszimmetrikus felületre kell összpontosítani.
> - **A harvest-now-decrypt-later nem jövőbeli forgatókönyv.** Az ellenfelek ma is elfogják és tárolják a titkosított pénzügyi naplókat, elszámolási rekordokat, M&A anyagokat és határokon átnyúló utalási adatokat, azzal a kifejezett szándékkal, hogy megfejtsék, amint egy kriptográfiailag releváns kvantumszámítógép (CRQC) létezik. A 10-20 éves bizalmassági követelménnyel rendelkező adatok esetében ez a kockázat már realizálódott.
> - **Az iparágnak most már működő referenciapontja van.** A [BIS Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), amelyet 2025 decemberében tettek közzé, sikeresen lecserélte a hagyományos digitális aláírásokat posztkvantum kriptográfiára az élő likviditási átutalásokban a TARGET2-n keresztül, és felszínre hozta azokat a konkrét mérnöki költségeket (ellenőrzési késleltetés, csomagméret), amelyekkel minden migrációs program szembesül majd.
> - **A NIST-készlet a globális horgony.** A [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") és a FIPS 204 (ML-DSA) minden nagyobb joghatóság hivatkozási alapja, még ott is, ahol a nemzeti álláspontok eltérnek a paraméterkészletek és a hibrid követelmények tekintetében. Az igazgatóságoknak az ML-KEM-768/ML-DSA-65-öt kell alsó határnak, az ML-KEM-1024/ML-DSA-87-et pedig a hosszú életű adatokra vonatkozó konzervatív alapvonalnak tekinteniük.
> - **A hibrid az egyetlen hiteles út.** A tiszta átállásokat egyetlen nagyobb hatóság sem javasolja. A klasszikus és a kvantumálló algoritmusok párhuzamos futtatása az a telepítési minta, amelyet az NCSC, az ANSSI és a BSI is támogat, és amelyet a Project Leap bizonyított. Nehezebb, mint bármelyik alternatíva, de ez az egyetlen, amely mind a mai kompatibilitást, mind a holnapi fenyegetést kezeli.

---

## Az év, amikor a szabályozói álláspont megkeményedett

Az elmúlt évtized nagy részében a posztkvantum kriptográfia a hosszú távú ütemterv kényelmes sarkában húzódott meg. A kvantumszámítógépek lenyűgözőek voltak, de távoliak; az RSA és az elliptikus görbék alapjául szolgáló kriptográfiai matematikát stabil alapzatként kezelték; és a migrációról szóló beszélgetés jórészt szakértői munkacsoportokra korlátozódott. Ez az álláspont már nem tartható.

2026 januárjában a [G7 Cyber Expert Group közzétette eddigi legjelentősebb állásfoglalását ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"), amelynek társelnöke az US Treasury és a Bank of England volt. A dokumentum nem szabályozás, de nagyobb súlyt hordoz a tipikus iránymutatásnál: a G7 joghatóságok pénzügyminisztériumainak, központi bankjainak és felügyeleti hatóságainak közös álláspontját képviseli arról, hogy a kriptográfiai átállás immár rendszerszintű kockázatkezelési kérdés. Az ütemterv a tervezési horizontját a 2030-as évek közepe köré igazítja, a kritikus pénzügyi rendszereket pedig korábbi migrációra ösztönzi: ez a megfogalmazás a központi bankárok óvatos idiómájában elvárást jelez, nem javaslatot.

Két hónappal korábban a BIS Innovation Hub és az Eurosystem közzétette a [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems") eredményeit, egy olyan technikai kísérletét, amely a hagyományos digitális aláírásokat posztkvantum kriptográfiára cserélte a Bank of Italy, a Banque de France, a Deutsche Bundesbank, a Nexi-Colt és a Swift közötti élő likviditási átutalásokban. A fő megállapítás siker volt: a kvantumálló módon aláírt átutalások végponttól végpontig sikeresen áthaladtak egy működő fizetési rendszeren. A címsor alatti részletek tanulságosabbak, és ezeket a cikk később vizsgálja.

E két esemény, egy összehangolt G7 szakpolitikai keret és egy működő bizonyíték egy valós fizetési rendszerben, együttesen azt hozta létre, amire a szakmai közösség egy évtizede várt: végleges választ a kérdésre, hogy „valós ez?”. A válasz 2026 májusában igen. A hátralévő kérdés a tempóé.

## Három fenyegetési vektor, amelynek aggasztania kell az igazgatóságot

A migráció mechanikájának tárgyalása előtt érdemes pontosan meghatározni, hogy konkrétan mi van veszélyben. A kvantumkockázat a vállalati bankolásban nem egyenletes a kriptográfiai állományban, és az igazgatóság figyelmét legjobb arra a három vektorra irányítani, ahol a kitettség a legélesebb.

### 1. Harvest Now, Decrypt Later (HNDL)

A legközvetlenebb aggodalom nem a jövő. Hanem a jelen. Állami szintű és kifinomult bűnözői ellenfelek szisztematikusan elfogják és tárolják a titkosított pénzügyi forgalmat: banki utalásokat, SWIFT üzenetfolyamokat, M&A kommunikációt, határokon átnyúló elszámolási naplókat, swap-megállapodásokat és KYC-fájlokat, jelenleg mindenféle olvasási képesség nélkül. Céljuk egyszerű: tárolj most, fejtsd később, amint egy CRQC létezik. Ahogyan a [Bank for International Settlements kifejezetten megjegyezte ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), ez a gyűjtés már zajlik.

Az igazgatóságok számára a következtetés kényelmetlen, de konkrét: minden érzékeny adat, amelyet ma klasszikus aszimmetrikus titkosítással továbbítanak, és amelynek bizalmassági követelménye túlnyúlik egy CRQC megjelenésén, már most kitettnek tekintendő. Nincs jogsértési értesítés, amikor HNDL történik. Nincs riasztás a SIEM-ben. A titkosítás egyelőre kitart, de az adat már elhagyta a védelmi vonalat.

### 2. Hosszú távú érzékenységi kockázat

A vállalati banki adatoknak szokatlanul hosszú intézményi eltarthatósága van. A stratégiai M&A dokumentáció egy évtizedig is piacérzékeny maradhat. Az üzleti titkokat érintő kommunikáció és a szellemi tulajdon értékelése tizenöt-húsz évig is bizalmas maradhat. A határokon átnyúló elszámolási naplók, a központi szerződő felek kitettségei és a partnerkockázati minősítések jóval a közvetlen tranzakciós életciklusukon túl is megőrzik kereskedelmi érzékenységüket.

A [Mosca-egyenlet ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), amelyet eredetileg Michele Mosca fogalmazott meg, és amely ma már minden komoly migrációs keretrendszer részét képezi, formalizálja a problémát. Ha az **S** az adat eltarthatósága, az **M** az azt védő rendszerek migrálásához szükséges idő, a **Q** pedig a CRQC elérhetőségéig hátralévő idő, akkor:

```
Ha S + M > Q, az adat már ki van téve.
```

A húszéves bizalmassági horizonttal rendelkező adatok és egy reálisan öt-hét évet igénylő migrációs program esetén az a burkolt Q-érték, amelyre az igazgatóság fogad, legalább 25 évre tehető. A szakértői értékelések növekvő halmaza: a [Forrester 2026-os APAC előrejelzései ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), a Global Risk Institute éves felmérései, valamint egy 2026 februári architektúra-tanulmány, amely a CRQC-t nagyjából 100 000 fizikai qubitre teszi QLDPC kódok használatával, arra utal, hogy ez a fogadás nem biztonságos.

### 3. Az alapvető kézfogások sebezhetősége

A harmadik vektor a legjelentősebb architektúra szempontjából. A szimmetrikus rejtjelek (AES-256) viszonylag stabilak maradnak; a Grover-algoritmus felezi az effektív biztonsági szintet, de a kulcshossz megduplázása helyreállítja a tartalékot. A katasztrofális kitettség az aszimmetrikus algoritmusokat érinti, és pontosan ezek az algoritmusok képezik a vállalati pénzügyek minden hitelesített kézfogásának alapját: az RSA a SWIFT nyilvános kulcsú infrastruktúrában, az ECDSA a TLS kliens/szerver hitelesítésben, az ECDH a munkamenetkulcs-létrehozásban, valamint az ECC-változatok a kliensoldali mobilhitelesítésben, az API-aláírásokban és a kódaláíró folyamatokban.

Egy működő, Shor-algoritmust futtató CRQC nem fokozatosan gyengíti ezeket a rendszereket. Feltöri őket. Amint egy CRQC üzemképes, minden RSA-védett kézfogás, minden ECDSA-aláírás és minden elliptikus görbés kulcscsere helyreállíthatóvá válik, nem hónapokig tartó erőfeszítéssel, hanem órák alatt. A „biztonságos”-ból „kompromittált”-ba való átmenet bináris, és egyszerre terjed minden olyan rendszerre, amely az érintett algoritmust használja. Ez az alapja a szabályozói sürgősségnek.

## Szabályozói szigorodás: joghatóságonkénti áttekintés

A globális szabályozási kép 2026 májusában már nem javaslatok foltvarrott takarója. Összehangolt határidők együttese, amelyek szigorúságukban eltérnek, de ugyanabba a célállomásba futnak össze. A nagyobb pénzügyi központokban működő multinacionális bank immár a legszigorúbb alkalmazandó joghatóság hatálya alá tartozik, nem a legengedékenyebbé.

### Egyesült Államok

Az Egyesült Államok rendelkezik a legszigorúbb előírásokkal minden olyan intézmény számára, amely szövetségi rendszerekhez kapcsolódik. Az NSA [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") ML-KEM-1024-et és ML-DSA-87-et ír elő a nemzetbiztonsági rendszerekhez, az új rendszerektől 2027 januárjától megkövetelve a PQC telepítését, az infrastruktúra teljes migrációját pedig 2035-ig. Az OMB M-23-02 memorandum ugyanerre a pályára kötelezi a szövetségi ügynökségeket. A kereskedelmi bankok számára a közvetlen kitettség a szövetségi beszerzési láncokon, az NSS-hez kapcsolódó szerződéseken, valamint azon a közvetett nyomáson keresztül jelenik meg, amelyet az NSA iránymutatása a tágabb piacra gyakorol.

### Európai Unió

Az EU három rétegen működik. Az [Európai Bizottság összehangolt megvalósítási ütemterve ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), amelyet a NIS Cooperation Group 2025 júniusában dolgozott ki, szakaszos mérföldköveket tűz ki 2026-ra (nemzeti stratégiák), 2030-ra (magas kockázatú rendszerek migrálva) és 2035-re (teljes átállás). A Cyber Resilience Act 2027 végétől kötelezővé teszi a legkorszerűbb biztonsági fejlesztéseket a digitális termékek számára. A NIS2 megerősíti az IKT-kockázatkezelést, bár egyik irányelv sem tartalmaz kifejezett PQC-követelményt. A nemzeti szabályozók azonban a Bizottság elé vágtak. Németország BSI-ja hibrid kulcscserét ír elő, és jóváhagyja az ML-KEM, a FrodoKEM és a Classic McEliece konzervatív kosarát. Franciaország ANSSI-ja hibridet követel meg mind a kulcs-enkapszulációhoz, mind az aláírásokhoz. Hollandia NLNCSA-ja és Norvégia hatóságai az ML-KEM-1024 köré igazodtak, mint a hosszú életű adatok konzervatív alapvonala.

### Egyesült Királyság

Az Egyesült Királyság NCSC 2025 márciusában tette közzé végleges iránymutatását, és a 2025-ös éves felülvizsgálaton keresztül megerősítette azt. A háromfázisú idővonal egyértelmű:

- **2028-ig** - A fejlesztést igénylő kriptográfiai szolgáltatások azonosítása, a migrációs terv kidolgozása és a teljes kriptográfiai leltár elkészítése.
- **2028 és 2031 között** - A magas prioritású fejlesztések végrehajtása, különösen a kritikus rendszereken és a kifelé néző internetes protokollokon.
- **2031 és 2035 között** - A migráció befejezése minden rendszeren, szolgáltatáson és terméken.

Az Egyesült Királyság pénzügyi intézményei számára a [CMORG (Cross-Market Operational Resilience Group) PQC-iránymutatás ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") az NCSC keretrendszere mellett helyezkedik el, a bankokat kritikus nemzeti infrastruktúraként kezelve, és hangsúlyozva a beszállítói felkészültséget és az ellátási lánc összehangolását.

### Ázsia és a Csendes-óceáni térség

Az APAC-álláspont töredezettebb, de gyorsan mozog. Ausztrália ASD-je rendelkezik a legszigorúbb állásponttal globálisan: a klasszikus nyilvános kulcsú kriptográfia 2030 vége után nem használható, nincs hibrid ajánlás, és ML-KEM-1024 szükséges (az ML-KEM-768 csak 2030-ig elfogadható). A szervezeteknek 2026 végére finomított átállási tervvel kell rendelkezniük. Szingapúr monetáris hatósága formális kvantumbiztos felkészültségi iránymutatást adott ki. Japán és Dél-Korea jelentős beruházásokat eszközöl, bár mindkettőnek van nemzeti algoritmuspályája (Korea az NTRU+-t és a SMAUG-T-t választotta KEM-ként, az ALMer-t és a HAETAE-t aláírásként). India Nemzeti Kvantummissziója, amelyet 6003,65 crore rúpiás kormányzati ráfordítás támogat, kifejezetten a banki és pénzügyi rendszereket azonosítja stratégiai prioritásként. A [Forrester 2026-os APAC előrejelzései ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") 90% fölé teszik azon regionális vállalatok arányát, amelyek várhatóan idén posztkvantum technológiákba fektetnek.

### A nettó álláspont

Egy igazgatóság számára e joghatósági álláspontok gyakorlati szintézise egyértelmű. Egy multinacionális bank nem igazodhat egyetlen szabályozó határidejéhez sem; a legszigorúbb alkalmazandóhoz kell igazodnia. A legtöbb nagy intézmény számára ez a magas kockázatú rendszerekre 2030 végi, a hosszú farokra pedig 2035 végi tervezési horizontot jelent, az ASD-nek kitett szervezetek 2030-ra tiszta PQC-t céloznak, a CNSA-nak kitett szervezetek pedig ugyanezt az ablakot célozzák, konkrétan ML-KEM-1024-gyel és ML-DSA-87-tel.

## BIS Project Leap: mit bizonyított valójában az iparág

A Project Leap nem azért érdemli meg egy igazgatóság figyelmét, mert marketingmérföldkő, hanem mert a posztkvantum kriptográfia eddigi leghitelesebb, végponttól végpontig terjedő demonstrációja egy élő pénzügyi fizetési rendszerben. A fő következtetés egyszerű: működik. A mögöttes részletekben rejlenek a működési következmények.

Az első fázis, amely 2023-ban fejeződött be, kvantumálló VPN-t hozott létre a Bank of France és a Deutsche Bundesbank informatikai rendszerei között, a Párizs és Frankfurt között továbbított fizetési üzenetekkel egy hibrid titkosítási séma alatt. A második fázis, amely 2025 végén fejeződött be, és amelyről [decemberben számoltak be ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), lényegesen tovább ment. A konzorcium a hagyományos RSA-alapú digitális aláírásokat posztkvantum aláírásokra cserélte a likviditási átutalások végrehajtása során a TARGET2-n, az Eurosystem valós idejű bruttó elszámolási rendszerén keresztül. A résztvevők, a BIS Innovation Hub Eurosystem Centre, a Bank of Italy, a Banque de France, a Deutsche Bundesbank, a Nexi-Colt (amely a TARGET2-kapcsolatot biztosítja) és a Swift, pontosan azokat az intézményeket képviselik, amelyek infrastruktúrájának végül migrálnia kell.

A jelentés három megállapítást emelt ki, amelyet minden migrációs programnak internalizálnia kell:

- **Az ellenőrzési késleltetés érdemben magasabb.** A posztkvantum aláírás-ellenőrzés lényegesen tovább tartott, mint az RSA-alapú ellenőrzés ugyanazon a hardveren. Egy másodperc alatti üzenetkezelésre tervezett RTGS-rendszer esetében ez nem marginális megfigyelés; ez kapacitástervezési bemenet.
- **A csomagméretek rendszer-újrafejlesztést igényelnek.** A PQC-aláírások egy nagyságrenddel nagyobbak, mint az ECDSA megfelelőik (erről bővebben lentebb). Azok a fizetési rendszerek, amelyek belső várólistáit, monitorozó eszközeit és adatbázis-sémáit örökölt üzenetméretekre méretezték, nem tudják befogadni az új hasznos terhelést újratervezés nélkül. A Project Leap kifejezetten megállapította, hogy a TARGET2 nem tudja „könnyen befogadni” a hibrid modellt jelentős újrafejlesztés nélkül.
- **A hibrid a helyes válasz, de nehezebb.** A klasszikus és a posztkvantum algoritmusok párhuzamos futtatása megőrizte a visszafelé kompatibilitást és mélységi védelmet nyújtott, de megduplázta a kriptográfiai feldolgozási többletterhelést. Ez a PQC helyes elvégzésének működési költsége az átmenet során; ez pusztán ügyes mérnöki munkával nem kerülhető el.

Egy PQC üzleti esetet áttekintő pénzügyi vezető (CFO) számára a Project Leap megállapításai éppen azért hasznosak, mert pontosak. A posztkvantum migráció költsége nem egyetlen tőkesor. Hanem ellenőrzési késleltetés, amely végigfut az SLA-szerződéseken, üzenetméret-növekedés, amely érinti a tárolási és sávszélességi költségvetéseket, valamint a duplikált kriptográfiai műveletek átmeneti időszaka, amely befolyásolja a számítási kapacitás tervezését. Ezek egyike sem spekulatív. Egy élő központi banki rendszerben mérték őket.

## A NIST eszköztár: ML-KEM és ML-DSA összehasonlítva

Minden hiteles nemzeti keretrendszer technikai központi eleme a NIST 2024 augusztusában közzétett posztkvantum szabványkészlete. Ezek közül két szabvány a vállalati bankolás közvetlen fókusza: az ML-KEM (FIPS 203) a kulcs-enkapszulációhoz és az ML-DSA (FIPS 204) a digitális aláírásokhoz. Közös matematikai alapon nyugszanak: mindkettő a Module Learning With Errors (ML-LWE) és a Module Short Integer Solution problémák nehézségére támaszkodik strukturált rácsok felett, de nagyon eltérő szerepet töltenek be a kriptográfiai állományban, és teljesítmény- és méretprofiljuk érdemben eltér.

### ML-KEM (FIPS 203): kulcs-enkapszuláció

Az ML-KEM, amely a [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)-ből származik, az ECDH és az RSA-KEM helyettesítője azokban a protokollokban, ahol két félnek megosztott szimmetrikus kulcsot kell létrehoznia egy nem biztonságos csatornán. Gyakorlati értelemben ide kerülnek a TLS-kézfogások, miután az RSA-t és az ECDH-t kivezetik. A NIST három paraméterkészletet definiál növekvő biztonsági erősséggel és csökkenő teljesítménnyel: ML-KEM-512 (NIST Category 1), ML-KEM-768 (Category 3) és ML-KEM-1024 (Category 5).

### ML-DSA (FIPS 204): digitális aláírások

Az ML-DSA, amely a CRYSTALS-Dilithiumból származik, az RSA- és az ECDSA-aláírások helyettesítője. Kezeli a tanúsítványaláírást, a kódaláírást, a dokumentumaláírást és a hitelesítést. A három paraméterkészlet az ML-DSA-44, az ML-DSA-65 és az ML-DSA-87, amelyek nagyjából a NIST 2., 3. és 5. kategóriájának felelnek meg.

### Méret- és teljesítményprofil

Egy migrációs kapacitást tervező informatikai vezető (CIO) számára a legfontosabb számadatok az artefaktumok méretei. Ezek a bemenetek a hálózati kapacitástervezéshez, a tárolási előrejelzésekhez és a protokollszintű teszteléshez.

| Algoritmus | Nyilvános kulcs | Rejtjelezett szöveg / aláírás | Legközelebbi klasszikus megfelelő | Méret a klasszikushoz képest |
|---|---|---|---|---|
| ML-KEM-512 | 800 bájt | 768 bájt (rejtjelezett szöveg) | ECDH P-256 (~32 bájtos nyilvános kulcs) | ~25× nagyobb |
| ML-KEM-768 | 1,184 bájt | 1,088 bájt (rejtjelezett szöveg) | ECDH P-384 | ~25× nagyobb |
| ML-KEM-1024 | 1,568 bájt | 1,568 bájt (rejtjelezett szöveg) | ECDH P-521 | ~25× nagyobb |
| ML-DSA-44 | 1,312 bájt | ~2,420 bájt (aláírás) | ECDSA P-256 (64 bájtos aláírás) | ~38× nagyobb |
| ML-DSA-65 | 1,952 bájt | ~3,293 bájt (aláírás) | ECDSA P-384 | ~50× nagyobb |
| ML-DSA-87 | 2,592 bájt | ~4,595 bájt (aláírás) | ECDSA P-521 | ~70× nagyobb |

*Forrás: a [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") és a FIPS 204 specifikációk szintézise, független benchmarking-irodalomból származó összehasonlító adatokkal.*

Három működési következmény adódik közvetlenül. **Először**, az aláírás mérete a meghatározó korlát a legtöbb vállalati telepítésnél. Egy ML-DSA-65 aláírás nagyjából ötvenszerese egy ECDSA P-256 aláírásnak, és a köztes CA-kat hordozó TLS-tanúsítványláncok arányosan nőnek. Az e felületen végzett kapacitásmunka nem opcionális, hanem teherhordó. **Másodszor**, az ML-KEM számítási szempontból versenyképes az ECDH-val, egyes implementációkban pedig érdemben gyorsabb, különösen az alapul szolgáló rácsaritmetika vektorizált támogatásával rendelkező hardveren. **Harmadszor**, az ML-DSA ellenőrzése egyenletesen gyors (gyakran gyorsabb, mint az ECDSA ellenőrzése), de az ML-DSA aláírás egy elutasításos mintavételi ciklust tartalmaz, amely korlátozott hardveren több próbálkozást igényelhet. A nagy áteresztőképességű aláíró szolgáltatásoknál ezt inkább ellenőrizni, mint feltételezni kell.

### A paraméterkészletek megválasztása

A paraméterválasztásra vonatkozó joghatósági álláspontok nem azonosak, de a konvergencia egyértelmű. Az ML-KEM-768 és az ML-DSA-65 a vállalati alsó határ: az Egyesült Királyság NCSC alapvonalként támogatja az egyesült királyságbeli szervezetek számára, és a legtöbb európai keretrendszer szerint elfogadható. Az ML-KEM-1024 és az ML-DSA-87 a konzervatív felső határ: az NSA CNSA 2.0 az amerikai nemzetbiztonsági rendszerekhez írja elő, az ASD pedig 2030-ig megköveteli az ausztrál szabályozott szervezetektől. A rendkívül hosszú távú érzékenységű adatok esetében: állami elszámolási naplók, egy évtizeden túli szellemi tulajdon, hosszú lejáratú instrumentumok letéti rekordjai, a magasabb paraméterkészletek a védhető alapértelmezés.

### Közös matematikai alap, közös kockázat

Egy igazgatósági szintű megjegyzés érdemel figyelmet: mind az ML-KEM, mind az ML-DSA a rácsproblémák ugyanazon családjából származtatja biztonságát. Egy jövőbeli kriptoanalitikai áttörés a Module-LWE ellen egyszerre érintené mindkét szabványt. Pontosan ezért ajánl több nemzeti hatóság, nevezetesen Németország BSI-ja és Franciaország ANSSI-ja, hogy a rácsalapú készletet hash-alapú aláírásokkal (SLH-DSA, FIPS 205) egészítsék ki a hosszú távú aláírási és kódaláírási felhasználási esetekhez. A kriptográfiai agilitás ebben az értelemben nem csak arról szól, hogy képesek legyünk az RSA-t ML-KEM-re cserélni. Arról szól, hogy képesek legyünk az egyik PQC-algoritmust egy másikra cserélni, amikor a kriptoanalitikai táj megváltozik.

## Logikus migrációs út: felderítés → triázs → hibrid telepítés

Egy többéves PQC-programot jóváhagyó igazgatóság számára a működési kérdés az, hogyan lehet a munkát fázisokra bontani anélkül, hogy elfogadhatatlan szolgáltatás-rendelkezésre állási kockázatot vállalnának. A G7 ütemterv, az NCSC keretrendszer, a BIS Project Leap és a nagyobb nemzeti iránymutatások dokumentumai mentén kirajzolódó minta három fázisba fut össze.

```
┌────────────────────────┐   ┌────────────────────────┐   ┌────────────────────────┐
│  1. FELDERÍTÉS ÉS CBOM │ → │  2. TRIÁZS (MOSCA)     │ → │  3. HIBRID TELEPÍTÉS   │
│  Kriptográfiai         │   │  Kockázatalapú         │   │  Kettős boríték:       │
│  leltár minden         │   │  prioritizálás az      │   │  klasszikus + PQC,     │
│  rendszerről           │   │  adatélettartam szerint│   │  kriptoagilis          │
└────────────────────────┘   └────────────────────────┘   └────────────────────────┘
```

### Első fázis: felderítés és a kriptográfiai anyagjegyzék (CBOM)

A migrációt nem lehet megtervezni egy olyan kriptográfiai állományra, amelyet nem térképeztek fel, és a legtöbb intézménynek nincs pontos térképe. Az első fázis ezért egy kriptográfiai anyagjegyzék (Cryptographic Bill of Materials) elkészítése: az aszimmetrikus kriptográfia minden előfordulásának strukturált leltára a szervezetben, ahol minden előfordulást megjelölnek algoritmus, kulcshossz, protokollkörnyezet, adatérzékenység és rendszergazda szerint. A kódbázisok, webalkalmazások, konténerképek, adatbázis-konfigurációk, tanúsítványtárolók, hardveres biztonsági modulok és beszállítói interfészek automatizált átvizsgálása a gyakorlati mechanizmus; az örökölt rendszerek és a szabadalmaztatott protokollok kézi leltározása az elkerülhetetlen kiegészítés.

Az első fázis eredménye nem látványos, de ez az egyetlen alap, amelyre a második és harmadik fázis épülhet. Ez egyben az a szállítandó eredmény is, amelyet a legtöbb belső ellenőrzési funkció és külső szabályozó először keres majd, amikor a PQC-megfelelőségi igazolásokat elkezdik kérni.

### Második fázis: kockázati triázs a Mosca-egyenlettel

A CBOM birtokában az intézmény eszközről eszközre alkalmazhatja Mosca keretrendszerét. Minden kriptográfiai függőségnél a kérdés az, hogy **S + M > Q**, vagyis hogy az adat eltarthatósága plusz a migrációs idő meghaladja-e a CRQC-ig becsült időt. Azok az eszközök, ahol az egyenlőtlenség a legélesebb, a hosszú életű érzékeny adatok olyan infrastruktúrán, amelynek migrálása évekbe telik, a sor elejére kerülnek. A rövid adatélettartamú vagy már modernizált infrastruktúrával rendelkező eszközök később ütemezhetők a programban.

Ez az a fázis, ahol az igazgatóság kockázati étvágya a leginkább látható. A Q-érték, amelyre az intézmény tervezni választ, valójában stratégiai fogadás a kvantumhardver fejlődésének ütemére. Egy konzervatív Q (2030-as évek közepe) agresszívabb migrációs tervet és magasabb rövid távú tőkesort eredményez. Egy optimista Q (2040 utáni) lazább tervet és magasabb, a már begyűjtött adatokra vonatkozó fennmaradó kitettséget eredményez. Egyik sem hibás; mindkettőnek az igazgatóság kifejezett döntésének kell lennie, nem a technológiai funkció burkolt alapértelmezésének.

### Harmadik fázis: hibrid telepítés

Miután a prioritásos eszközöket azonosították, a telepítésnek a Project Leapben bizonyított, és az NCSC, az ANSSI, a BSI, valamint a G7 ütemterv által támogatott hibrid mintát kell követnie. A hibrid telepítés egy klasszikus algoritmust és egy posztkvantum algoritmust futtat párhuzamosan, kimeneteiket egyetlen borítékba egyesítve. A kompozit biztonságos mind a klasszikus támadásokkal szemben (a klasszikus algoritmus ma kitart), mind a kvantumtámadásokkal szemben (a PQC-algoritmus holnap kitart). Konkrétan a gyakori minta az X25519 kombinálva ML-KEM-768-cal vagy ML-KEM-1024-gyel a kulcs-enkapszulációhoz, valamint az ECDSA kombinálva ML-DSA-val az aláírásokhoz, ahol a kettős aláírás működésileg megvalósítható.

A Project Leap azon megállapítása, hogy a hibrid „sokkal, de sokkal nehezebb”, mint bármelyik tiszta megközelítés, az őszinte ellensúlya ennek az ajánlásnak. Az igazgatóságoknak számítaniuk kell a számítási és tárolási kapacitás növekedésére, hosszabb kézfogásokra és a tanúsítványlánc további bonyolultságára az átmenet során. A kompromisszum az, hogy a hibrid megszünteti a migrációs kockázat legnagyobb forrását: a szakadékszerű átállást az egyik kriptográfiai alapról a másikra egy éles környezetben.

## Mennyibe kerül ez, és miért kerül többe a tétlenség

A Mastercard elemzése, amelyről [2026 elején számoltak be ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), a globális pénzügyi szektor PQC-migrációs költségét 28-42 milliárd dollárra tette. Ezen aggregátumon belül a tényleges intézményi kiadásokat követő [RedCompass Labs és CMORG kutatás ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") arra utal, hogy az első vonalbeli bankok évi 20-30 millió dollárt fordítanak felkészülési programokra, több vezetői cikluson átívelő megvalósítási határidőkkel. Ezek jelentős számok. Mégsem ezek a releváns összehasonlítás.

A releváns összehasonlítás egyetlen visszamenőleges visszafejtési esemény költsége. Egy olyan intézmény számára, amelynek begyűjtött utalási forgalma, M&A levelezése vagy partnerkockázati kitettségi adatai 2032-ben olvashatóvá válnak egy ellenfél számára, a működési és reputációs költséget nem a migrációs tőkeköltség sora korlátozza. Hanem a mögöttes évtizednyi stratégiai információ értéke korlátozza, amely bármely rendszerszinten fontos intézmény esetében érdemben nagyobb bármely elképzelhető migrációs költségvetésnél. A G7 megfogalmazása, amely a kriptográfiai átállást inkább rendszerszintű kockázatkezelési kérdésként, mintsem technológiai fejlesztésként kezeli, helyes, és az igazgatóságoknak ezen az alapon kell foglalkozniuk vele.

Van egy második költségsor is, amelyet érdemes elkülöníteni. A PQC-re való migráció kényszerítő funkció a kriptográfiai agilitás számára: az architekturális képesség a kriptográfiai algoritmusok cseréjére anélkül, hogy újra kellene építeni a tőlük függő rendszereket. A legtöbb intézmény jelenleg nem rendelkezik kriptográfiai agilitással; RSA- és ECC-függőségeik mélyen beágyazódtak a PKI-kba, a kódaláíró láncokba, a beszállítói integrációkba és az évtizedek alatt felhalmozódott egyedi protokollokba. Az agilitásba tett befektetés, amelyet a PQC-átállás nyomása alatt hajtanak végre, tartós. Ismét igénybe veszik majd, amikor a következő kriptográfiai átállás megérkezik, legyen az a rácsalapú PQC utódja, egy kvantumkulcs-elosztási (QKD) réteg, vagy valami, ami még nincs a szabványosítási ütemterven. Helyesen kezelve a PQC-migráció tőkeköltsége egyszeri befektetés, amely visszatérő opcionalitást hoz.

## Következtetés

A posztkvantum migráció 2026-os igazgatósági szintű prioritásként való kezelése melletti érv nem egy CRQC közelségén alapul. Ennek becslései valóban bizonytalanok maradnak: hiteles tudományos vélemény a 2028-ig bekövetkező CRQC valószínűségét jóval egy százalék alá teszi, amely 2037-2040-re nagyjából ötven százalékra emelkedik. Az érv három másik megfigyelésen alapul, amelyek nem bizonytalanok.

Először, a harvest-now-decrypt-later ma is zajlik, és az egy évtizeden túli bizalmassági követelménnyel rendelkező adatok ki vannak téve, függetlenül attól, mikor érkezik a CRQC. Másodszor, egy nagy pénzügyi intézmény kriptográfiai állományának migrálása öt-hét évet vesz igénybe még megfelelő finanszírozás és vezetői összpontosítás mellett is, ami azt jelenti, hogy a 2026-ban megkezdett program 2031 körül fejeződik be, ami jóval a CRQC-valószínűség-eloszlás konzervatív végén belül van. Harmadszor, a szabályozói elvárások érdemben megkeményedtek az elmúlt tizenkét hónapban, és azok az intézmények, amelyek 2026-os igazgatósági jegyzőkönyvei egyértelmű PQC-programot rögzítenek, érdemben erősebb helyzetben lesznek, mint azok, amelyek jegyzőkönyvei csupán megfigyelői állást rögzítenek.

A most kezdő intézményeknek megvan a választás előnye. Ütemezhetik a munkát a vezetői ciklusokon át, integrálhatják a tágabb ellenállóképességi kezdeményezésekkel, és a hibrid telepítés működési költségeit a normál tőketervezésen belül nyelhetik el. Azok az intézmények, amelyek várnak, ugyanezzel a munkával szembesülnek majd szorosabb határidők mellett, kevesebb ütemezési mozgástérrel, és a PQC-képes hardver, a szakértelem és a beszállítói kapacitás ellátási korlátainak hátterében. A korai cselekvés költsége ismert; a késői cselekvés költsége pontosan úgy aszimmetrikus, ahogy a kockázatkezelés azt elkerülni hivatott.

E webhely korábbi kontextusához: a [2026. áprilisi cikk a kvantumküszöb-kompresszióról](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") a mögöttes hardverpályát vizsgálta, a [CRYSTALS-Kyber 2023. novemberi elemzése](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") a ma ML-KEM-ként szabványosított matematikai alapokat tárgyalta, a [Quantum Key Distributionről szóló 2023. decemberi cikk](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") a kiegészítő [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) réteget vizsgálta, a [KyberLib nyílt forráskódú referencia-implementáció](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") pedig működő Rust-implementációt biztosít az alapul szolgáló primitívekhez azon intézmények számára, amelyek közvetlenül szeretnék megvizsgálni a kriptográfiai felületet. A gyakorlati és technikai részletekkel való foglalkozás, nem csupán a szabályozói címsorokkal, az a mód, ahogyan az igazgatóságok megkülönböztetik a hiteles migrációs programokat a megfelelőségi színjátéktól.

## Gyakran ismételt kérdések

**Mikor fog valójában létezni egy kriptográfiailag releváns kvantumszámítógép?**

A hiteles becslések széles skálán mozognak. 2026 elején a nyilvános kvantumdemonstrációk nagyjából 24-28 logikai qubitet értek el, míg egy CRQC becslések szerint körülbelül 6000 logikai qubitet igényel, amelyet 100 000 és több millió közötti fizikai qubit támogat, a hibajavítási megközelítéstől függően. A szakértői konszenzus a CRQC valószínűségét 2028-ig egy százalék alá, 2037-2040-re nagyjából ötven százalékra teszi, jelentős változékonysággal az előrejelzések között. Az elméleti erőforrás-becslések közelmúltbeli csökkenései: néhány évvel ezelőtti 20 millió qubitről Gidney 2025-ös munkájában egymillió alá, a 2026. februári QLDPC-architektúra tanulmányban pedig nagyjából 100 000-re, összenyomták a tervezési horizontot. Igazgatósági célokra a megfelelő tervezési feltételezés a 2030-as évek közepe a magas kockázatú rendszerekhez, a 2030-as évek vége konzervatív középpontként, és korábbi, ha a HNDL-kitettség a meghatározó aggály.

**Miért hibrid telepítés a tiszta posztkvantum helyett?**

Három ok. Először, az ML-KEM és az ML-DSA, bár jól átvizsgáltak, rövidebb kriptoanalitikai múlttal rendelkeznek, mint az RSA és az ECC. Egy hibrid séma biztonságos marad, ha bármelyik összetevő kitart; egy tiszta PQC-séma ki van téve, ha a rácsproblémát váratlanul meggyengítik. Másodszor, a hibrid megőrzi a visszafelé kompatibilitást azokkal a partnerekkel, amelyek még nem migráltak, ami kritikus egy többéves iparági átmenetben. Harmadszor, az Australian Signals Directorate-en kívül minden nagyobb hatóság kifejezetten hibridet ajánl az átmeneti időszakra: az NCSC, az ANSSI, a BSI, az NLNCSA és a G7 keretrendszer mind támogatja a kettős boríték megközelítést. A kompromisszum, ahogy a Project Leap számszerűsítette, érdemben magasabb számítási és tárolási többletterhelés. Ez az opcionalitás ára.

**Szükségünk van mind az ML-KEM-re, mind az ML-DSA-ra, vagy választhatunk egyet?**

Mindkettőre. Az ML-KEM és az ML-DSA különböző kriptográfiai szerepeket tölt be. Az ML-KEM a kulcslétrehozási primitíveket helyettesíti a TLS-ben, a VPN-ekben, a mobilhitelesítésben és hasonló protokollokban, ahol két félnek meg kell állapodnia egy megosztott szimmetrikus kulcsban. Az ML-DSA a digitális aláírási primitíveket helyettesíti a PKI-tanúsítványokban, a kódaláírásban, a dokumentumaláírásban, a SWIFT-stílusú hitelesített üzenetküldésben és az identitásállításokban. Egy intézmény kriptográfiai állománya mindkét fajta primitívet használja különböző helyeken; a migrációnak mindkettőt kezelnie kell. Az ML-DSA jelentősen nagyobb aláírásmérete (az ECDSA 50-70-szerese) általában a kettő közül a működésileg igényesebb; az ML-DSA hálózati és tárolási tervezési munkája uralja a legtöbb migrációs kapacitásfelmérést.

**Hogyan mérjük az előrehaladást egy ekkora programon?**

Három mérőszám gyakorlatias, és igazodik a nagyobb szabályozói keretrendszerekhez. **A CBOM lefedettsége**: az intézmény aszimmetrikus kriptográfiai előfordulásainak hány százalékát leltározták, osztályozták és jelölték meg migrációs prioritásként. **A magas kockázatú eszközök migrációs lefedettsége**: azon eszközök hány százalékát vitték át hibrid PQC-re, ahol Mosca S + M > Q feltétele fennáll. **A kriptográfiai agilitás lefedettsége**: a kriptográfiai függőségű rendszerek hány százaléka képes algoritmust cserélni kódmódosítás nélkül, kizárólag konfigurációval. A G7 CEG ütemterve, az NCSC háromfázisú keretrendszere és az EU összehangolt ütemterve mind nagyjából e három mérőszámra képezhető le, még ahol eltérő terminológiát használnak is.

**Mennyibe kerül még egy év várakozás?**

Nem nulla, és nem szimmetrikus. Egy év várakozás egy évnyi HNDL-védelmet veszít el a hosszú életű adatokon: az az adat, amelynek bizalmassági követelménye 2040-ig terjed, a szükségesnél egy évvel tovább van kitéve. Összenyomja a migrációs ablakot a rögzített szabályozói határidőkkel szemben (ASD 2030, NSA CNSA 2.0 mérföldkövek, EU 2030-as kritikus rendszerek célkitűzése), ami magasabb szállítási kockázatot és csökkentett ütemezési rugalmasságot jelent. Kiteszi az intézményt a beszállítói és tehetség-ellátási korlátoknak, amelyek már láthatók a piacon, és amelyek súlyosbodnak majd, ahogy az iparág legnagyobb szereplői a tervezésből a végrehajtásba lépnek. A költség egyetlen évben sem katasztrofális, de halmozódik, és a szabályozói környezet egy olyan álláspont felé konvergál, ahol az igazgatóságoktól elvárják majd, hogy a késedelmet magyarázzák, ne a kiadást.

## Hivatkozások

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement, January 2026"). GOV.UK.
- Bank for International Settlements, (2025). [Project Leap Phase 2: Quantum-Proofing Payment Systems ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"). BIS.
- Bank for International Settlements, (2025). [Project Leap: Quantum-Proofing the Financial System ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"). BIS.
- NIST, (2024). [FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard"). NIST.
- UK NCSC, (2025). [Timelines for Migration to Post-Quantum Cryptography ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines "Timelines for migration to post-quantum cryptography — NCSC"). UK National Cyber Security Centre.
- CMORG, (2025). [Guidance for Post-Quantum Cryptography ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"). Cross-Market Operational Resilience Group.
- Post-Quantum Cryptography Coalition, (2025). [International PQC Requirements ⧉](https://pqcc.org/international-pqc-requirements/ "International PQC Requirements — Post-Quantum Cryptography Coalition"). PQCC.
- PQShield, (2025). [PQC Roadmaps and Transition Guidance ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"). PQShield.
- Banking.Vision, (2026). [The Year of Quantum Computing: 2026 ⧉](https://banking.vision/en/the-year-of-quantum-computing/ "The Year of Quantum Computing 2026"). Banking.Vision / msg for banking.
- The Quantum Insider, (2026). [How to Prep For Post-Quantum Cryptography: G7 Releases Roadmap ⧉](https://thequantuminsider.com/2026/01/15/how-to-prep-for-post-quantum-crytography-g7-releases-roadmap-to-help-financial-sector-navigate-transition-to-quantum-era/ "How to Prep For Post-Quantum Cryptography — The Quantum Insider"). The Quantum Insider.
- Quantum Computing Report, (2026). [Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates ⧉](https://quantumcomputingreport.com/shor-qldpc-codes-and-the-compression-of-rsa-2048-resource-estimates-part-i/ "Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates"). Quantum Computing Report.
- Cryptomathic, (2025). [A Banker's Guide to Quantum Safe Cryptography — Roadmap to PQC Migration for Financial Institutions ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography"). Cryptomathic.
- Forrester, (2025). [2026 Asia Pacific Predictions: Quantum Security ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"). Forrester Research.
- The Asian Banker, (2025). [Building Resilience for a Quantum-Ready Financial System ⧉](https://www.theasianbanker.com/updates-and-articles/building-resilience-for-a-quantum-ready-financial-system "Building resilience for a quantum-ready financial system"). The Asian Banker.
