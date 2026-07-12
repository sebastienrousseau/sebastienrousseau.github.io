---
title: "Üzenetektől a térképig: globális vállalati szabvány építése az ISO 20022-re és a Swiftre"
tags: "ISO 20022, Swift, CBPR+, corporate banking, CPMI, CGI-MP, cross-border payments, APIs, OpenAPI, FAPI, structured address, treasury, transaction banking, standards, G20 payments"
subtitle: "Az ISO 20022 és a Swift CBPR+ programja harmonizálta, hogy egy határon átnyúló fizetésnek mit kell mondania. Azt nem szabványosították, hogyan használja azt egy vállalat. A letisztult adatrétegtől a hiányzó interfész- és viselkedésrétegig, és hogy a bankok hogyan építhetnek globális vállalati szabványt a már meglévő infrastruktúrájukra, új bizottság nélkül."
description: "Az ISO 20022 és a Swift CBPR+ programja harmonizált globális nyelvet adott a határon átnyúló fizetéseknek, de nem adott globális térképet ahhoz, hogyan használják azt a vállalatok. Hogyan terjeszthető ki a harmonizáció arról, amit egy fizetés mond, arra, ahogyan egy vállalat használja azt, a már meglévő infrastruktúrán."
date: "July 8, 2026"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/shubham-dhage-yKzECK-O9-k.webp"
banner_alt: "Egymáshoz kapcsolódó, izzó blokkok láncot alkotnak egy sötét mezőn: harmonizált ISO 20022 üzenetek egyesülnek egy összekapcsolt hálózattá, felidézve a hiányzó globális térképet, amely a strukturált fizetési adatokat használható vállalati szabvánnyá alakítja"
keywords: "ISO 20022, Swift CBPR+, vállalati banki API-k, CPMI, CGI-MP, MyStandards, határon átnyúló fizetések, camt.053, pain.001, FAPI, OpenAPI, strukturált cím, G20 fizetési ütemterv, tranzakciós banki szolgáltatások, treasury, OAuth2"
---

## Üzenetektől a térképig: globális vállalati szabvány építése az ISO 20022-re és a Swiftre

**Az iparágnak végre van egy globális nyelve a fizetésekhez. Még mindig nincs globális térképe ahhoz, hogy a vállalatok cselekedhessenek alapján.** Az ISO 20022 és a Swift CBPR+ programja gazdag, strukturált, harmonizált adatokat adott a határon átnyúló fizetéseknek, amit a CPMI G20 ütemterv szerinti, 2027 végi adatkövetelményei tovább erősítenek. Amit nem tettek meg: nem mondják meg egy vállalati treasury vezetőnek, vagy a nevében eljáró rendszereknek, hogyan kell azokat az adatokat a valós világban közzétenni, biztosítani, verziózni és mi legyen a rájuk adott viselkedés. A következmény egy furcsa fordítottság: az üzenetek világszerte közelítenek egymáshoz, de az, ahogyan a bankok engedik a vállalatokat használni őket, bankonként töredezett marad. Így juthatnak el a bankok és a pénzügyi intézmények a harmonizált üzenetektől egy globális vállalati szabványig, a már meglévő infrastruktúrájuk használatával.

> **Vezetői összefoglaló**
>
> - **A kényszerítő tényezők már beindultak.** Az ISO 20022 mostanra a határon átnyúló fizetések világszerte használt szabványos nyelve; az MT/MX együttélés 2025 novemberében véget ért, a strukturált címek 2026 novemberében érkeznek, a CPMI harmonizált adatkövetelményei pedig legalább 2027 végéig futnak.
> - **A harmonizáció megállt az üzenet határánál.** A CPMI és a Swift azt szabványosította, *amit egy fizetésnek mondania kell*. Nem szabványosították azt, *ahogyan egy bank engedi egy vállalatnak használni azt*: a csatornát, a hitelesítést, a szolgáltatási szinteket, a hiba- és újrapróbálkozási szemantikát.
> - **A megoldás a meglévő szabványokat terjeszti ki, nem talál fel újat.** Egy globális vállalati szabvány az ISO 20022 és a CBPR+ tetejére épül, és három kérdésre válaszol: mely interfészeken keresztül, mely biztonsági minták alatt és milyen viselkedési garanciákkal használhat egy vállalat ezeket az üzeneteket a bankok között.
> - **Az aszimmetria döntő.** Egy közös interfészprofil megállapításának költségét egyszer, közösen fizetjük meg; azt a költséget, hogy száz kétoldalú integrációra hagyjuk, örökké fizetjük, integrációs órákban és egyeztetési eltérésekben. Egy vállalati szabvány hiánya mostanra döntés arról, hogy nem rajzoljuk meg a térképet.

## Az új alapvonal: az ISO 20022 az adatok szempontjából már nem opcionális

A kiindulópont egyértelmű. 2025 novemberétől a Swift hálózatán a határon átnyúló fizetések és jelentések tekintetében véget ért az MT és az ISO 20022 közötti együttélési időszak a pénzügyi intézmények számára. A CBPR+ mostantól ISO 20022-t követel meg a fizetési megbízásokhoz, a következő mérföldkő pedig már a naptárban van: 2026 novemberétől a strukturálatlan postai címeket eltávolítják a CBPR+ üzenetekből a teljesen strukturált vagy hibrid formátumok javára. Ezzel párhuzamosan a CPMI és a PMPG közzétette a harmonizált ISO 20022 adatkövetelményeket, elkötelezve magukat azok fenntartása mellett legalább 2027 végéig, a gyorsabb, olcsóbb és átláthatóbb határon átnyúló fizetéseket célzó G20 program keretében.

Más szóval a globális közösség konvergált abban, hogy egy fizetésnek mit **kell mondania**. A CPMI saját követelményei mindent lefednek az egyedi, végponttól végpontig terjedő hivatkozásoktól, a strukturált fél- és címinformációtól, valamint az átlátható díjaktól a minimális átutalási mezőkig, mindezt azért, hogy az üzenetek jobban összehasonlíthatók és gépileg olvashatók legyenek a piacok között. A Swift ezt konkrét CBPR+ irányelvekké és határidőkké fordította le, amelyeket a hálózat szintjén érvényesítenek. Ez az adatréteg: gazdag, strukturált, harmonizált.

## Amit a Swift és az ISO 20022 már ad a vállalatoknak

A vállalatok nem utólagos gondolatok ebben a történetben. A Swift egy évtizeden át építette ki az „ISO 20022 vállalatoknak” megközelítést és a kapcsolódó piaci gyakorlatot, és az előnyök valódiak.

Az üzenet szintjén az ISO 20022 a következőket kínálja a vállalatoknak:

- **Jobb egyeztetés**, a strukturált átutalási információk és a végponttól végpontig terjedő azonosítók használatával a pain és camt üzenetekben, ami felgyorsítja a követelések párosítását és csökkenti a kézi munkát.
- **Jobb forgótőke-menedzsment**, mivel a készpénzjelentésben (camt.052/053/054) szereplő gazdagabb és strukturáltabb adatok pontosabb előrejelzést tesznek lehetővé a beérkező és kimenő pénzáramlásokról.
- **Támogatás a nevében eljáró (on-behalf-of) modellekhez és a virtuális számlákhoz**, a végső adós/hitelező, a kezdeményező fél és más szerepkörök dedikált mezőin keresztül, amelyeket a régi MT struktúra sosem úgy tervezett, hogy tisztán hordozzon.

A Swift vállalati munkája nem korlátozódott elméletre. A SCORE keretrendszer és a CGI-MP (Common Global Implementation, Market Practice) csoport részletes ISO 20022 használati irányelveket dolgozott ki a vállalati fizetéskezdeményezésre és a készpénzkezelési üzenetekre. A bankok és vállalatok ezeket a sablonokat használják, amelyeket a MyStandardsön tesznek közzé és éles kísérletekkel finomítanak, hogy elkerüljék az új dialektusok kitalálását minden egyes kapcsolathoz. Az olyan esettanulmányok, mint a SEB korai ISO 20022 bevezetése vállalatok számára, azt mutatják, hogy a multinacionális cégek egyetlen pain.001 és camt változatra szabványosíthatnak több bank és piac között, mérhető hatékonyság- és kontrollnövekedéssel.

Tehát az építőelemek léteznek. A vállalatoknak tiszta képük van az előnyökről; a bankoknak vannak üzenet-irányelveik és példáik; a CPMI harmonizálta a minimális adatkészletet a joghatóságok között. Amit mindebből még semmi sem ad meg, az egy globálisan egységes válasz egy másik kérdésre: nem az, hogy „hogyan nézzen ki az üzenet?”, hanem hogy „hogyan engedje egy bank egy vállalatnak használni azt?”

## A hiányzó réteg: a harmonizált üzenetektől a vállalati szabványig

A megkülönböztetés finomnak hangzik, de ez a különbség egy szótár és egy közlekedési rendszer között. Az ISO 20022 és a CPMI megmondja a szavakat és a nyelvtant, amelyeknek végponttól végpontig kell utazniuk. Nem mondják meg:

- Hogy a vállalat fájlokon, portálokon, host-to-host csatornákon vagy API-kon keresztül éri-e el ezeket az üzeneteket, vagy hogy ezek közül melyiket kezelik elsőrangúként.
- Hogyan hitelesítik ezek a csatornák az ügyfeleket: saját tulajdonú tanúsítványokkal, kézi engedélyezőlistákkal vagy modern OAuth2/mTLS profilokkal.
- Milyen nem funkcionális viselkedést feltételezhet a vállalat: késleltetési kereteket, rendelkezésre állást, határidő-érvényesítést és STP-elvárásokat.
- Hogyan jelzik a hibákat, és milyen újrapróbálkozási minták biztonságosak, különösen akkor, amikor automatizáció és ügynökök cselekszenek ezekkel a csatornákkal szemben.

Ez a hézag most jobban számít, mint 2015-ben. Akkor az integrátor egy ember volt, a horizont pedig vállalatonként néhány bank. Ma a nagyvállalatok és platformjaik valós idejű láthatóságot, közvetlen kezdeményezést és gépi vezérlésű egyeztetést várnak el több tucat partnernél, és egyre inkább API-kon, nem pedig lapos fájlokon keresztül. Az ISO 20022 gazdagabb adatokat adott nekik. Önmagában nem adott nekik kiszámítható interfészt.

Egy hiteles **globális vállalati szabványnak** kifejezetten az ISO 20022 és a CBPR+ alapvonal tetejére kell épülnie, ugyanazokat a harmonizált üzeneteket használva, és három kérdésre kell válaszolnia: mely interfészeken keresztül, mely biztonsági minták alatt és milyen viselkedési garanciákkal használhatja egy vállalat megbízhatóan ezeket az üzeneteket a bankok között?

## Amit egy globális vállalati szabványnak hozzá kell tennie

A jó hír az, hogy a bankoknak nem kell egy új szabványt a nulláról feltalálniuk. Ki kell terjeszteniük azokat, amelyekkel már rendelkeznek.

### 1. Rögzítsük az üzenetréteget: fogadjuk el a harmonizált ISO 20022 sablonokat

Először is, a bankoknak és a vállalatoknak el kell kötelezniük magukat amellett, hogy a CPMI harmonizált adatkövetelményeit és a meglévő Swift/CGI-MP sablonokat **nem alku tárgyát képező alapvonalként** kezeljék a határon átnyúló vállalati folyamatoknál.

Ez a következőket jelenti:

- Harmonizált ISO 20022 üzenetek (pain, pacs, camt) használata a határon átnyúló fizetésekhez és készpénzjelentéshez, a CBPR+-hoz és a 2026 novemberi követelményekhez igazított strukturált és hibrid címekkel.
- Az egyedi bővítések elkerülése, hacsak nem feltétlenül szükségesek, és ha mégis azok, dokumentálásuk a MyStandardsön, hogy felfedezhetők és újrahasználhatók legyenek, ahelyett, hogy a sötétben burjánzanának.
- Annak biztosítása, hogy a belső rendszerek ténylegesen megőrizzék a gazdagított ISO 20022 adatokat, ahelyett, hogy azokat a maghoz érve visszalapítanák MT-szerű struktúrákká.

Ez a „mit mondjunk” réteg: a CPMI definiálja a harmonizált adatmodellt; a Swift üzemszerűvé teszi a CBPR+-ban; a CGI-MP pedig konkrét sablonokat ad a vállalatoknak és a bankoknak, amelyeket követhetnek.

### 2. Szabványosítsuk az interfészréteget: API-profilok, nem csak fájlok

Másodszor, a bankoknak és a pénzügyi intézményeknek el kell dönteniük, hogy az ISO 20022 alapú fizetések és készpénzjelentés **elsődleges vállalati interfésze** közös profilú API-k lesznek, nem pedig fájlok és portálok foltvarrottsága.

Ez a következőkkel jár:

- A vállalati fizetéskezdeményezés (pain.001) és a készpénzkezelési üzenetek (camt.052/053/054) közzététele REST API-kon keresztül, szabványos lapozási, korrelációs és szűrési mintával.
- OpenAPI specifikációk közzététele ezekhez az API-khoz ugyanott, ahol a vállalatok már keresik a használati irányelveket, például az ISO 20022 sablonok mellett a MyStandardsön vagy azzal egyenértékű portálokon.
- Elkötelezettség a hitelesítési modellek korlátozott halmaza mellett, lehetőleg FAPI-szintű OAuth2.1 kölcsönös TLS-sel a vállalati API-khoz, az egyedi SFTP-kulcsok, ad-hoc IP-engedélyezőlisták és bankspecifikus tanúsítványrituálék helyett.

A Swift saját, vállalatoknak szóló útmutatása már utal ebbe az irányba, ahogy a nagy bankok ISO 20022 migrációs kézikönyvei is, amelyek egyre inkább összekötik az üzenetek készenlétét az API-k bevezetésével a vállalati ügyfelek számára. Egy globális vállalati szabvány ezt explicitté tenné: ugyanazoknak az ISO 20022 üzenetdefinícióknak elérhetőnek kell lenniük néhány kiszámítható API-mintán keresztül.

### 3. Definiáljuk a viselkedésréteget: SLO-k, hibaszemantika és újrapróbálkozások

Harmadszor, a szabványnak el kell ismernie, hogy a vállalatok, és különösen a treasury rendszereik és ügynökeik számára, **az, ahogyan az interfész viselkedik**, ugyanolyan fontos, mint az, ahogyan az üzenet kinéz.

Itt a bankoknak és a pénzügyi intézményeknek legalább regionálisan össze kell hangolniuk a következőket:

- Nem funkcionális szolgáltatási szintek:
 - Késleltetési elvárások a fizetéskezdeményezés, az állapotfrissítések és a készpénzjelentési hívások esetén.
 - Rendelkezésre állási célok és tervezett karbantartási ablakok.
 - Közvetlen feldolgozási (STP) elvárások és határidő-viselkedés az aznapi és a határon átnyúló folyamatoknál.
- Egy közös hibamodell:
 - Közös hibakódok és kategóriák (validációs hiba, határidő-elmulasztás, likviditási probléma, megfelelőségi tartás, technikai hiba), amelyek tisztán leképezhetők az intézmények között.
 - Világos útmutatás arról, hogy mi próbálható újra, mit nem szabad újrapróbálni, és hogyan viselkedjenek az idempotencia-kulcsok a fizetéskezdeményezési hívások között.

E viselkedésréteg nélkül a vállalatok továbbra is minden bankot különálló integrációs projektként kezelnek majd, még akkor is, ha mindegyik pain.001-et küld és camt.053-at fogad. Ezzel a réteggel a bankkapcsolatot inkább csereszabatos komponensként kezelhetik: ugyanazok az üzenetek, ugyanaz az API-minta, ugyanaz a szemantika az „elfogadva”, „függőben”, „sikertelen” és „ne próbáld újra” állapotokra.

## Hogyan hangolhatják össze a bankok és a pénzügyi intézmények magukat új bizottság nélkül

A kísértés, amikor egy újabb szabványosítási hézaggal szembesülünk, az, hogy új fórumot találjunk ki. Erre itt nincs szükség. Az intézmények, amelyek már gondozzák az ISO 20022-t, egy réteggel feljebb terjeszthetik ki hatáskörüket.

Három fórum kézenfekvő:

- **A Swift és vállalati programjai.** A Swift már most is a CBPR+, a CGI-MP és a vállalati használati irányelvek gyűjtőpontja. Otthont adhat referencia API-profiloknak és viselkedési ajánlásoknak, például kanonikus OpenAPI specifikációkat és hibataxonómiákat téve közzé a meglévő ISO 20022 üzenetsablonok mellett.
- **A CPMI harmonizált adatkormányzása.** A CPMI elkötelezte magát amellett, hogy fenntartja és fejleszti harmonizált ISO 20022 követelményeit legalább 2027-ig, piaci gyakorlati csoportok testületének támogatásával. Bár a CPMI az adatokra összpontosít, kifejezetten ösztönözheti a piacokat, hogy konzisztens interfészszabványokat építsenek ezekre az adatokra, elkerülve az eltérést az „amit küldünk” és az „ahogyan használjuk” között.
- **Regionális és globális piaci gyakorlati csoportok.** Azok a csoportok, amelyek már összehangolják az ISO 20022 megvalósítást, a CGI-MP-től a regionális fizetési tanácsokig, közös API- és SLO-profilokat fogadhatnak el munkájuk részeként, ahelyett, hogy az interfész viselkedését kétoldalú tárgyalásokra hagynák.

Itt nem arról van szó, hogy a CPMI-t vagy a Swiftet API-szabályozóvá alakítsuk. Arról van szó, hogy a meglévő közösségeket használjuk annak elfogadására, hogy **ugyanazokat a harmonizált üzeneteket ne vegyék körül végtelenül egyedi interfészek**.

## Egy fokozatos megközelítés a következő három évre

Azoknak a bankoknak és pénzügyi intézményeknek, amelyek vezetni akarnak, nem pedig követni, az út lépésenkénti és összhangban áll azokkal a mérföldkövekkel, amelyekkel amúgy is szembenéznek.

### 1. fázis: fejezzük be az adatmunkát, végponttól végpontig

- Fejezzük be a határon átnyúló MT üzenetek ISO 20022-re migrálását a CBPR+ számára ott, ahol még hátra van, és biztosítsuk, hogy a belső rendszerek megőrizzék a strukturált ISO adatokat, ahelyett, hogy a szélen lecsupaszítanák.
- Igazítsuk a vállalati fizetéskezdeményezési és készpénzjelentési üzeneteket a CBPR+ és a CGI-MP sablonokhoz, elkerülve a harmonizációt megtörő bankspecifikus eltéréseket.
- Valósítsuk meg a strukturált és hibrid postai címeket a 2026 novemberi határidő előtt, mind a banki, mind a vállalati csatornákon, hogy a vállalatok egyetlen címzési modellre támaszkodhassanak.

### 2. fázis: tegyük az API-kat elsőrangú vállalati csatornákká

- Tegyük közzé az ISO 20022-höz igazított fizetéskezdeményezést és készpénzjelentést REST API-kon keresztül, a piacok és üzletágak közötti közös profillal.
- Fogadjuk el a FAPI-szintű OAuth2.1-et kölcsönös TLS-sel alapértelmezett biztonsági modellként ezekhez az API-khoz, felváltva vagy háttérbe szorítva az egyedi, fájlalapú hitelesítési mechanizmusokat.
- Tegyük közzé az OpenAPI specifikációkat és a fejlesztői útmutatókat úgy, hogy a vállalatok könnyen összehasonlíthassák őket a bankok között, ideális esetben egy közös tárolóban vagy portálon, amelyre a Swift vagy iparági csoportok hivatkoznak.

### 3. fázis: szabványosítsuk a viselkedést, és kormányozzuk azt

- Csatlakozzunk munkacsoportokhoz, vagy segítsünk létrehozni azokat, a Swift, a CGI-MP vagy regionális tanácsok alatt, hogy közös hibakódokat, idempotencia-irányelveket és újrapróbálkozási mintákat definiáljunk a vállalati ISO 20022 API-khoz.
- Állítsunk fel és tegyünk közzé SLO-kat a késleltetésre, a rendelkezésre állásra és az STP-re a vállalati fizetéskezdeményezési és jelentési API-khoz, és felügyeljük őket olyan szigorúan, ahogy a CBPR+ megfelelést felügyeljük.
- Ösztönözzük a vállalatokat és a treasury platformokat, hogy ezekre a közös profilokra építsenek, a korai alkalmazókat referenciaesetként használva, ahogy a Swift és mások már megtették az ISO 20022 üzenetkezeléssel.

Maguk a vállalatok számára a program párhuzamos:

- Modernizálják az ERP- és TMS-platformokat ISO 20022-natívvá, beleértve a strukturált átutalás és címek támogatását, valamint a camt készpénzjelentés teljes fogyasztását.
- Részesítsék előnyben azokat a bankkapcsolatokat, amelyek ISO 20022-höz igazított API-kat kínálnak átlátható szolgáltatási szintekkel és harmonizált szemantikával, nem csak „ISO 20022 fájlon keresztül” megoldást.
- Használják a gazdagabb adatokat és a kiszámítható viselkedést a belső folyamatok, az egyeztetés, az előrejelzés, az OBO modellek szabványosítására az összes bank között, ahelyett, hogy egyesével tennék.

## A lehetőség és a kockázat

A kényszerítő tényezők már mozgásban vannak. Az ISO 20022 mostanra a határon átnyúló fizetések világszerte használt szabványos nyelve, az együttéléssel a hátunk mögött és a strukturált adatok hálózati szintű érvényesítésével. A CPMI harmonizált adatkövetelményei Frankfurttól Washingtonig beépülnek a piaci gyakorlatba és a szabályozói elvárásokba. A bankok jelentős összegeket fektetnek az ISO 20022 migrációkba és a vállalati API-k bevezetésébe; a vállalatok fejlesztik az ERP-ket és TMS-eket az új üzenetek kezelésére.

A kérdés az, hogy ez a hullám megáll-e az üzenet határánál, vagy átvezet-e a vállalati élménybe. Ha a bankok az ISO 20022-t tisztán üzenetkezelési frissítésként kezelik, a vállalatok továbbra is egy olyan világban élnek, ahol ugyanaz a fizetés hasonlóan néz ki a vezetéken, de minden banknál másképp érhető el, kontrollálható és értelmezhető. Ha viszont a bankok az ISO 20022-t és a Swift keretrendszereit egy globális vállalati szabvány **alapjaként** használják, kiterjesztve a harmonizációt a „mit”-ről a „hogyan”-ra, akkor a vállalatok végre megkaphatják azt, amit a G20 napirend évek óta ígér: gyorsabb, olcsóbb, átláthatóbb határon átnyúló fizetéseket, amelyek valóban szabványosítottak, nem csak szerkezetileg hasonlóak.

Van itt egy ismerős aszimmetria. Egy közös interfészprofil megállapításának költségét egyszer, közösen fizetjük meg. Azt a költséget, hogy száz kétoldalú megállapodásra hagyjuk, örökké, egyenként fizetjük meg, integrációs órákban, egyeztetési eltérésekben és az automatizáció elszalasztott lehetőségeiben. Egy olyan világban, ahol a vállalatok, a platformok és egyre inkább az ügynökök is készen állnak az ISO 20022 natív fogyasztására, egy globális vállalati szabvány hiánya kevésbé a táj egy hézagja, inkább döntés arról, hogy nem rajzoljuk meg a térképet.

## Gyakran ismételt kérdések

**Az ISO 20022 még mindig opcionális a határon átnyúló fizetéseknél?**
Nem. 2025 novemberétől a Swift hálózatán a határon átnyúló fizetések és jelentések MT/MX együttélési időszaka véget ért a pénzügyi intézmények számára, és a CBPR+ ISO 20022-t követel meg a fizetési megbízásokhoz. A következő mérföldkő már rögzített: 2026 novemberétől a strukturálatlan postai címeket eltávolítják a CBPR+ üzenetekből a strukturált vagy hibrid formátumok javára.

**Ha az üzenetek harmonizáltak, mi hiányzik még?**
Az interfész. A CPMI és a Swift azt szabványosította, *amit* egy fizetésnek mondania kell: egy gazdag, strukturált, összehasonlítható adatkészletet. Nem szabványosították azt, *ahogyan* egy bank engedi egy vállalatnak elérni és használni azt: melyik csatorna elsőrangú, hogyan hitelesít, milyen késleltetést és rendelkezésre állást feltételezhet a vállalat, és hogyan viselkednek a hibák és az újrapróbálkozások. Ez a különbség egy szótár és egy közlekedési rendszer között.

**Szükségük van a bankoknak egy új szabványügyi bizottságra ennek megoldásához?**
Nem. Az intézmények, amelyek már gondozzák az ISO 20022-t, egy réteggel feljebb terjeszthetik ki hatáskörüket. A Swift már összehívja a CBPR+, a CGI-MP és a vállalati használati irányelveket, és otthont adhat referencia API-profiloknak és hibataxonómiáknak; a CPMI, amely a harmonizált adatkészletet 2027 végéig kormányozza, ösztönözheti a konzisztens interfészszabványokat ezen adatok tetején; a regionális piaci gyakorlati csoportok pedig közös API- és SLO-profilokat fogadhatnak el.

**Mit tegyen egy bank először?**
Fejezze be az adatmunkát végponttól végpontig: őrizze meg a strukturált ISO 20022-t, ahelyett, hogy a maghoz érve lelapítaná, és valósítsa meg a strukturált és hibrid címeket a 2026 novemberi határidő előtt. Aztán tegye az API-kat elsőrangú vállalati csatornává egy közös FAPI-szintű profillal és közzétett OpenAPI specifikációkkal. Aztán szabványosítsa a viselkedést: közös hibakódok, idempotencia-útmutatás és közzétett SLO-k, amelyeket olyan szigorúan felügyel, mint a CBPR+ megfelelést.

## Hivatkozások

- [Bank for International Settlements (CPMI), *Harmonised ISO 20022 data requirements for enhancing cross-border payments*](https://www.bis.org/cpmi/publ/d230.htm "BIS CPMI — Harmonised ISO 20022 data requirements") ⧉. [A 2027 végi harmonizált adatkészlet a G20 határon átnyúló fizetési program keretében, az „amit egy fizetésnek mondania kell” réteg, amelyre ez az elemzés épül.]
- [Swift, *ISO 20022 — a new era for global payments*](https://www.swift.com/news-events/news/iso-20022-new-era-global-payments "Swift — ISO 20022 for global payments") ⧉. [A CBPR+ program; az MT/MX együttélés 2025 novemberében véget ért a határon átnyúló fizetéseknél és jelentéseknél, hálózati szinten érvényesítve.]
- [Swift, *ISO 20022 milestone: November 2026, unstructured addresses to be removed*](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "Swift — November 2026 structured-address milestone") ⧉. [A strukturált / hibrid cím követelmény a CBPR+ üzenetekhez.]
- [Swift, *ISO 20022 for corporates*](https://www.swift.com/corporates/iso-20022-corporates "Swift — ISO 20022 for corporates") ⧉. [SCORE és CGI-MP használati irányelvek; vállalati előnyök az egyeztetésben, a forgótőke-menedzsmentben és a nevében eljáró modellekben.]
- [Federal Reserve Financial Services, *Understanding ISO 20022*](https://fedpaymentsimprovement.org/wp-content/uploads/understanding-iso-20022.pdf "Federal Reserve — Understanding ISO 20022") ⧉. [Strukturált átutalás, camt készpénzjelentés, valamint a fent említett vállalati egyeztetési és előrejelzési nyereségek.]
- [Swift, *ISO 20022 harmonisation charter*](https://www.swift.com/sites/default/files/documents/swift_standards_iso20022_harmonisation_charter_factsheet.pdf "Swift — ISO 20022 harmonisation charter") ⧉. [MyStandards, CGI-MP sablonok és a bővítések dokumentálásának fegyelme az egyedi dialektusok burjánoztatása helyett.]

*Utoljára ellenőrizve: 2026 július. Eredeti elemzés; a források hivatkozottak, nem reprodukáltak. A számok és időzítések gyorsan változnak ezen a területen; újraközlés előtt ellenőrizze őket elsődleges forrásokból. A CC-BY-4.0 licenc alatt.*
