---
title: "DORA, az EU AI Act és az adatszuverenitás: a bankok 2026-os megfelelőségi stackje"
tags: "DORA, EU AI Act, data sovereignty, operational resilience, cloud concentration risk, AI governance, ISO 20022, post-quantum cryptography, AI, platform engineering, sovereign cloud, cloud native banking, cross-border payments"
subtitle: "A 2026-os megfelelőségi stack nem szabályzati dosszié. Olyan adat-, felhő-, MI- és működési ellenállóképességi architektúra, amely nyomás alatt is képes bizonyítani a kontrollt."
description: "A DORA, az EU AI Act, a GDPR, a felhőkoncentrációs kockázat és az adatszuverenitás egyetlen 2026-os megfelelőségi stackké olvad össze a bankok számára."
date: "May 28, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/akande-voice-assistant-office-1200.webp"
banner_alt: "Megfelelőségi stack diagram, amely a DORA ellenállóképességet, az EU AI Act átláthatóságot, az adatszuverenitást, a felhőkoncentrációs kockázatot, az auditnaplókat, a modellirányítást és a harmadik feles szolgáltatókat ábrázolja"
keywords: "DORA 2026, EU AI Act 2026, adatszuverenitás bankok, működési ellenállóképesség, felhőkoncentrációs kockázat, pénzügyi szolgáltatások MI-megfelelőség, magas kockázatú MI"
---

## DORA, az EU AI Act és az adatszuverenitás: a bankok 2026-os megfelelőségi stackje

A 2026-os uniós megfelelőségi stack már nem előretekintő téma. A DORA 2025. január 17. óta aktív jogérvényesítés alatt áll. Az EU AI Act magas kockázatú kötelezettségei 2026. augusztus 2-án lépnek teljes hatályba, nyolc héttel e cikk megjelenésének dátuma után. A Schrems II és az EU-USA adatvédelmi keret (Data Privacy Framework) a határon átnyúló adattovábbítás működési valósága, nem jövőbeli aggodalom. A felhőkoncentrációs kockázat az EBA kiszervezési perimeterén belül helyezkedik el az [EBA/GL/2019/02 ⧉](https://www.eba.europa.eu/regulation-and-policy/internal-governance/guidelines-on-outsourcing-arrangements "EBA Guidelines on Outsourcing Arrangements") és a DORA kritikus harmadik feles szolgáltató (CTPP) kijelölési rendszerén keresztül. Azok az intézmények, amelyek ezt még mindig "felkészülési" napirendként keretezik, már két szabályozási ciklust elveszítettek.

---

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - **A DORA auditfázisban van.** A [2022/2554 (EU) rendelet ⧉](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R2554 "DORA — Digital Operational Resilience Act") 6. cikke (IKT-kockázatkezelési keret), 8. cikke (információs nyilvántartás), 18. cikke (incidensbejelentés), 26. cikke (fenyegetésvezérelt behatolásvizsgálat) és a 28-44. cikkek szerinti CTPP-rendszer 16 hónapja hatályban van. A felügyeleti elvárások most már formális vizsgálati megállapítások, nem tanácsadói kommentárok.
> - **Az EU AI Act magas kockázatú határideje 2026. augusztus 2.** A III. melléklet 5(b) pontja a hitelképesség-pontozásra vonatkozik; az 1. pont az ügyfélbelépéskori biometrikus azonosításra; a 7. pont az élet- és egészségbiztosítás kockázatértékelésére. A 16-29. cikkek kötelezettségei, azaz a kockázatkezelés, adatirányítás, műszaki dokumentáció, nyilvántartás-vezetés, átláthatóság, emberi felügyelet, pontosság és kiberbiztonság, e naptól alkalmazandók.
> - **A határon átnyúló adattovábbítás SCC + TIA, nem homályos "adatszuverenitás".** Általános szerződési feltételek (SCC), adattovábbítási hatásvizsgálatok (TIA), kiegészítő intézkedések ott, ahol a TIA azt mutatja, hogy szükségesek. A DPF csak a DPF-tanúsított egyesült államokbeli címzettekre terjed ki; minden más továbbra is SCC + TIA szükséges. Az ír adatvédelmi biztos, a CNIL és a Garante egyaránt hozott jogérvényesítési határozatokat 2025-ben.
> - **A felhőkoncentráció mérnöki munka, nem deklaráció.** Több régiós active-active a kritikus szolgáltatásokhoz; dokumentált kilépési terv tesztelt végrehajtási bizonyítékkal; helyettesíthetőségi értékelések szolgáltatási szint szerint; olyan harmadik feles IKT-nyilvántartás, amely egyeztethető a felhőszolgáltató saját szolgáltatási leltárával. Az EBA/GL/2019/02 81. bekezdését ellenőrzik az auditorok.
> - **A 2026-os megkülönböztető tényező a futásidőbe kötött policy-as-code.** Az Open Policy Agent DORA-alapú szabályok szerint kapuzza a produkciós telepítéseket; megváltoztathatatlan auditnaplók táplálják a 8. cikk szerinti nyilvántartás bizonyítékait; MI-rendszerleltár III. melléklet szerinti besorolással a CI/CD folyamatban megjelenítve. Bizonyíték a munkafolyamat sebességén, nem a vizsga előtti héten összeállított PDF-ekben.
>
---

## Miért 2026 az auditfázis éve

Három szabályozási rendszer csap a működési valóságba egyszerre.

**DORA jogérvényesítés (2025. január 17-től).** Az európai felügyeleti hatóságok (EBA, EIOPA, ESMA) 2024 folyamán tették közzé a végleges RTS-t és ITS-t, a CTPP kijelölési rendszer 2025 elején nyílt meg, és az elsődleges (tier-1) bankok 2025 folyamán végig nyújtottak be 18. cikk szerinti incidensjelentéseket a 4 órás kezdeti értesítési szabály alapján. Az ESA-k közös TLPT-kerete, formálisan a DORA 26. cikkéhez igazított [TIBER-EU keret ⧉](https://www.ecb.europa.eu/paym/cyber-resilience/tiber-eu/html/index.en.html "TIBER-EU — Threat Intelligence-based Ethical Red Teaming"), az alapja a legtöbb G-SIB által ma futtatott fenyegetésvezérelt behatolásvizsgálati programnak. Az első felügyeleti vizsgálati hullám megállapításai 2025 negyedik negyedévében kezdtek megérkezni.

**EU AI Act fokozatos alkalmazás.** A rendelet 2024. augusztus 1-jén lépett hatályba. A tiltott gyakorlatokra vonatkozó rendelkezéseket 2025. február 2-ától; az általános célú MI-kötelezettségeket 2025. augusztus 2-ától; a magas kockázatú rendszerek kötelezettségeit **2026. augusztus 2-ától** kell alkalmazni. Ez az a határidő, amely a bankok szempontjából számít. A legtöbb tier-1 intézménynek legalább egy III. melléklet szerinti rendszere van produkcióban: hitelképesség-pontozás (5b pont), ügyféllel érintkező biometrikus azonosítás (1. pont) vagy élet- és egészségbiztosítási kockázatértékelés (7. pont). A 16-29. cikkek szerinti kötelezettségek, azaz a kockázatkezelés, adatirányítás, műszaki dokumentáció, nyilvántartás-vezetés, átláthatóság, emberi felügyelet, pontosság, robusztusság és kiberbiztonság, ettől az egyetlen dátumtól alkalmazandók, lágy átmeneti időszak nélkül.

**Schrems II működési rendeződés.** Az Európai Unió Bíróságának Schrems II ítélete (2020. július) érvénytelenítette a Privacy Shieldet, és az SCC-ket érvényesnek tekintette, feltéve, hogy kiegészítő intézkedések alkalmazandók ott, ahol a TIA a védelmet elégtelennek mutatja. Az Európai Bizottság 2023 júliusában fogadta el az EU-USA adatvédelmi keretet (DPF), amely kizárólag a DPF-tanúsított egyesült államokbeli címzettek számára biztosít adattovábbítási mechanizmust. Minden más továbbra is SCC-t és dokumentált TIA-t igényel. A CNIL francia közigazgatási Microsoft 365-telepítésekre vonatkozó jogérvényesítési határozatai, az ír adatvédelmi biztos 1,2 milliárd eurós, a Meta ellen 2023 májusában kiszabott bírsága, valamint a Garante OpenAI elleni 2024-es intézkedései megalapozták a felügyeleti mintázatot: a TIA-kat vizsgálják, a kiegészítő intézkedéseket alaposan ellenőrzik, és a puszta "SCC-ket használunk" állítás önmagában nem elegendő.

A 2026-os intézményi kérdés nem az, hogy alkalmazandó-e az egyes rendszerek mindegyike. Az, hogy a megfelelőségi bizonyíték, amelyet az intézmény a vizsgálati ellenőrzés alatt produkál, összeáll-e.

## A DORA auditfázisban: cikkspecifikus mechanika

Azok a cikkek, amelyek 2026-ban felügyeleti megállapításokat eredményeznek:

### 6. cikk: IKT-kockázatkezelési keret

A keretet dokumentálni kell, a vezető testületnek jóvá kell hagynia, legalább évente felül kell vizsgálni, és integrálni kell az intézmény átfogó kockázatkezelési keretébe. A felügyeletek a következőket vizsgálják: explicit kockázati tolerancia-nyilatkozatok IKT-kockázati kategóriánként; dokumentált információbiztonsági szabályzat; meghatározott szerepek és felelősségek a második és harmadik védelmi vonalon; számszerűsített éves IKT-kockázatértékelés, amely az intézmény kockázati étvágyát vezérli. A 2026 eleji megállapítások mintázata: olyan intézmények, amelyek IKT-kockázati taxonómiája nem egyeztethető a 18. cikk szerinti incidensbejelentési taxonómiájukkal.

### 8. cikk: Információs nyilvántartás (harmadik feles IKT)

A nyilvántartásnak tartalmaznia kell minden IKT-szolgáltatás igénybevételéről szóló szerződéses megállapodást. Az [információs nyilvántartásról szóló ITS ⧉](https://www.eba.europa.eu/activities/direct-supervision-and-oversight/digital-operational-resilience-act "ESAs ITS on Register of Information") szerinti kötelező mezők közé tartozik a támogatott funkció, a kritikussági besorolás, az adatfeldolgozás és -tárolás helye, az alvállalkozói lánc és a kilépési stratégia értékelése. A 31. cikk szerinti CTPP kijelölési rendszer az EU-szerte olvassa a nyilvántartásokat annak azonosítására, hogy mely harmadik felek lépik át a rendszerszintű küszöböt. Egy hiányos vagy inkonzisztens 8. cikk szerinti nyilvántartás most már egyszerre egyedi megállapítás és a CTPP-perimeter integritási kockázata.

### 18. cikk: IKT-vel kapcsolatos incidensbejelentés

A jelentős IKT-vel kapcsolatos incidensek 4 órás kezdeti értesítési ablaka az, ami az intézményeket megfogja. A "jelentős" besorolási kritériumai a 18. cikk (3) bekezdését és a technikai RTS-t követik: az érintett ügyfelek száma, földrajzi kiterjedés, adatvesztés, gazdasági hatás, reputációs hatás, az érintett szolgáltatások kritikussága, időtartam. A kiforrott incidenskezelési folyamatokat futtató bankok is küzdenek az első órás besorolási döntéssel. A mérnöki teljesítmény: egy automatizált súlyosság-besorolási segéd az incidenskezelési platformba kötve, amely az első reagálási cikluson belül, nem egy triázs-megbeszélés után állít elő 18. cikk szerinti döntési indoklást.

### 26. cikk: Fenyegetésvezérelt behatolásvizsgálat

A TLPT az illetékes hatóság által kijelölt pénzügyi szervezetekre vonatkozik, az intézmény kritikus vagy fontos funkciói szerint körvonalazva. A vizsgálatnak követnie kell a TIBER-EU módszertant (vagy egy egyenértékű nemzeti keretet), fenyegetettségi hírszerzést kell használnia a támadási forgatókönyvek felépítéséhez, és legalább háromévente le kell futnia. A szolgáltatók bevonását a 27. cikk (szolgáltatóválasztás) és a 28. cikk (tesztvégrehajtás) szabályozza. A 2026-os felügyeleti kérdés: az intézmény TLPT-hatóköre magában foglalja-e a nyilvános felhőben tárolt kritikus funkcióit, és a szolgáltató bevonási modellje tisztán kezeli-e a felhőszolgáltató saját biztonsági határait?

### 28-44. cikk: Kritikus harmadik feles szolgáltatók

A CTPP-rendszer az a felügyeleti innováció, amely a leginkább közvetlenül érinti a felhőstratégiát. Az AWS, a Microsoft (Azure), a Google (GCP), a Salesforce, a Workday és néhány más stratégiai szolgáltató a kijelölési perimeteren belül vagy annak közelében helyezkedik el. A kijelölés az ESA-k közvetlen felügyeletét váltja ki, beleértve az információkérés jogát, a helyszíni ellenőrzéseket és a felügyeleti ajánlásokat. A tier-1 bankok számára ez azt jelenti: a felhőszolgáltatói koncentráció most már szabályozott felügyeleti mérőszám, nem csupán belső kockázatkezelési aggály.

## Az EU AI Act architektúrája a magas kockázatú banki rendszerekhez

A fokozatos alkalmazás idővonala:

| Dátum | Rendelkezések | Banki vonatkozás |
|---|---|---|
| 2024. augusztus 1. | Hatálybalépés | Indul a visszaszámláló óra |
| 2025. február 2. | Tiltott gyakorlatok (5. cikk) | Társadalmi pontozás jellegű rendszerek tiltva |
| 2025. augusztus 2. | Általános célú MI-kötelezettségek (V. fejezet) | A GPAI-modellszolgáltatókra dokumentációs és szerzői jogi kötelezettségek vonatkoznak |
| **2026. augusztus 2.** | **Magas kockázatú rendszerek kötelezettségei (16-29. cikk)** | **A III. melléklet szerinti rendszereknek teljesíteniük kell a teljes megfelelőségi keretet** |
| 2027. augusztus 2. | Más szabályozott termékekkel integrált magas kockázatú rendszerek | Az I. melléklet szerinti termékbiztonsági rendszerekkel integrált banki rendszerek |

A III. melléklet azon rendelkezései, amelyek a legerősebben érintik a bankokat:

- **III. melléklet 1. pont: Biometrikus azonosítás és kategorizálás.** Az ügyfélbelépéskori biometrikus egyeztetés (pl. élőségérzékelés és okmányfotó-egyeztetés) magas kockázatúnak minősül, ha azonosításra, nem pedig egyetlen személynek egy állítással szembeni ellenőrzésére használják. A megkülönböztetés működési szempontból lényeges: egy bejelentett identitással szembeni egyeztetés ellenőrzés; adatbázissal szembeni egyeztetés azonosítás.
- **III. melléklet 5(b) pont: Hitelképesség-értékelés.** Bármely rendszer, amelyet természetes személyek hitelképességének értékelésére vagy hitelpontszámuk megállapítására használnak, hatókörbe tartozik. Ez lefedi a lakossági hitelkártya-pontozást, a jelzáloghitel-indítási pontozást, a BNPL-hitelbírálatot és a kkv-hitelezési döntéshozatalt, ahol természetes személyek az alanyok. Kizárja a pénzügyi csalást észlelő rendszereket (58. preambulumbekezdés).
- **III. melléklet 5(c) pont: Kockázatértékelés és árazás az élet- és egészségbiztosításban.** Az élet- vagy egészségbiztosítási termékeken bírálati modelleket futtató bankbiztosítási egységek e ponton belül vannak, még akkor is, ha az anyabank lakossági hitelezési tevékenysége is hatókörbe tartozik az 5(b) pont alatt.
- **III. melléklet 7. pont: Igazságszolgáltatás és demokratikus folyamatok.** Rendszerint nem banki relevanciájú, de érdemes megerősíteni azon intézmények esetében, amelyek bírósági fizetési vagy igazságügyi számlavezetési szolgáltatásokat nyújtanak.

A 16-29. cikkek kötelezettségeinek összefoglalása:

- **Kockázatkezelési rendszer (9. cikk).** Folyamatos, iteratív folyamat a rendszer teljes életciklusán át, írásban dokumentálva.
- **Adatok és adatirányítás (10. cikk).** A tanító-, validáló- és tesztadatok adatirányítási és kezelési gyakorlatoknak vannak alávetve, beleértve a relevanciát, reprezentativitást, teljességet és a torzítások értékelését.
- **Műszaki dokumentáció (11. cikk) és nyilvántartás-vezetés (12. cikk).** Automatikus eseménynaplózás magából a rendszerből, a rendszer céljához igazodó időszakokra megőrizve.
- **Átláthatóság az alkalmazók felé (13. cikk).** Használati utasítások, amelyek lehetővé teszik az alkalmazók számára a rendszer kimenetének értelmezését.
- **Emberi felügyelet (14. cikk).** Beépített intézkedések, amelyek lehetővé teszik természetes személyek számára a felügyeletet, beleértve a rendszer felülbírálásának vagy leállításának képességét.
- **Pontosság, robusztusság, kiberbiztonság (15. cikk).** A használati utasításokban közzétett teljesítménymutatók; ellenállóképesség az ellenséges bemenetekkel szemben; torzításkorrekció működés közben.

A 2026 augusztusi felügyeleti kérdés: elő tud-e állítani a bank egy VI. melléklet szerinti megfelelőségértékelést minden produkcióban lévő III. melléklet szerinti rendszerhez? Azoknak az intézményeknek, amelyek az SR 11-7 / SS1/23 szerint kiépített modellkockázat-kezelési kereteket alakítottak ki, a legtöbb bemenet már megvan; a munka a meglévő kontrollok leképezése az AI Act 9-15. cikk szerinti bizonyítékkategóriáira.

## Az adatszuverenitás mint mérnöki fegyelem

A 2026-os működési adatszuverenitási modell:

**Általános szerződési feltételek (2. vagy 3. modul, az alkalmazandó szerint).** A 2021/914 (EU) bizottsági határozattal elfogadott frissített SCC-k az alapvonal. A 2021 előtti SCC-k türelmi időt kaptak; 2026-ban való használatuk megállapítást von maga után.

**Adattovábbítási hatásvizsgálat.** Minden nem megfelelő védelmi szintű harmadik országba történő továbbításnál dokumentálni kell: a címzett ország adatvédelem szempontjából releváns jogszabályait és gyakorlatait; hogy ezek a jogszabályok lehetővé teszik-e a hatósági hozzáférést egy demokratikus társadalomban szükségeset és arányosat meghaladó mértékben; a konkrét továbbított adatokat; az alkalmazott technikai és szervezési kiegészítő intézkedéseket. Az EDPB [01/2020. sz. ajánlása ⧉](https://www.edpb.europa.eu/our-work-tools/our-documents/recommendations/recommendations-012020-measures-supplement-transfer_en "EDPB Recommendations 01/2020 — Supplementary Measures") adja a keretet.

**EU-USA adatvédelmi keret tanúsítás-ellenőrzés.** A DPF-tanúsított egyesült államokbeli címzettek a megfelelőségi határozat alapján SCC + TIA nélkül fogadhatnak adattovábbítást. Ellenőrzés: a címzett [DPF-tanúsítási oldala ⧉](https://www.dataprivacyframework.gov/list "Data Privacy Framework List") plusz az ellenőrzés dátumának belső nyilvántartása. A DPF 2024-ben túlélte első éves felülvizsgálatát; hosszabb távú tartóssága továbbra is élő kérdés.

**Kiegészítő intézkedések ott, ahol a TIA azt mutatja, hogy szükségesek.** Álnevesítés a továbbítás előtt, titkosítás az EU-ban tartott kulcsokkal, megosztott feldolgozás vagy továbbítás aggregálás után. A 2025-ös jogérvényesítési mintázat: a CNIL francia közigazgatási Microsoft 365-re vonatkozó megállapításai arra összpontosultak, hogy a Connected Experiences kikapcsolása és az EU Data Boundary bérlőelhelyezés konfigurálása elegendő kiegészítő intézkedésnek minősül-e.

**Felhőszolgáltatói EU Data Boundary mechanizmusok.** Az AWS European Sovereign Cloud, a Microsoft EU Data Boundary, a Google Cloud EU szuverenitási csomag, valamint a szuverén felhő partnerségek (Bleu / Capgemini-Orange, Delos Cloud, Oracle EU Sovereign Cloud) mind megpróbálják platformszinten megtervezni az adatszuverenitási garanciákat. Egyik sem szünteti meg az SCC + TIA követelményt; a TIA maradványkockázati felületét csökkentik.

## Felhőkoncentráció a DORA és az EBA kiszervezési iránymutatások alatt

A DORA CTPP-rendszer és az EBA kiszervezési iránymutatások egymásra rétegződnek:

Az [EBA/GL/2019/02 ⧉](https://www.eba.europa.eu/regulation-and-policy/internal-governance/guidelines-on-outsourcing-arrangements "EBA Outsourcing Guidelines") 64. bekezdése megköveteli az intézményektől, hogy biztosítsák, hogy a kritikus vagy fontos kiszervezési megállapodások ne rontsák az intézmény érdemi jelenlétét az EU-ban, a vezetés általi felügyeletet, vagy a kiszervezett funkcióval kapcsolatos döntéshozatali képességet. A 81. bekezdés helyettesíthetőségi értékeléseket ír elő. A 113-117. bekezdések a kilépési stratégia dokumentációját fedik le, amelyet a felügyeletek ténylegesen vizsgálnak.

A DORA 28. cikke hozzáadja a kritikus vagy fontos funkciókat támogató IKT-harmadikfeles megállapodások szerződéses tartalmi követelményeit: adathozzáférhetőség, adatbiztonság, adatrezidencia, auditjogok, kilépési stratégiák és folytonossági rendelkezések.

A CTPP-rendszer ezután mindkettő felett helyezkedik el: ha egy harmadik fél átlépi a kijelölési küszöböt, az ESA-k közvetlen felügyeleti jogkört szereznek. A mérnöki következmények földrajzi és architekturális tervezési döntésekről szólnak: több régiós active-active a kritikus szolgáltatásokhoz; dokumentált kilépési tervek időszakos végrehajtási tesztekkel (nem csak asztali gyakorlatokkal); harmadik feles IKT-nyilvántartások, amelyek egyeztethetők a felhőszolgáltató saját szolgáltatási leltárával.

## Mit jelent ez banktípusonként

### Globálisan rendszerszinten jelentős bankok

A megfelelőségi perimeter most már architektúraprobléma. A befektetés nem egy újabb szabályzatfrissítés, hanem az a policy-as-code platform, amely a DORA-alapú szabályokat a CI/CD folyamatba köti, az MI-rendszerleltár, amely telepítéskor megjeleníti a III. melléklet szerinti besorolást, a harmadik feles IKT-nyilvántartás, amely automatikusan egyeztethető a beszerzési és a felhő-anyagjegyzék rendszerekkel, valamint a megváltoztathatatlan auditnapló, amely felügyeleti kérésre 8. cikk szerinti nyilvántartási bizonyítékot állít elő. Építsd meg a platformot; az AI Act magas kockázatot követő szabályozási ciklus (valószínűleg egy bővítés az általános célú MI magatartási kódex keretében) örökli az infrastruktúrát.

### Univerzális és középméretű bankok

A pragmatikus tartás a szigorú III. melléklet szerinti leltár. A legtöbb univerzális banknak van egy-két egyértelműen hatókörbe tartozó rendszere (hitelpontozás, jelzáloghitel-indítás, ügyféllel érintkező biometria) és a határesetek hosszú sora. Ha 2026 első félévében három hónapot töltünk azzal, hogy produkcióban lévő MI-rendszerenként védhető III. melléklet szerinti besorolást állítsunk elő, olyan írásos indoklással, amely külső felülvizsgálatot is kiáll, az nagyobb értékű, mint egy újabb kontrollkeret-frissítés. A besorolási munka egyben DORA 6. cikk szerinti IKT-kockázatkezelési bizonyítékként is szolgál az MI-t tartalmazó rendszerekhez.

### Kisebb bankok és lakástakarékpénztárak

A stratégiai válasz a beszállítói átvilágítás a belső fejlesztéssel szemben. Válassz olyan MI-beszállítókat, amelyek közzéteszik a III. melléklet szerinti megfelelőségértékelési dokumentációt, amelyek a szerződéseikben elkötelezik magukat a 9-15. cikk szerinti bizonyítéktámogatás mellett, és amelyek harmadik feles biztonsági akkreditációi összhangban vannak a DORA 28. cikk követelményeivel. Ellenőrizd a beszállítók állításait az MRM-folyamatodon keresztül. A belső hatókör az integráció, a konfiguráció és a működési felügyelet, nem a keretépítés.

### Biztosítók és bankbiztosítási egységek

A III. melléklet 5(c) pontja az élet- és egészségbiztosítási kockázatértékelésről a biztosítási egységeket a magas kockázatú perimeteren belülre helyezi, függetlenül az anyabank kitettségétől. A 2026. augusztusi határidő alkalmazandó. Egyeztess az anyabank AI Act megfelelőségi funkciójával; a legtöbb alapul szolgáló leltár- és bizonyítékmunka közös, és a szabályozási kitettség egyetlen üzletágra jellemző.

### Fintechek, PSP-k és regtechek

A 2026-ban uniós bankokba értékesítő beszállítók termékkérdése már nem "megfelel-e a platformotok a DORA / AI Act előírásainak". Az, hogy "előállítja-e a platformotok azt a dokumentációt, amelyre egy tier-1 bank megfelelőségi funkciójának szüksége van a saját megfelelősége bizonyításához". DORA 8. cikk szerinti nyilvántartási bemenetek, AI Act 11. cikk szerinti műszaki dokumentációs sablonok, SCC + TIA sablonszöveg bármely adattovábbítási megállapodáshoz. Azok a beszállítók, akik használható sablonokkal válaszolnak, megkötik a vállalati üzleteket; azok, akik PDF-ekkel válaszolnak, veszítenek azokkal a versenytársakkal szemben, akik nem.

## A működési modell megtervezése

A 2026-os megkülönböztető tényező a futásidőbe kötött policy-as-code.

**Open Policy Agent a telepítési kapunál.** Minden produkciós telepítés áthalad az OPA-értékelésen a DORA-alapú szabályzattal szemben. Példák: minden ügyféladatot érintő szolgáltatásnak dokumentált 8. cikk szerinti nyilvántartási bejegyzéssel kell rendelkeznie; minden III. melléklet szerinti MI-rendszernek a telepítési jegyzékből hivatkozott megfelelőségértékelési bizonyítékkal kell rendelkeznie; minden harmadik feles IKT-szolgáltatásnak érvényességen belüli helyettesíthetőségi értékeléssel kell rendelkeznie. A szabályzatnyilvántartás Git-verziózott; az elutasított telepítések felülvizsgálható indoklásokat állítanak elő.

**Megváltoztathatatlan auditnaplózás, amely a 8. cikk szerinti bizonyítékot táplálja.** WORM-tárolt telepítési, konfigurációs és hozzáférési események, amelyek visszaegyeztethetők a harmadik feles IKT-nyilvántartással. A "mutassa meg a kontrollokat az X szolgáltatásra Y dátumon" kérdést feltevő felügyeletek lekérdezési eredményt kapnak, nem dokumentum-összeállítási projektet.

**MI-rendszerleltár III. melléklet szerinti besorolással a CI/CD-ben megjelenítve.** Az intézmény leltárában minden MI-rendszer visel egy III. melléklet szerinti besorolást (1., 5(a), 5(b), 5(c), 6., 7. pont vagy egyik sem). A besorolást felülvizsgálják, amikor a rendszer megváltozik; a produkcióba telepítés ellenőrzi, hogy a besorolás aktuális-e. A 9-15. cikk szerinti bizonyítékkategóriák leltármezőkre képződnek le, és a CI/CD folyamat minden kiadás részeként bizonyítékartefaktumokat ír.

**Fenyegetésvezérelt behatolásvizsgálat az SDLC-be kötve.** A TLPT-hatókörök az intézmény kritikus és fontos funkcióinak leltárából származnak; a vizsgálati program folyamatosan fut, nem különálló eseményként háromévente. A megállapítások visszatáplálódnak az OPA-szabályzatnyilvántartásba; a lezárt megállapítások felügyeletre kész bizonyítékcsomagokat állítanak elő.

Azok az intézmények, amelyek a munkafolyamat sebességén állítanak elő bizonyítékot, átmennek a vizsgákon. Azok az intézmények, amelyek adatkérésekre válaszul dokumentációs csomagokat állítanak elő, nem.

## Gyakran ismételt kérdések

**A DORA még mindig "felkészülési" fázisban van 2026-ban?**

Nem. A DORA 2025. január 17. óta aktív jogérvényesítés alatt áll. A 6., 8., 18. és 26. cikk mind hatályban van; a CTPP kijelölési rendszer 2025 és 2026 folyamán nyílik meg; az első vizsgálati hullám felügyeleti megállapításai 2025 negyedik negyedévében érkeztek meg. A "felkészülési" keretezés két szabályozási ciklussal elavult.

**Melyik EU AI Act határidő számít a bankok szempontjából?**

2026. augusztus 2., az a dátum, amikor a 16-29. cikkek kötelezettségei a III. melléklet szerinti magas kockázatú rendszerekre alkalmazandók. A III. melléklet 5(b) pontja a hitelképesség-értékelésről, az 1. pont a belépéskori biometrikus azonosításról, és az 5(c) pont az élet- és egészségbiztosítási kockázatértékelésről a bankrelevanciájú kategóriák. A legtöbb tier-1 banknak legalább egy III. melléklet szerinti rendszere van produkcióban.

**Az adatvédelmi keret megszünteti az SCC-k szükségességét?**

Csak a DPF-tanúsított egyesült államokbeli címzettek esetében. A tanúsítás ellenőrzése az adattovábbítás pillanatában szükséges, plusz egy belső nyilvántartás. Minden más továbbra is SCC-t és dokumentált adattovábbítási hatásvizsgálatot igényel.

**Mi az a mérnöki teljesítmény, amely egy vizsgálaton demonstrálja a DORA-megfelelőséget?**

Policy-as-code, amely a produkciós telepítéseket a DORA-alapú szabályok szerint kapuzza, megváltoztathatatlan auditnaplók, amelyek a 8. cikk szerinti nyilvántartási bizonyítékot táplálják, egy MI-rendszerleltár III. melléklet szerinti besorolással telepítéskor megjelenítve, és egy TLPT-program a kritikus és fontos funkciók leltára szerint körvonalazva. Bizonyíték a munkafolyamat sebességén.

**A felhőszolgáltatók szabályozás alá esnek a DORA szerint?**

Igen, a 28-44. cikk alatt. A CTPP kijelölési rendszer az európai felügyeleti hatóságoknak közvetlen felügyeletet ad a kijelölt kritikus harmadik feles szolgáltatók felett. Az AWS, a Microsoft (Azure), a Google (GCP) és a Salesforce mind a kijelölési perimeteren belül vagy annak közelében helyezkedik el.

## Hivatkozások

- Európai Unió, (2022). [2022/2554 (EU) rendelet: Digitális működési ellenállóképességi rendelet (DORA) ⧉](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R2554 "DORA").
- Európai Unió, (2024). [2024/1689 (EU) rendelet: mesterséges intelligenciáról szóló rendelet ⧉](https://eur-lex.europa.eu/eli/reg/2024/1689/oj "EU AI Act").
- Európai Bankhatóság, (2019). [EBA/GL/2019/02: iránymutatások a kiszervezési megállapodásokról ⧉](https://www.eba.europa.eu/regulation-and-policy/internal-governance/guidelines-on-outsourcing-arrangements "EBA Outsourcing Guidelines").
- Európai felügyeleti hatóságok, (2024). [Zárójelentés a DORA szerinti információs nyilvántartásról szóló ITS-ről ⧉](https://www.eba.europa.eu/activities/direct-supervision-and-oversight/digital-operational-resilience-act "ESAs ITS").
- Európai Központi Bank, (2024). [TIBER-EU keret ⧉](https://www.ecb.europa.eu/paym/cyber-resilience/tiber-eu/html/index.en.html "TIBER-EU").
- Európai Adatvédelmi Testület, (2020). [01/2020. sz. ajánlás a kiegészítő intézkedésekről ⧉](https://www.edpb.europa.eu/our-work-tools/our-documents/recommendations/recommendations-012020-measures-supplement-transfer_en "EDPB Recommendations 01/2020").
- Egyesült Államok Kereskedelmi Minisztériuma, (2023). [EU-USA adatvédelmi keret ⧉](https://www.dataprivacyframework.gov/list "DPF participant list").
- Európai Bizottság, (2021). [2021/914 (EU) bizottsági végrehajtási határozat: általános szerződési feltételek ⧉](https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj "2021 SCCs").
